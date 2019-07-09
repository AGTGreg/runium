import random
import time
from runium.runium import Runium


def t_task(msg):
    # sleep_for = round(random.uniform(0, 1), 2)
    sleep_for = 1
    print('==>', time.time(), msg, 'Running')
    time.sleep(sleep_for)
    print('==>', msg, 'Finished')
    return "yo"


if __name__ == "__main__":
    rn = Runium()
    r1 = rn.run(t_task, kwargs={'msg': 'r1'})
    r2 = rn.run(t_task, kwargs={'msg': 'r2'})
    r3 = rn.run(t_task, kwargs={'msg': 'r3'})

    print('==> r1:')
    print(r1)
    print('==> r2:')
    print(r2)
    print('==> r3:')
    print(r3)
    time.sleep(2)
    print('==> r1:')
    print(r1)
    print('==> r2:')
    print(r2)
    print('==> r3:')
    print(r3)
