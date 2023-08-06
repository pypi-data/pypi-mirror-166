"""IO to/from SLURM python jobs over TCP
"""

import pickle
import socket
import time
import logging
from numbers import Number
from contextlib import contextmanager
from typing import Any, Optional, Tuple
from dataclasses import dataclass
from threading import Event
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from concurrent.futures import CancelledError
from weakref import WeakValueDictionary
from . import base
from ..errors import CancelledResultError
from ..errors import PendingResultError
from ..errors import NoResultError

logger = logging.getLogger(__name__)


@dataclass
class JobFuture(base.JobFuture):
    def __init__(self, job_id: int, future: Future, stop: Event) -> None:
        super().__init__(job_id)
        self._future = future
        self._stop = stop
        self._has_result = False
        self._result = None
        self._cancelled = False
        future.add_done_callback(self._fetch)

    def _fetch(
        self,
        future: Future,
        error_on_pending: bool = False,
        timeout: Optional[Number] = 0,
    ) -> None:
        """
        :raises:
            PendingResultError: when timeout is reached with `error_on_pending=True`
        """
        if self._has_result:
            return
        try:
            result = future.result(timeout=timeout)
        except FutureTimeoutError:
            if not error_on_pending:
                return
            raise PendingResultError(f"SLURM job {self.job_id} has no result yet")
        except CancelledError:
            self._cancelled = True
            self._has_result = True
            self._future = None
            return
        except BaseException as e:
            result = e
        self._result = result
        self._has_result = True
        self._future = None

    def fetch(self, timeout: Optional[Number] = 0) -> None:
        future = self._future
        if future is None:
            return
        self._fetch(future, timeout=timeout)

    def cancel(self) -> bool:
        future = self._future
        if future is None:
            return True
        logger.debug("[JOB ID=%s] cancel SLURM job IO ...", self.job_id)
        self._stop.set()
        future.cancel()
        logger.debug("[JOB ID=%s] SLURM job IO cancelled", self.job_id)
        return future.done()

    def result(self, timeout: Optional[Number] = None) -> Any:
        future = self._future
        if future is not None:
            self._fetch(future, timeout=timeout, error_on_pending=True)
        if not self._has_result:
            raise NoResultError(f"SLURM job {self.job_id} has no result")
        if self._cancelled:
            return CancelledResultError(f"SLURM job {self.job_id} IO was cancelled")
        if isinstance(self._result, BaseException):
            raise self._result
        return self._result


_RESULTS = base.JobResults()


class JobTcpIoHandler(base.JobIoHandler):
    def __init__(
        self, max_workers: Optional[int] = None, global_results: bool = False
    ) -> None:
        self.__local_results = WeakValueDictionary()
        if global_results:
            self.__job_results = _RESULTS
        else:
            self.__job_results = base.JobResults()
        self.__executor = ThreadPoolExecutor(max_workers=max_workers)

    @property
    def _local_results(self) -> WeakValueDictionary:
        return self.__local_results

    @property
    def _job_results(self) -> base.JobResults:
        return self.__job_results

    def __enter__(self):
        self.__executor.__enter__()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.__executor.__exit__(exc_type, exc_val, exc_tb)
        return False

    def cleanup(self, wait: bool = True) -> None:
        logger.debug("Cleanup SLURM TCP IO handler ...")
        super().cleanup()
        self.__executor.shutdown(wait=True)
        logger.debug("SLURM TCP IO cleaned up")

    @contextmanager
    def start_job_io(
        self, data: Any, timeout: Optional[Number] = None
    ) -> Tuple[str, dict, JobFuture]:
        host, port = _get_free_port()
        online_event = Event()
        stop_event = Event()
        future = self.__executor.submit(
            _send_end_receive, host, port, data, online_event, stop_event
        )
        if not online_event.wait(timeout):
            raise TimeoutError(f"Job IO did not start in {timeout} seconds")
        future = JobFuture(0, future, stop_event)
        environment = {
            "_PYSLURMUTILS_HOST": host,
            "_PYSLURMUTILS_PORT": port,
        }
        try:
            yield _PYTHON_SCRIPT, environment, future
        finally:
            self._finalize_start_job_io(future)


def _send_end_receive(
    host: str, port: int, data: Any, online_event: Event, stop_event: Event
) -> Any:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        online_event.set()
        logger.debug("Wait until the SLURM job started and connects ...")
        sock.settimeout(0.5)
        conn = None
        while not stop_event.is_set():
            try:
                conn, _ = sock.accept()
                break
            except socket.timeout:
                pass
        if conn is None:
            raise CancelledResultError(
                "Cancelled before making a connection to the SLURM job"
            )
        logger.debug("SLURM job connected. Send work ...")
        conn.settimeout(10)
        _send(conn, data)
        logger.debug("SLURM job work send, wait for result ...")
        conn.settimeout(None)
        result = _receive(conn, stop_event)
        logger.debug("SLURM job result received")
        return result


def _send(sock: socket.socket, data: Any) -> None:
    bdata = pickle.dumps(data)
    sock.sendall(len(bdata).to_bytes(4, "big"))
    sock.sendall(bdata)


def _receive(
    sock: socket.socket, stop_event: Event, period: Optional[Number] = None
) -> Any:
    data = _receive_nbytes(sock, 4, stop_event, period)
    nbytes = int.from_bytes(data, "big")
    data = _receive_nbytes(sock, nbytes, stop_event, period)
    if not data:
        raise CancelledResultError("SLURM job returned nothing (most likely cancelled)")
    return pickle.loads(data)


def _receive_nbytes(
    sock: socket.socket, nbytes: int, stop_event: Event, period: Optional[Number] = None
) -> bytes:
    data = b""
    block = min(nbytes, 512)
    if period is None:
        period = 0.5
    while not stop_event.is_set() and len(data) < nbytes:
        data += sock.recv(block)
        time.sleep(period)
    return data


def _get_free_port() -> Tuple[str, int]:
    with socket.socket() as sock:
        sock.bind(("", 0))
        port = sock.getsockname()[-1]
        host = socket.gethostbyname(socket.gethostname())
        return host, port


def job_test_client(env, response=None):
    host = env.get("_PYSLURMUTILS_HOST")
    port = int(env.get("_PYSLURMUTILS_PORT"))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((host, port))
        data = _receive(s, Event())
        if response is not None:
            _send(s, response)
        return data


_PYTHON_SCRIPT = """
import os,sys,pickle,socket,time,traceback
print("Python version: %s" % sys.version)
print("working directory: %s" % os.getcwd())

def send(s, data):
    bdata = pickle.dumps(data)
    nbytes = len(bdata)
    s.sendall(nbytes.to_bytes(4, "big"))
    s.sendall(bdata)

def receive_nbytes(s, nbytes):
    data = b""
    block = min(nbytes, 512)
    while len(data) < nbytes:
        data += s.recv(block)
        time.sleep(0.1)
    return data

def receive(s):
    data = receive_nbytes(s, 4)
    nbytes = int.from_bytes(data, "big")
    data = receive_nbytes(s, nbytes)
    return pickle.loads(data)

host = os.environ.get("_PYSLURMUTILS_HOST")
port = int(os.environ.get("_PYSLURMUTILS_PORT"))
try:
    hostname = socket.gethostbyaddr(host)[0]
except Exception:
    hostname = host
hostport = "%s:%s" % (hostname, port)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to", hostport, "...")
    s.settimeout(10)
    s.connect((host, port))

    try:
        print("Receiving work from", hostport, "...")
        func, args, kw = receive(s)

        print("Executing work:", func)
        if args is None:
            args = tuple()
        if kw is None:
            kw = dict()
        result = func(*args, **kw)
    except Exception as e:
        traceback.print_exc()
        result = e

    print("Sending result", type(result), "to", hostport, "...")
    try:
        send(s, result)
    except Exception:
        traceback.print_exc()
        print("JOB succeeded but client went down first")
"""
