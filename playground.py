import random
import time
from runium.runium import Runium

some_data = 0


def add():
    time.sleep(0.5)
    global some_data
    print('Adding')
    some_data += 1
    return some_data


def a_callback(future_result):
    time.sleep(0.5)
    print('==> Callback called.')
    print('==> This is the result we have:', future_result.result())


def t_task(msg, **kwargs):
    # sleep_for = round(random.uniform(0, 1), 2)
    sleep_for = 1
    print('==>', time.time(), msg, 'Running')
    time.sleep(sleep_for)
    print('==>', msg, 'Finished')
    return "==> {} returns.".format(msg)


def t_exep():
    raise Exception('This is a test exception.')


if __name__ == "__main__":
    rn = Runium()
    r1 = rn.run(t_task, kwargs={'msg': 'R1'}, callback=a_callback)
    # r2 = rn.run(t_task, kwargs={'msg': 'R2'})
    print(r1)
    print(r1.thread)
    print('==> Is running:', r1.running())
    print(r1.result())
    print('==> Is running:', r1.running())