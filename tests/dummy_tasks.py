import time


def simple_task():
    return True


def task_with_kwargs(msg=None, **kwargs):
    return msg


def runnium_param(runium):
    print(runium['iterations_remaining'])
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