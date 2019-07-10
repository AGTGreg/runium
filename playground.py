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


def t_task(msg, **kwargs):
    # sleep_for = round(random.uniform(0, 1), 2)
    sleep_for = 1
    print('==>', time.time(), msg, 'Running')
    time.sleep(sleep_for)
    print('==>', msg, 'Finished')
    return "==>{} returns.".format(msg)


def t_exep():
    raise Exception('This is a test exception.')


if __name__ == "__main__":
    rn = Runium()
    r1 = rn.run(t_task, kwargs={'msg': 'r1'}, every=1, times=2)
    # print(r1)
    r2 = rn.run(t_task, kwargs={'msg': 'r2'}, every='1 second', times=3)
    r3 = rn.run(t_task, kwargs={'msg': 'r3'})
    r4 = rn.run(add)

    # re = rn.run(t_exep, every='1 second', times=3)

    print('==> Runium tasks:')
    for ti, td in rn.tasks.items():
        print(ti, td)

    print(r1.result())
    # print('==> re:')
    # print(re.result())

    # print('==> Runium tasks:')
    # for ti, td in rn.tasks.items():
    #     print(ti, td)

    # print('==> r2:', r2)
    # print('==> r3:', r3)
    # print(t_exep.result())

    # print(some_data)
    # rn.run(add)
    # rn.run(add)
    # rn.run(add, every='1 second', times=5).result()
    # print(some_data)
