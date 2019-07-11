import random
import time
from runium.core import Runium

some_data = 0


def add():
    time.sleep(0.5)
    global some_data
    print('Adding')
    some_data += 1
    return some_data


def a_callback(future):
    time.sleep(0.5)
    print('==> Callback called.')
    print('==> Exception:')
    print(future.exception())
    print('==> Result:')
    print(future.result())


def b_callback(future):
    print('==> b_callback initiated.')
    if future.exception():
        print('==> The task has failed.')
        print('==> Exception:')
        # print(future.result())
        print(future.exception())
    else:
        print('==> The task was successful.')
        print(future.result())


def task_time():
    print(time.time())
    time.sleep(0.5)


def task_args(msg, **kwargs):
    print('==>', msg, 'Running')
    time.sleep('1')
    print('==>', msg, 'Finished')
    return "task_args return msg: {}".format(msg)


def t_exep():
    raise Exception('This is a test exception.')


if __name__ == "__main__":
    rn = Runium()
    # r1 = rn.run_thread()
    # r1 = rn.run(task, mode='thread')
    # r1 = rn.run(task_args, kwargs={'msg': 'R1'}, callback=a_callback)
    # r2 = rn.run(task, kwargs={'msg': 'R2'})
    # r1 = rn.run(task_time, every='1 seconds', times=5).then(a_callback)

    r1 = rn.run(
        task_args, kwargs={'msg': 'R1'}, every='1 seconds', times=3,
        exit_on_exception=False
    )
    # r1.when_finished(b_callback)

    print(r1.result())
    print(r1.runs_count)
    # print(r1.thread)
    # print('==> Is running:', r1.running())
    # print(r1.result())
    # print('==> Is running:', r1.running())
