"""IO to/from SLURM python jobs over file
"""

import logging
import time
from contextlib import contextmanager
from numbers import Number
from typing import Any, Optional, Tuple
import pickle
from weakref import WeakValueDictionary
from ..errors import NoResultError
from ..errors import PendingResultError
from ..errors import CancelledResultError
from . import base

logger = logging.getLogger(__name__)


_RESULTS = base.JobResults()


class JobFuture(base.JobFuture):
    def __init__(self, job_id: int, filename: str) -> None:
        super().__init__(job_id)
        self._filename = filename
        self._cancelled = False
        self._has_result = False
        self._result = None

    def cancel(self) -> bool:
        self._cancelled = True
        return True

    def _read_job_result(self, timeout: Optional[Number] = None):
        """
        :raises:
            TimeoutError:
        """
        t0 = time.time()
        filename = self._filename.replace("%j", str(self.job_id))
        while True:
            try:
                with open(filename, "rb") as f:
                    return pickle.load(f)
            except FileNotFoundError:
                pass
            if self._cancelled:
                return
            if timeout is not None and (time.time() - t0) > timeout:
                raise TimeoutError(timeout)

    def _fetch(
        self, error_on_pending: bool = False, timeout: Optional[Number] = 0
    ) -> None:
        """
        :raises:
            PendingResultError: when timeout is reached with `error_on_pending=True`
        """
        try:
            result = self._read_job_result(timeout=timeout)
        except TimeoutError:
            if not error_on_pending:
                return
            raise PendingResultError(f"SLURM job {self.job_id} has no result yet")
        self._result = result
        self._has_result = True

    def fetch(self, timeout: Optional[Number] = 0) -> None:
        self._fetch(timeout=timeout)

    def result(self, timeout: Optional[Number] = None) -> Any:
        if not self._has_result:
            self._fetch(timeout=timeout, error_on_pending=True)
        if self._cancelled:
            raise CancelledResultError(f"SLURM job {self.job_id} IO was cancelled")
        if not self._has_result:
            raise NoResultError(f"SLURM job {self.job_id} has no result")
        if isinstance(self._result, BaseException):
            raise self._result
        return self._result


class JobFileIoHandler(base.JobIoHandler):
    def __init__(self, global_results: bool = False) -> None:
        self.__local_results = WeakValueDictionary()
        if global_results:
            self.__job_results = _RESULTS
        else:
            self.__job_results = base.JobResults()

    @property
    def _local_results(self) -> WeakValueDictionary:
        return self.__local_results

    @property
    def _job_results(self) -> base.JobResults:
        return self.__job_results

    def cleanup(self, wait: bool = True) -> None:
        logger.debug("Cleanup SLURM FILE IO handler ...")
        super().cleanup()
        logger.debug("SLURM FILE IO cleaned up")

    @contextmanager
    def start_job_io(
        self, data: Any, infile: str, outfile: str
    ) -> Tuple[str, dict, JobFuture]:
        with open(infile, "wb") as f:
            pickle.dump(data, f)
        environment = {"_PYSLURMUTILS_INFILE": infile, "_PYSLURMUTILS_OUTFILE": outfile}
        future = JobFuture(0, outfile)
        try:
            yield _PYTHON_SCRIPT, environment, future
        finally:
            self._finalize_start_job_io(future)


_PYTHON_SCRIPT = """
import os,sys,pickle
print("Python version: %s" % sys.version)
print("working directory: %s" % os.getcwd())

infile = os.environ.get("_PYSLURMUTILS_INFILE")
try:
    outfile = os.environ.get("_PYSLURMUTILS_OUTFILE")
    outfile = outfile.replace("%j", os.environ["SLURM_JOB_ID"])

    try:
        print("Reading work from", infile)
        with open(infile, "rb") as f:
            func,args,kw = pickle.load(f)

        print("Executing work:", func)
        if args is None:
            args = tuple()
        if kw is None:
            kw = dict()
        result = func(*args, **kw)
    except Exception as e:
        import traceback
        traceback.print_exc()
        result = e

    with open(outfile, "wb") as f:
        pickle.dump(result, f)
finally:
    if infile:
        os.remove(infile)
"""
