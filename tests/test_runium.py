import pytest
import time
from runium.core import Runium


@pytest.fixture(scope="module")
def rnt():
    return Runium()


@pytest.fixture(scope="module")
def rnp():
    return Runium(mode='multiprocessing')


def test_run_3_times(rnt, rnp):
    rt = rnt.run(runnium_param, times=3).result()
    rp = rnp.run(runnium_param, times=3).result()
    assert rt['iterations'] == 3
    assert rp['iterations'] == 3


def test_loop_drift(rnt, rnp):
    prev_time = time.time()
    rnt.run(simple_task, every=0.1, times=10).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 1
    assert time_elapsed > 0.88
    prev_time = time.time()
    rnp.run(simple_task, every=0.1, times=10).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 1
    assert time_elapsed > 0.88


def test_start_in(rnt, rnp):
    prev_time = time.time()
    rnt.run(simple_task, start_in=0.1).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.11
    assert time_elapsed > 0.09
    prev_time = time.time()
    rnp.run(simple_task, start_in=0.1).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.11
    assert time_elapsed > 0.09


def test_skipping_tasks(rnt, rnp):
    prev_time = time.time()
    rnt.run(sleepy_task, every=0.1, times=2).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.51
    assert time_elapsed > 0.2
    prev_time = time.time()
    rnp.run(sleepy_task, every=0.1, times=2).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.51
    assert time_elapsed > 0.2


def test_kwargs(rnt, rnp):
    rt = rnt.run(
        task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}
    ).result()
    rp = rnp.run(
        task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}

    ).result()
    assert rt == 'Spam, Spam, Spam, egg and Spam'
    assert rp == 'Spam, Spam, Spam, egg and Spam'


def test_return_exception(rnt, rnp):
    rt = rnt.run(task_with_exception)
    rp = rnp.run(task_with_exception)
    pytest.raises(ValueError, rt.result)
    pytest.raises(ValueError, rp.result)


def test_detect_exception(rnt, rnp):
    assert str(rnt.run(task_with_exception).exception()) == 'ni'
    assert str(rnp.run(task_with_exception).exception()) == 'ni'


def test_run_no_kwargs_bleeding(rnt, rnp):
    assert rnt.run(simple_task).result() is True
    assert rnp.run(simple_task).result() is True


# DUMMY TASKS =================================================================
def simple_task():
    return True


def task_with_kwargs(msg=None, **kwargs):
    return msg


def runnium_param(runium):
    return runium


def task_with_exception(runium):
    raise ValueError('ni')
    return runium


def sleepy_task():
    time.sleep(0.2)
    return True
