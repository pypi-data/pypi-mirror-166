import gc
import pytest
from ..client.job_io import tcp_io
from ..client.errors import PendingResultError
from ..client.errors import CancelledResultError


def test_tcp_io():
    with tcp_io.JobTcpIoHandler() as handler:
        with handler.start_job_io({"question"}) as (script, env, future):
            future.job_id = 1234
        with pytest.raises(PendingResultError):
            handler.get_job_result(1234)
        assert tcp_io.job_test_client(env, {"response"}) == {"question"}
        handler.wait_job_result(1234, timeout=None)
        assert handler.get_job_result(1234) == {"response"}


def test_tcp_io_cancel():
    with tcp_io.JobTcpIoHandler() as handler:
        with handler.start_job_io({"question"}) as (script, env, future):
            future.job_id = 1
        handler.stop_job_io(1)
        handler.wait_job_result(1, timeout=None)
        with pytest.raises(CancelledResultError):
            handler.get_job_result(1)

        with handler.start_job_io({"question"}) as (script, env, future):
            future.job_id = 2
        handler.stop_job_io(2)
        assert tcp_io.job_test_client(env) == {"question"}
        handler.wait_job_result(2, timeout=None)
        with pytest.raises(CancelledResultError):
            handler.get_job_result(2)


def test_tcp_io_cleanup():
    with tcp_io.JobTcpIoHandler() as handler:
        with handler.start_job_io({"question"}) as (script, env, future):
            future.job_id = 1
        with pytest.raises(PendingResultError):
            handler.get_job_result(1)
        assert tcp_io.job_test_client(env, {"response"}) == {"question"}
        handler.wait_job_result(1, timeout=None)
        assert handler.get_job_result(1) == {"response"}

        with handler.start_job_io({"question"}) as (script, env, future):
            future.job_id = 2
        handler.stop_job_io(2)
        handler.wait_job_result(2, timeout=None)
        with pytest.raises(CancelledResultError):
            handler.get_job_result(2)

    while gc.collect():
        pass

    pytest.skip(reason="find out what keeps a reference")
    # assert not handler.get_job_ids()
