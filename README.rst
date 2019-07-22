Runium
======

Runium is a Python library that makes it easy to write non-blocking,
asynchronous tasks.

You can add new tasks as you please, choose when and how to execute them as
**Threads** or **Processes** and attach callbacks to be executed as soon as the
task is finished running. Run those tasks once or periodically or schedule to
run them at a specific time.

The purpose of Runium is to do these simple, easy and clean with minimum to
no changes to your code. Just one line of code is all it takes.

**Documentation** `https://runium.readthedocs.io/en/latest/main.html <https://runium.readthedocs.io/en/latest/main.html>`_

**Pypi:** `https://pypi.org/project/runium/ <https://pypi.org/project/runium/>`_

Features
========
* **Concurrency**: Run a task once or many times in its own Thread or Process.
* **Repetition**: Run tasks periodically on even time intervals. Optionally for a certain amount of times.
* **Scheduling**: Run tasks at a certain date and time.
* **Callbacks**: Runium tasks can accept callback functions which are executed when the task is finished running.
* **Simplicity and Readability**: Do all the above in a single line of code that is easy to read.


Installation
============

Runium is distributed on PyPI. The best way to install it is with pip:

.. code-block:: console

    $ pip install runium

Quickstart
==========

.. code-block:: python

    from runium.core import Runium

    # Initialize Runium
    rn = Runium()

    # Or you may want to run your tasks in Processes
    rn = Runium(mode='multiprocessing')

    # Create a task
    async_task = rn.new_task(task)
    
    # Attach callbacks (Check the documentation for callbacks)
    async_task.on_finished(callback)

    # or you can be more flexible...
    async_task.on_success(s_callback).on_error(e_callback)

    # Run it. This will return a future object.
    future = async_task.run()

    # Or if you want to run it multiple times
    future = async_task.run(times=3)

    # Or maybe run it 3 times every 1 hour
    future = async_task.run(every='1 hour', times=3)

    # Or tell Runium to start the task in a specific time
    future = async_task.run(start_in='5 hours')

    # Then you can wait for the result.
    future.result()

    # Of course you can do all these in one line :)
    rn.new_task(task).run(every='1 second', times=3).result()

Links
=====

**Github:** `https://github.com/AGTGreg/runium <https://github.com/AGTGreg/runium>`_

**Pypi:** `https://pypi.org/project/runium/ <https://pypi.org/project/runium/>`_
