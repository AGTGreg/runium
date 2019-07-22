Running Tasks
=============

********
run()
********
``Task.run(every=None, times=None, start_in=0)``

Starts running the task. Returns a ``future`` object.
(check the Python documentation of concurrent.futures)

**Parameters**
    - **every** -- Run the task every n seconds. This value can be an integer or a float that indicates the number of seconds or a string that starts with an integer and finishes with the time scale.
    - **times** -- How many times the task should run. It accepts an integer.
    - **start_in** -- The amount of seconds to wait before start runing the task. It accepts the same values as :every.

.. note::

    In order to improve readability the ``every`` and ``start_in`` parameters
    can accept strings in this format:

    ``1 second`` ``2 seconds`` ``1 minute`` ``2 minutes`` ``1 hour`` ``2 hours``

.. warning::

    Python's ``future.excetion()`` will allways return ``None`` because Runium
    catches all exceptions and passes them to ``future.result()``.

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

    # async_task returns a future object when run() is called. You can call
    # result() to wait for it.
    async_task.result()
