from pyslurmutils.client.pyscript import SlurmPythonJobApi
from weakref import proxy


class Future:
    def __init__(self, job_id: int, pyapi: SlurmPythonJobApi) -> None:
        self.job_id = job_id
        self.pyapi = proxy(pyapi)

    def cancel(self):
        self.pyapi.cancel_job(self.job_id)

    def result(self, timeout=None):
        self.pyapi.wait_done(self.job_id, timeout=timeout)
        return self.pyapi.get_result(self.job_id)


class SlurmExecutor:
    def __init__(self, *args, api_object=None, **kw) -> None:
        if api_object is None:
            self.pyapi = SlurmPythonJobApi(*args, **kw)
        else:
            self.pyapi = api_object

    def submit(self, *args, **kwargs) -> Future:
        job_id = self.pyapi.spawn(*args, **kwargs)
        return Future(job_id, self.pyapi)

    def shutdown(self, wait=True):
        self.pyapi.clean_full(wait=wait)

    def __enter__(self):
        self.pyapi.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return self.pyapi.__exit__(exc_type, exc_val, exc_tb)
