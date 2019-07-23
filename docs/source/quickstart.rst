Quickstart
==========

**A basic example:**

.. code-block:: python

    from runium.core import Runium

    # Initialize Runium
    rn = Runium()

    # Create a task
    async_task = rn.new_task(task)

    # Run it. This will return a future object.
    future = async_task.run()

    # Then you can wait for the result.
    future.result()

    # Of course you can do all these in one line :)
    rn.new_task(task).run().result()


**Callbacks:**

.. code-block:: python

    async_task.on_finished(callback).run()

    async_task.on_success(s_callback).on_error(e_callback).run()

    async_task.on_iter(callback).run()

**Choose how, when and how many times a task should run:**

.. code-block:: python

    # Run it multiple times...
    future = async_task.run(times=3)

    # ...every 1 hour
    future = async_task.run(every='1 hour', times=3)

    # Or tell Runium to start the task in a specific time
    future = async_task.run(start_in='5 hours')

    # All the methods above will return a future object. You can use result()
    # to wait for it.
    future.result()

    # Here it is in one line :)
    rn.new_task(task).run(every='1 second', times=3).result()
