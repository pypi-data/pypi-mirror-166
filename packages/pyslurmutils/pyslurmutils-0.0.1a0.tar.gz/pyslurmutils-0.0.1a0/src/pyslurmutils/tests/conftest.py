import os
from typing import Iterator, Optional
import pytest
from ..client.base import SlurmBaseApi
from ..client.script import SlurmScriptApi
from ..client.pyscript import SlurmPythonJobApi
from ..client.job_io import file_io
from ..client.job_io import tcp_io
from ..futures import SlurmExecutor


@pytest.fixture(scope="session")
def slurm_file_dir(request):
    path = request.config.getoption("slurm_file_dir")
    if path and not os.path.isdir(path):
        pytest.skip(f"{path} is not mounted")
    return path


@pytest.fixture(scope="session")
def log_directory(slurm_file_dir) -> Optional[str]:
    if slurm_file_dir:
        user_name = os.environ.get("SLURM_USER", "wrong_user_name")
        return os.path.join(slurm_file_dir, user_name, "slurm_data")
    else:
        return None


@pytest.fixture(scope="session")
def data_directory(slurm_file_dir) -> Optional[str]:
    if slurm_file_dir:
        user_name = os.environ.get("SLURM_USER", "wrong_user_name")
        return os.path.join(slurm_file_dir, user_name, "slurm_data")
    else:
        return None


@pytest.fixture(scope="session")
def slurm_config(log_directory) -> dict:
    token = os.environ.get("SLURM_TOKEN", "").rstrip()
    user_name = os.environ.get("SLURM_USER", "").rstrip()
    if not token:
        pytest.skip("SLURM_TOKEN environment variable missing")
    if not user_name:
        pytest.skip("SLURM_USER environment variable missing")
    url = "http://slurm-api.esrf.fr:6820"
    return {
        "url": url,
        "token": token,
        "user_name": user_name,
        "log_directory": log_directory,
    }


@pytest.fixture
def slurm_base_api(slurm_config) -> Iterator[SlurmBaseApi]:
    with SlurmBaseApi(**slurm_config) as api:
        yield api


@pytest.fixture
def slurm_script_api(slurm_config) -> Iterator[SlurmScriptApi]:
    with SlurmScriptApi(**slurm_config) as api:
        yield api


@pytest.fixture
def slurm_python_api(slurm_config, data_directory) -> Iterator[SlurmPythonJobApi]:
    try:
        with SlurmPythonJobApi(data_directory=data_directory, **slurm_config) as api:
            yield api
    finally:
        assert len(tcp_io._RESULTS) == 0, "TCP cleanup not done properly"
        assert len(file_io._RESULTS) == 0, "File cleanup not done properly"


@pytest.fixture
def slurm_pool(slurm_python_api) -> Iterator[SlurmExecutor]:
    with SlurmExecutor(api_object=slurm_python_api) as pool:
        yield pool
