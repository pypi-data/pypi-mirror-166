"""Base classes for IO to/from SLURM python jobs
"""

import logging
from contextlib import contextmanager
from numbers import Number
from typing import Any, Iterator, List, Optional, Tuple
from collections.abc import MutableMapping as AbcMutableMapping
from weakref import WeakValueDictionary
from ..errors import NoResultError


logger = logging.getLogger(__name__)


class JobFuture:
    def __init__(self, job_id: int) -> None:
        self.job_id = job_id

    def __repr__(self):
        return f"JobFuture({self.job_id})"

    def cancel(self) -> bool:
        """Non-blocking and returns `True` when cancelled."""
        raise NotImplementedError

    def result(self, timeout: Optional[Number] = None) -> Any:
        """Waits for the result indefinitely by default.

        :raises:
            NoResultError: the job has not result for unknown reasons
            PendingResultError: the job is not finished
            CancelledResultError: the job IO was cancelled
            Exception: the exception raised by the job
        """
        raise NotImplementedError

    def fetch(self, timeout: Optional[Number] = None) -> Any:
        """Never raises an exception."""
        raise NotImplementedError


ResultType = Any


class JobResults(AbcMutableMapping):
    def __init__(self) -> None:
        self._futures = dict()

    def __getitem__(self, job_id: int) -> ResultType:
        return self.get_future(job_id).result(timeout=0)

    def __setitem__(self, job_id: int, value: JobFuture):
        self._futures[job_id] = value

    def __delitem__(self, job_id: int) -> None:
        try:
            self.cancel(job_id)
        except NoResultError:
            pass
        del self._futures[job_id]

    def __iter__(self) -> Iterator:
        return iter(self._futures)

    def __len__(self) -> int:
        return len(self._futures)

    def cancel(self, job_id: int, timeout: Optional[Number] = 0) -> None:
        future = self.get_future(job_id)
        future.fetch(timeout=timeout)
        future.cancel()

    def fetch(self, job_id: int, timeout: Optional[Number] = 0) -> None:
        self.get_future(job_id).fetch(timeout=timeout)

    def get_future(self, job_id: int):
        try:
            return self._futures[job_id]
        except KeyError:
            raise NoResultError(
                f"SLURM job {job_id} result no longer in memory"
            ) from None


class JobIoHandler:
    _JOB_FUTURE_CLASS = JobFuture

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        return False

    @property
    def _local_results(self) -> WeakValueDictionary:
        return self.__local_results

    @property
    def _job_results(self) -> JobResults:
        return self.__job_results

    @contextmanager
    def start_job_io(
        self, data: Any, timeout: Optional[Number] = None
    ) -> Tuple[str, dict, JobFuture]:
        """Returns the script, environment variables and pending result parameters"""
        raise NotImplementedError

    def _finalize_start_job_io(self, jobfuture: JobFuture):
        if jobfuture.job_id is None:
            jobfuture.cancel()
            return
        self._job_results[jobfuture.job_id] = jobfuture
        self._local_results[jobfuture.job_id] = jobfuture

    def stop_job_io(self, job_id: str, timeout: Optional[Number] = 0) -> None:
        """Stop IO and keep result"""
        self._job_results.cancel(job_id, timeout=timeout)

    def cleanup_job_io(self, job_id: str) -> None:
        """Stop IO and delete result"""
        logger.debug("[JOB ID=%s] cleanup SLURM job IO", job_id)
        try:
            del self._job_results[job_id]
        except KeyError:
            pass

    def get_job_ids(self) -> List[int]:
        return list(self._local_results)

    def cleanup(self) -> None:
        for job_id in self.get_job_ids():
            self.cleanup_job_io(job_id)

    def get_job_result(self, job_id: str) -> ResultType:
        return self._job_results[job_id]

    def wait_job_result(self, job_id: str, timeout: Optional[Number] = 0) -> None:
        self._job_results.fetch(job_id, timeout=timeout)
