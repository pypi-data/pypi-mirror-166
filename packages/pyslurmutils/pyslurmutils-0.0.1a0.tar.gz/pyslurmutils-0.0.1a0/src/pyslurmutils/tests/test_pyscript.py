from pyslurmutils.client.errors import NoResultError
import pytest


@pytest.mark.parametrize("pre_script", [None, "echo 'run pre script'"])
@pytest.mark.parametrize("post_script", [None, "echo 'run post script'"])
def test_python_script(pre_script, post_script, slurm_python_api):
    job_id = slurm_python_api.spawn(
        sum, args=([1, 1],), pre_script=pre_script, post_script=post_script
    )
    try:
        slurm_python_api.wait_done(job_id)
        slurm_python_api.print_stdout_stderr(job_id)
        assert slurm_python_api.get_result(job_id) == 2
        slurm_python_api.clean_job_artifacts(job_id)
        with pytest.raises(NoResultError):
            assert slurm_python_api.get_result(job_id) is None
    finally:
        slurm_python_api.clean_job_artifacts(job_id)


def test_failing_python_script(slurm_python_api):
    job_id = slurm_python_api.spawn(sum, args=([1, "abc"],))
    try:
        slurm_python_api.wait_done(job_id)
        slurm_python_api.print_stdout_stderr(job_id)
        with pytest.raises(TypeError):
            slurm_python_api.get_result(job_id)
    finally:
        slurm_python_api.clean_job_artifacts(job_id)
