import atexit
import time
import uuid
import traceback
from inspect import signature
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from runium.util import get_seconds


class Runium(object):
    """
    Initialises the pool and tasks list.
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
        Creates a new Task, and adds it to the tasks list. Returns a Task
        object.
        """
        task_id = uuid.uuid4().int
        task = Task(task_id, fn, kwargs, self.__executor, self.debug)
        self.__tasks[task_id] = task
        return task

    def pending_tasks(self):
        return self.__clean_tasks_list()

    def __remove_task_from_tasks_list(self, task_id):
        try:
            del self.__tasks[task_id]
        except KeyError:
            pass

    def __clean_tasks_list(self):
        """
        Removes all finished tasks from the tasks list. Returns the cleaned
        tasks list.
        """
        tasks_to_remove = []
        for task_id, task in self.__tasks.items():
            if task.future is not None and task.future.done() is True:
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
        self.__callbacks = {
            'on_success': None,
            'on_error': None,
            'on_finished': None
        }
        self.__debug = debug
        self.future = None

    def on_success(
        self, fn=None, updates_result=False, stop=None, repeat=None
    ):
        self.__set_callback('on_success', fn, updates_result, stop, repeat)
        return self

    def on_error(self, fn=None, updates_result=False, stop=None, repeat=None):
        self.__set_callback('on_error', fn, updates_result, stop, repeat)
        return self

    def on_finished(self, fn=None, updates_result=False):
        self.__set_callback('on_finished', fn, updates_result)
        return self

    def __set_callback(
        self, callback_type, fn=None, updates_result=False, stop_task=None,
        repeat_task=None
    ):
        if fn is not None:
            self.__callbacks[callback_type] = {
                'fn': fn, 'updates_result': updates_result
            }
        elif stop_task is True:
            self.__callbacks[callback_type] = {
                'stop_task': True
            }
        elif repeat_task is not None:
            # times is mandatory, every is not
            times = repeat_task['times']
            try:
                every = repeat_task['every']
            except KeyError:
                every = None
            self.__callbacks[callback_type] = {
                'fn': _repeat_task(times, every),
                'updates_result': updates_result
            }
        else:
            raise ValueError('No callback parameters set.')

    def run(self, every=None, times=None, start_in=0):
        """
        Submits the task to the Pool.
        """
        every = get_seconds(every)
        start_in = get_seconds(start_in)
        every, times = self.__set_every_times_defaults(every, times)

        self.future = self.__executor.submit(
            _run_task,
            self.__fn, self.__id, every, times, start_in, self.__kwargs,
            self.__debug, self.__callbacks
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
    fn, id, interval, times, start_in, kwargs, debug, callbacks
):
    task_result = None
    task_success = None
    task_error = None
    iterations = 0

    if start_in > 0:
        time.sleep(start_in)

    next_time = time.time() + interval
    while True:
        iterations += 1

        # This is where the task is executed.
        task_result, task_success, task_error =\
            _get_results(fn, kwargs, iterations, times, debug)

        # Callbacks
        task_result = _run_callback(
            callbacks['on_success'], success=task_success, result=task_result)
        task_result = _run_callback(
            callbacks['on_error'], error=task_error, result=task_result)

        if times > 0 and iterations >= times:
            break

        # Skip tasks if we are behind schedule:
        if interval > 0:
            next_time +=\
                (time.time() - next_time) // interval * interval + interval
            time.sleep(max(0, next_time - time.time()))

    task_result = _run_callback(
        callbacks['on_finished'], success=task_success, error=task_error,
        result=task_result
    )

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
        if result is None:
            success = True
        else:
            success = result
    finally:
        return result, success, error


def _run_callback(callback, success=None, error=None, result=None):
    callback_result = None

    if callback is not None:
        fn = None
        try:
            fn = callback['fn']
        except KeyError:
            pass
        else:
            if fn is not None:
                if success is not None and error is not None:
                    callback_result = fn(success, error)
                elif error is not None:
                    callback_result = fn(error)
                elif success is not None:
                    callback_result = fn(success)

        try:
            if callback['updates_result'] is True:
                result = callback_result
        except KeyError:
            pass

    return result


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


def _stop_task():
    pass


def _repeat_task(times, every):
    pass
