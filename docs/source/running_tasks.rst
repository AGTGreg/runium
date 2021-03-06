Running Tasks
=============

After you create a Task you have to call its ``run()`` method in order to start
running it. You can specify how often, how many times and when the task should
start running.

Here's how it works:

********
run()
********
``Task.run(every=None, times=None, start_in=0)``

Starts running the task. Returns a `Future`_ object.

**Parameters**
    - **every** -- *(Optional)* Run the task every n seconds. This value can be an integer or a float that indicates the number of seconds or a string that starts with an integer and finishes with the time scale.
    - **times** -- *(Optional)* How many times the task should run. It accepts an integer.
    - **start_in** -- *(Optional)* The amount of seconds to wait before start runing the task. It accepts the same values as :every.

.. note::

    In order to improve readability the ``every`` and ``start_in`` parameters
    can accept strings in this format:

    ``1 second`` ``2 seconds`` ``1 minute`` ``2 minutes`` ``1 hour`` ``2 hours``

**Example**

.. code-block:: python

    # Run a task once.
    async_task = runium.new_task(task).run()

    # Run a task multiple times.
    async_task = runium.new_task(task).run(times=3)

    # Run the task at once then repeat indefinitely every 1 hour.
    async_task = runium.new_task(task).run(every='1 hour')

    # Start the task in 5 hours.
    async_task = runium.new_task(task).run(start_in='5 hours')

Calling the ``run()`` method will give you a `Future`_ object so you may use
its methods:

.. code-block:: python

    # You can call result() to wait for it.
    async_task.result()

.. warning::

    Python's ``future.excetion()`` will allways return ``None`` because Runium
    catches all exceptions and passes them to ``future.result()``.


.. _Future: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future