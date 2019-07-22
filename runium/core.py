import atexit
import time
import uuid
import traceback
from inspect import signature
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from runium.util import get_seconds
from runium.constants import UPDATES_RESULT, FN


class Runium(object):
    """
    Initialises the pool and tasks list.
    Returns a Task object.
    """
    def __init__(self, mode='multithreading', max_workers=None, debug=True):
        self.__mode = mode
        self.__max_workers = max_workers
        self.debug = debug
        self.__tasks = {}
        if self.__mode == 'multiprocessing':
            self.__executor = ProcessPoolExecutor(
                max_workers=self.__max_workers)
        elif self.__mode == "multithreading":
            self.__executor = ThreadPoolExecutor(
                max_workers=self.__max_workers)
        else:
            raise ValueError(
                'Mode can only be multiprocessing or multithreading.'
            )
        atexit.register(self.__executor.shutdown)

    def new_task(self, fn, kwargs={}):
        """
        Creates a new Task, and adds it to the tasks list.
        Returns a Task object.
        """
        task_id = uuid.uuid4().int
        task = Task(task_id, fn, kwargs, self.__executor, self.debug)
        self.__tasks[task_id] = task
        return task

    def pending_tasks(self):
        """
        Returns a dictionary with all the pending tasks.
        """
        return self.__clean_tasks_list()

    def __remove_task_from_tasks_list(self, task_id):
        try:
            del self.__tasks[task_id]
        except KeyError:
            pass

    def __clean_tasks_list(self):
        """
        Removes all finished tasks from the tasks list.
        Returns the cleaned tasks list.
        """
        tasks_to_remove = []
        for task_id, task in self.__tasks.items():
            if task.future is not None:
                if task.future.done() is True:
                    tasks_to_remove.append(task_id)
        for t_id in tasks_to_remove:
            self.__remove_task_from_tasks_list(t_id)
        return self.__tasks


class Task(object):
    """
    This is the object that is returned when we use Runium.new_task(...).
    """
    def __init__(self, task_id, fn, kwargs, executor, debug):
        self.__id = task_id
        self.__fn = fn
        self.__kwargs = kwargs
        self.__executor = executor
        self.__on_success_callback = None
        self.__on_error_callback = None
        self.__on_iter_callback = None
        self.__on_finished_callback = None
        self.__debug = debug
        self.future = None

    def on_success(self, fn, updates_result=False):
        '''
        Accepts a callable with the task's result as its only argument.
        Runs the callback after the task has been executed successfully and no
        exceptions were raised.
        '''
        self.__on_success_callback = (fn, updates_result)
        return self

    def on_error(self, fn, updates_result=False):
        '''
        Accepts a callable with the task's exception object as its only
        argument.
        Runs the callback after an exception was raised by the task.
        '''
        self.__on_error_callback = (fn, updates_result)
        return self

    def on_iter(self, fn, updates_result=False):
        '''
        Accepts a callable with the task's success and error results as its
        only arguments.
        '''
        self.__on_iter_callback = (fn, updates_result)
        return self

    def on_finished(self, fn, updates_result=False):
        '''
        Accepts a callable with the task's success and error results as its
        only arguments.
        '''
        self.__on_finished_callback = (fn, updates_result)
        return self

    def run(self, every=None, times=None, start_in=0):
        """
        Start running the task. Returns a future object.
        """
        every = get_seconds(every)
        start_in = get_seconds(start_in)
        every, times = self.__set_every_times_defaults(every, times)

        self.future = self.__executor.submit(
            _run_task,
            self.__fn, self.__id, every, times, start_in, self.__kwargs,
            self.__debug,
            self.__on_success_callback, self.__on_error_callback,
            self.__on_iter_callback, self.__on_finished_callback
        )

        return self.future

    def __set_every_times_defaults(self, every, times):
        """
        Sets the :every and :times properties to sensible defaults if one or
        any of them are not set.
        Sets defaults so that Runium will:
            Run the task one time if the :times and :every are not set.
            Loop indefinitely if :every is set and :times is not set.
        """
        if every is None and times is None:
            times = 1
            every = 0
        elif every is not None and times is None:
            times = 0
        elif every is None and times is not None:
            every = 0
        return every, times


def _run_task(
    fn, id, interval, times, start_in, kwargs, debug,
    on_success, on_error, on_iter, on_finished
):
    callback_result = None
    task_result = None
    task_success = None
    task_error = None
    iterations = 0

    if start_in > 0:
        time.sleep(start_in)

    next_time = time.time() + interval
    while True:
        iterations += 1
        callback_result = None

        # This is where the task is executed.
        task_result, task_success, task_error =\
            _get_results(fn, kwargs, iterations, times, debug)

        if on_iter is not None:
            callback_result = on_iter[FN](task_success, task_error)
            if on_iter[UPDATES_RESULT] is True:
                task_result = callback_result

        if times > 0 and iterations >= times:
            break

        # Skip tasks if we are behind schedule:
        if interval > 0:
            next_time +=\
                (time.time() - next_time) // interval * interval + interval
            time.sleep(max(0, next_time - time.time()))

    # Run callbacks
    if task_success is not None and on_success is not None:
        callback_result = on_success[FN](task_success)
        if on_success[UPDATES_RESULT] is True:
            task_result = callback_result
    if task_error is not None and on_error is not None:
        callback_result = on_error[FN](task_error)
        if on_error[UPDATES_RESULT] is True:
            task_result = callback_result
    if on_finished is not None:
        callback_result = on_finished[FN](task_success, task_error)
        if on_finished[UPDATES_RESULT] is True:
            task_result = callback_result

    return task_result


def _get_results(fn, kwargs, iterations, times, debug):
    """
    Runs the task and catches any exceptions that might occur. Passes the
    runium parameter if the task accepts one.
    Returns:
        success: The return of the task or None if an Exception has occurred.
        error: The Exception object or None if no Exception occurred.
        result: Either the return of the task or an Exception object.
    """
    result = None
    success = None
    error = None
    try:
        if 'runium' in signature(fn).parameters.keys():
            runium_param = _make_runium_param(iterations, times)
            result = fn(runium=runium_param, **kwargs)
        else:
            result = fn(**kwargs)
    except Exception as err:
        if debug is True:
            traceback.print_exc()
        error = err
        result = err
    else:
        success = result
    finally:
        return result, success, error


def _make_runium_param(iterations, times):
    """
    Creates and returns a dict with runium specific stats and functions that
    can be accessed from within the task.
    """
    context = {
        'iterations': iterations,
        'iterations_remaining': times - iterations
    }
    return context
