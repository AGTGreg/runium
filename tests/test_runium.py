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
    rt = rnt.new_task(runnium_param).run(times=3).result()
    rp = rnp.new_task(runnium_param).run(times=3).result()
    assert rt['iterations'] == 3
    assert rp['iterations'] == 3


def test_loop_drift(rnt, rnp):
    prev_time = time.time()
    rnt.new_task(simple_task).run(every=0.1, times=10).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 1
    assert time_elapsed > 0.88
    prev_time = time.time()
    rnp.new_task(simple_task).run(every=0.1, times=10).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 1
    assert time_elapsed > 0.88


def test_start_in(rnt, rnp):
    prev_time = time.time()
    rnt.new_task(simple_task).run(start_in=0.1).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.11
    assert time_elapsed > 0.09
    prev_time = time.time()
    rnp.new_task(simple_task).run(start_in=0.1).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.11
    assert time_elapsed > 0.09


def test_skipping_tasks(rnt, rnp):
    prev_time = time.time()
    rnt.new_task(sleepy_task).run(every=0.1, times=2).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.51
    assert time_elapsed > 0.2
    prev_time = time.time()
    rnp.new_task(sleepy_task).run(every=0.1, times=2).result()
    time_elapsed = time.time() - prev_time
    assert time_elapsed < 0.51
    assert time_elapsed > 0.2


def test_kwargs(rnt, rnp):
    rt = rnt.new_task(
        task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}
    ).run().result()
    rp = rnp.new_task(
        task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}

    ).run().result()
    assert rt == 'Spam, Spam, Spam, egg and Spam'
    assert rp == 'Spam, Spam, Spam, egg and Spam'


def test_return_exception(rnt, rnp):
    rt = rnt.new_task(task_with_exception).run().result()
    rp = rnp.new_task(task_with_exception).run().result()
    assert type(rt).__name__ == 'ValueError'
    assert type(rp).__name__ == 'ValueError'


def test_run_no_kwargs_bleeding(rnt, rnp):
    assert rnt.new_task(simple_task).run().result() is True
    assert rnp.new_task(simple_task).run().result() is True


def test_on_finished_success_callback(rnt, rnp):
    assert rnt.new_task(task_callback_success).on_finished(
        se_callback, updates_result=True
    ).run().result() == 'Success'
    assert rnp.new_task(task_callback_success).on_finished(
        se_callback, updates_result=True
    ).run().result() == 'Success'


def test_on_finished_error_callback(rnt, rnp):
    assert rnt.new_task(task_callback_error).on_finished(
        se_callback, updates_result=True
    ).run().result() == 'Error'
    assert rnp.new_task(task_callback_error).on_finished(
        se_callback, updates_result=True
    ).run().result() == 'Error'


def test_success_callback(rnt, rnp):
    assert rnt.new_task(task_callback_success).on_success(
        success_callback, updates_result=True
    ).run().result() == 'Success'
    assert rnp.new_task(task_callback_success).on_success(
        success_callback, updates_result=True
    ).run().result() == 'Success'


def test_error_callback(rnt, rnp):
    assert rnt.new_task(task_callback_error).on_error(
        error_callback, updates_result=True
    ).run().result() == 'Error'
    assert rnp.new_task(task_callback_error).on_error(
        error_callback, updates_result=True
    ).run().result() == 'Error'


def test_iter_success_callback(rnt, rnp):
    assert rnt.new_task(task_callback_success).on_iter(
        se_callback, updates_result=True
    ).run(times=3).result() == 'Success'
    assert rnp.new_task(task_callback_success).on_iter(
        se_callback, updates_result=True
    ).run(times=3).result() == 'Success'


def test_iter_error_callback(rnt, rnp):
    assert rnt.new_task(task_callback_error).on_iter(
        se_callback, updates_result=True
    ).run(times=3).result() == 'Error'
    assert rnp.new_task(task_callback_error).on_iter(
        se_callback, updates_result=True
    ).run(times=3).result() == 'Error'


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


def task_callback_success():
    return 'Callback not fired.'


def task_callback_error():
    raise Exception('Callback not fired.')


def success_callback(success):
    if success:
        return 'Success'
    return None


def error_callback(error):
    if error:
        return 'Error'
    return None


def se_callback(success, error):
    if success:
        return 'Success'
    elif error:
        return 'Error'
    return None
