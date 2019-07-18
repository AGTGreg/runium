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

So if you want to run a long-running method without blocking your code, instead
of doing this:

.. code-block:: python

  send_email()

...you can use Runium and run it asynchronously like this:

.. code-block:: python

  runium.run(send_email)

And now this method will run in the background without blocking your entire
app. It's that simple!

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

    rn = Runium()

    # Run task asynchronously
    rn.run(task)

    # Run task in 10 seconds from now.
    rn.run(task, start_in='10 seconds')

    # Run task every 10 seconds for 10 times
    rn.run(task, every='10 seconds', times=10)

    # Run task for 10 times, then run a callback function
    rn.run(task, times=10).then_run(callback)

Links
=====

**Github:** `https://github.com/AGTGreg/runium <https://github.com/AGTGreg/runium>`_

**Pypi:** `https://pypi.org/project/runium/ <https://pypi.org/project/runium/>`_
