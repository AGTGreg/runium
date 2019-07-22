Quickstart
==========


Install Runium using pip:

.. code-block:: console

    $ pip install runium


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
