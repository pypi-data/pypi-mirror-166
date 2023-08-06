from time import sleep


def test_pool(slurm_pool):
    future1 = slurm_pool.submit(sleep, args=(2,))
    future2 = slurm_pool.submit(sum, args=([1, 1],))
    assert future2.result() == 2
    assert future1.result() is None
