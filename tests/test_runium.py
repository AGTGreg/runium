import pytest
import time
from .dummy_tasks import (
    simple_task, none_task, task_with_kwargs, runnium_param,
    task_with_exception, sleepy_task, task_callback_success,
    task_callback_error, success_callback,
    error_callback, se_callback
)
from runium.core import Runium


@pytest.fixture(scope="module")
def rnt():
    return Runium()


@pytest.fixture(scope="module")
def rnp():
    return Runium(mode='multiprocessing')


class TestTimes():
    def test_threading(self, rnt):
        rt = rnt.new_task(runnium_param).run(times=3).result()
        assert rt['iterations'] == 3

    def test_processing(self, rnp):
        rp = rnp.new_task(runnium_param).run(times=3).result()
        assert rp['iterations'] == 3


class TestRuniumParam():
    def test_threading(self, rnt):
        rt = rnt.new_task(runnium_param).run(times=3).result()
        assert rt['iterations_remaining'] == 0

    def test_processing(self, rnp):
        rp = rnp.new_task(runnium_param).run(times=3).result()
        assert rp['iterations_remaining'] == 0


class TestLoopDrift():
    def test_threading(selft, rnt):
        prev_time = time.time()
        rnt.new_task(simple_task).run(every=0.1, times=10).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 1) and (time_elapsed > 0.88)
        assert is_ok is True

    def test_processing(selft, rnp):
        prev_time = time.time()
        rnp.new_task(simple_task).run(every=0.1, times=10).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 1) and (time_elapsed > 0.88)
        assert is_ok is True


class TestStartIn():
    def test_threading(self, rnt):
        prev_time = time.time()
        rnt.new_task(simple_task).run(start_in=0.1).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 0.11) and (time_elapsed > 0.09)
        assert is_ok is True

    def test_processing(self, rnp):
        prev_time = time.time()
        rnp.new_task(simple_task).run(start_in=0.1).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 0.11) and (time_elapsed > 0.09)
        assert is_ok is True


class TestTaskSkipping():
    def test_threading(self, rnt):
        prev_time = time.time()
        rnt.new_task(sleepy_task).run(every=0.1, times=2).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 0.51) and (time_elapsed > 0.2)
        assert is_ok is True

    def test_processing(self, rnp):
        prev_time = time.time()
        rnp.new_task(sleepy_task).run(every=0.1, times=2).result()
        time_elapsed = time.time() - prev_time
        is_ok = (time_elapsed < 0.51) and (time_elapsed > 0.2)
        assert is_ok is True


class TestKwargs():
    def test_threading(self, rnt):
        r = rnt.new_task(
            task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}
        ).run().result()
        assert r == 'Spam, Spam, Spam, egg and Spam'

    def test_processing(self, rnp):
        r = rnp.new_task(
            task_with_kwargs, kwargs={'msg': 'Spam, Spam, Spam, egg and Spam'}
        ).run().result()
        assert r == 'Spam, Spam, Spam, egg and Spam'


class TestReturnException():
    def test_threading(self, rnt):
        r = rnt.new_task(task_with_exception).run().result()
        assert type(r).__name__ == 'ValueError'

    def test_processing(self, rnp):
        r = rnp.new_task(task_with_exception).run().result()
        assert type(r).__name__ == 'ValueError'


class TestKwargsBleeding():
    def test_threading(self, rnt):
        assert rnt.new_task(simple_task).run().result() is True

    def test_processing(self, rnp):
        assert rnp.new_task(simple_task).run().result() is True


class TestCallbacks(object):
    def test_on_finished_success_threading(self, rnt):
        assert rnt.new_task(task_callback_success).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_finished_success_processing(self, rnp):
        assert rnp.new_task(task_callback_success).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_finished_error_threading(self, rnt):
        assert rnt.new_task(task_callback_error).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_finished_error_processing(self, rnp):
        assert rnp.new_task(task_callback_error).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_finished_no_return_threading(self, rnt):
        assert rnt.new_task(none_task).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_finished_no_return_processing(self, rnp):
        assert rnp.new_task(none_task).on_finished(
            se_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_success_threading(self, rnt):
        assert rnt.new_task(task_callback_success).on_success(
            success_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_success_processing(self, rnp):
        assert rnp.new_task(task_callback_success).on_success(
            success_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_success_no_return_threading(self, rnt):
        assert rnt.new_task(none_task).on_success(
            success_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_success_no_return_processing(self, rnp):
        assert rnp.new_task(none_task).on_success(
            success_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_error_threading(self, rnt):
        assert rnt.new_task(task_callback_error).on_error(
            error_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_error_processing(self, rnp):
        assert rnp.new_task(task_callback_error).on_error(
            error_callback, updates_result=True
        ).run().result() == 'Error'

    def test_on_iter_success_threading(self, rnt):
        assert rnt.new_task(task_callback_success).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Success'

    def test_on_iter_success_processing(self, rnp):
        assert rnp.new_task(task_callback_success).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Success'

    def test_on_iter_error_threading(self, rnt):
        assert rnt.new_task(task_callback_error).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Error'

    def test_on_iter_error_processing(self, rnp):
        assert rnp.new_task(task_callback_error).on_iter(
            se_callback, updates_result=True
        ).run(times=3).result() == 'Error'

    def test_on_iter_no_return_threading(self, rnt):
        assert rnt.new_task(none_task).on_iter(
            se_callback, updates_result=True
        ).run().result() == 'Success'

    def test_on_iter_no_return_processing(self, rnp):
        assert rnp.new_task(none_task).on_iter(
            se_callback, updates_result=True
        ).run().result() == 'Success'


class TestTasksList(object):
    def test_count_threading(self, rnt):
        r1 = rnt.new_task(simple_task)
        tasks_prev_count = len(rnt.pending_tasks())
        r1.run().result()
        assert tasks_prev_count == 1

    def test_count_processing(self, rnp):
        r1 = rnp.new_task(simple_task)
        tasks_prev_count = len(rnp.pending_tasks())
        r1.run().result()
        assert tasks_prev_count == 1

    def test_count_finished_threading(self, rnt):
        rnt.new_task(simple_task).run().result()
        assert len(rnt.pending_tasks()) == 0

    def test_count_finished_processing(self, rnp):
        rnp.new_task(simple_task).run().result()
        assert len(rnp.pending_tasks()) == 0
