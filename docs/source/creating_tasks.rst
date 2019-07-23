Creating tasks
==============

After initializing Runium, the first thing you want to do is create new tasks.
Creating a new task will not execute it but it will return a ``Task`` object
instead were you can attach callbacks and call its ``run()`` method to start
running the task.

********
new_task
********
``Runium.new_task(fn, kwargs={})``

Creates a new Task, and adds it to the tasks list. Returns a handy
``runium.core.Task`` object.

**Parameters**
    - **fn** -- The callable to be executed.
    - **kwargs** -- *(Optional)* A dictionary that contains the arguments of the callable (if any).


**Example:**

.. code-block:: python

    def simple_task():
        print("I'm working...")

    runium.new_task(simple_task)

**Here's what it looks like if your task has arguments:**

.. code-block:: python

    def send_email(to, msg):
        print("Sending", msg, "to", to)
        return True


    runium.new_task(
        send_email, kwargs={
            'to': 'mail.example.com',
            'msg': 'This is a test email.'
        })


.. note::

    You can add the optional argument ``runium`` in your function to get access
    to some of the statistics of that task inside that function. For example:

    .. code-block:: python

        def task(runium):
            print(runium['iterations_remaining'])

        runium.new_task(task).run(times=3)

    .. code-block:: console

        >> 3
        >> 2
        >> 1