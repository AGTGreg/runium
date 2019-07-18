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
