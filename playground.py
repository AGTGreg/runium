import random
import time
from runium.runium import Runium


def t_task(msg, **kwargs):
    sleep_for = round(random.uniform(0, 1), 2)
    sleep_for = 1
    print('==>', time.time(), msg, 'Running')
    time.sleep(sleep_for)
    print('==>', msg, 'Finished')
    return "==>{} returns.".format(msg)


def t_exep():
    raise Exception('This is a test exception.')


if __name__ == "__main__":
    rn = Runium()
    # r1 = rn.run(t_task, kwargs={'msg': 'r1'})
    # r2 = rn.run(t_task, kwargs={'msg': 'r2'}, every='1 second', times=3)
    # r3 = rn.run(t_task, kwargs={'msg': 'r3'}, start_in='5 seconds')

    # print('==> r1:', r1.get())
    # print('==> r2:', r2.get())
    # print('==> r3:', r3.get())

    re = rn.run(t_exep)
    t_exep.wait()
    print(t_exep.successful())
