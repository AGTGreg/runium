The Runium object
==================

********
Runium()
********
``runium.core.Runium(mode='multithreading', max_workers=None, debug=True)``

In order to start using Runium, you must first import it from the core module
and Intitialize it.

Runium will start a new Thread or Process pool and will create an empty tasks
list.

**Parameters**
    - **mode** -- A string indicating wether the tasks should be run as Threads or Processes. It can be either ‘multithreading’ (Default) or ‘multiprocessing’.
    - **max_workers** --  An integer that indicates the max number of Threads or Processes to use. In Multithreading mode if max_workers is None or not given, it will default to the number of processors on the machine, multiplied by 5. In Multiprocessing mode it will default to the number of processors on the machine.
    - **debug** -- If True all the exceptions raised by the tasks will be printed in the console.


.. code-block:: python

    from runium.core import Runium

    rn = Runium()


********
new_task
********
``Runium.new_task(fn, kwargs={})``

Creates a new Task, and adds it to the tasks list. Returns a handy
``runium.core.Task`` object.

**Parameters**
    - **fn** -- The callable to be executed.
    - **kwargs** -- A dictionary that contains the arguments of the callable (if any).

**Example**

.. code-block:: python

    def send_email(to, msg):
        print("Sending", msg, "to", to)
        return True


    runium.new_task(
        send_email, kwargs={
            'to': 'mail.example.com',
            'msg': 'This is a test email.'
        })


*************
pending_tasks
*************
``Runium.pending_tasks()``

Returns a dictionary with all the pending tasks that looks like this: 

.. code-block:: python

    {
        task_id: task,
        task_id: task,
        …
    }
