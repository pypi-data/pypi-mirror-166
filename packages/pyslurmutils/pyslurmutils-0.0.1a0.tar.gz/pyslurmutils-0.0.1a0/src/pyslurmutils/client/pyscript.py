import os
import time
import logging
import json
from uuid import uuid4
from typing import Any, Callable, Mapping, Optional, Tuple
from .script import SlurmScriptApi
from .job_io import tcp_io
from .job_io import file_io
from . import config

logger = logging.getLogger(__name__)


class SlurmPythonJobApi(SlurmScriptApi):
    def __init__(
        self,
        *args,
        data_directory=None,
        global_results: bool = False,
        max_workers: Optional[int] = None,
        **kw,
    ):
        if data_directory:
            os.makedirs(data_directory, exist_ok=True)
        self.data_directory = data_directory
        if data_directory:
            self._io_handler = file_io.JobFileIoHandler(global_results=global_results)
        else:
            self._io_handler = tcp_io.JobTcpIoHandler(
                global_results=global_results, max_workers=max_workers
            )
        super().__init__(*args, **kw)

    def cleanup(self, wait: bool = True) -> None:
        """Cleanup in-memory artifacts but not on-disk artifacts (see `clean_all_job_artifacts`)"""
        self._io_handler.cleanup(wait=wait)
        super().cleanup(wait=wait)

    def clean_all_job_artifacts(self) -> None:
        """Cleanup on-disk artifacts"""
        for job_id in self._io_handler.get_job_ids():
            self.clean_job_artifacts(job_id)

    def clean_full(self, wait: bool = True) -> None:
        """Cleanup in-memory and on-disk artifacts"""
        ids = self._io_handler.get_job_ids()
        try:
            self.cleanup(wait=wait)
        finally:
            for job_id in ids:
                self.clean_job_artifacts(job_id)

    def spawn(
        self,
        func: Callable,
        args: Optional[Tuple] = None,
        kwargs: Optional[Mapping] = None,
        pre_script: Optional[str] = None,
        post_script: Optional[str] = None,
        job_name: Optional[str] = None,
        **kw,
    ) -> int:
        if not job_name:
            job_name = config.DEFAULT_JOB_NAME
        data = func, args, kwargs
        if self.data_directory:
            infile = f"{self.data_directory}/{job_name}.in.{str(uuid4())}.pkl"
            outfile = f"{self.data_directory}/{job_name}.out.%j.pkl"
            ctx = self._io_handler.start_job_io(data, infile, outfile)
            metadata = {"transfer": "file", "infile": infile, "outfile": outfile}
        else:
            ctx = self._io_handler.start_job_io(data)
            metadata = {"transfer": "tcp"}
        with ctx as (pyscript, environment, job_future):
            script = self._generate_script(
                pyscript, pre_script=pre_script, post_script=post_script
            )
            job_id = self.submit_script(
                script,
                environment=environment,
                metadata=metadata,
                job_name=job_name,
                **kw,
            )
            job_future.job_id = job_id
        return job_id

    def _generate_script(
        self,
        script: str,
        pre_script: Optional[str] = None,
        post_script: Optional[str] = None,
    ) -> str:
        if pre_script or post_script:
            if not pre_script:
                pre_script = ""
            if not post_script:
                post_script = ""
            return f"{pre_script}\n\npython3 <<EOF\n{script}EOF\n\n{post_script}"
        else:
            return f"#!/usr/bin/env python3\n{script}"

    def get_result(self, job_id: int) -> Any:
        return self._io_handler.get_job_result(job_id)

    def wait_done(self, job_id: int, *args, **kw) -> str:
        timeout = kw.get("timeout", None)
        t0 = time.time()
        status = super().wait_done(job_id, *args, **kw)
        if timeout is not None:
            timeout -= time.time() - t0
            timeout = max(timeout, 0)
        self._io_handler.wait_job_result(job_id, timeout=timeout)
        return status

    def cancel_job(self, job_id: int, request_options=None) -> None:
        super().cancel_job(job_id, request_options)
        self._io_handler.stop_job_io(job_id)

    def clean_job_artifacts(self, job_id: int, raise_on_error=False, **kw):
        metadata = self._get_metadata(job_id, **kw)
        if not metadata:
            return
        self._io_handler.cleanup_job_io(job_id)
        if metadata["transfer"] == "file":
            self._cleanup_job_io_artifact(job_id, metadata["infile"])
            self._cleanup_job_io_artifact(job_id, metadata["outfile"])
        super().clean_job_artifacts(job_id, raise_on_error=raise_on_error, **kw)

    def _get_metadata(self, job_id: int, **kw) -> Optional[dict]:
        properties = self.get_job_properties(job_id, **kw)
        if properties is None:
            return None
        metadata = properties.get("comment")
        if metadata is None:
            return None
        return json.loads(metadata)
