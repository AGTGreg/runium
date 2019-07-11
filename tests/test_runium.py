import pytest
from runium.core import Runium


@pytest.fixture
def trn():
    rn = Runium()
    return rn


# Dummy tasks =================================================================
def simple_task():
    return True


def task_with_kwargs(msg=None, **kwargs):
    return msg


def task_with_exception():
    raise ValueError('ni')


def add_one(val=0):
    print('Adding to', val)
    val += 1
    return val


# TESTS =======================================================================
def test_thread_return_kwargs(trn):
    assert trn.run(task_with_kwargs, kwargs={'msg': 'spam'}).result() == 'spam'


def test_thread_return_exception(trn):
    task = trn.run(task_with_exception)
    pytest.raises(ValueError, task.result)


def test_thread_detect_exception(trn):
    task = trn.run(task_with_exception)
    ex = task.exception()
    assert ex, 'ni'


def test_thread_run_3_times(trn):
    task = trn.run(simple_task, times=3)
    task.result()
    assert task.runs_count == 3


def test_thread_exit_on_exception(trn):
    task = trn.run(task_with_exception, times=3, exit_on_exception=True)
    try:
        task.result()
    except ValueError:
        pass
    assert task.runs_count == 1


def test_thread_dont_exit_on_exception(trn):
    task = trn.run(task_with_exception, times=3, exit_on_exception=False)
    try:
        task.result()
    except ValueError:
        pass
    assert task.runs_count == 3
