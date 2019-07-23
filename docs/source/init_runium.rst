Initialize Runium
=================

It all starts with the Runium object which lives in ``runium.core``. You will
use Runium to create new tasks and choose how to run them (as Threads or
Processes).

Runium also keeps a list of all the pending tasks.

********
Runium()
********
``runium.core.Runium(mode='multithreading', max_workers=None, debug=True)``

In order to start using Runium, you must first import it from the core module
and Intitialize it.

Runium will start a new Thread or Process pool and will create an empty tasks
list.

**Parameters**
    - **mode** -- *(Optional)* A string indicating wether the tasks should be run as Threads or Processes. It can be either ‘multithreading’ (Default) or ‘multiprocessing’.
    - **max_workers** --  *(Optional)* An integer that indicates the max number of Threads or Processes to use. In Multithreading mode if max_workers is None or not given, it will default to the number of processors on the machine, multiplied by 5. In Multiprocessing mode it will default to the number of processors on the machine.
    - **debug** -- *(Optional)* If True all the exceptions raised by the tasks will be printed in the console.

**Example:**

.. code-block:: python

    from runium.core import Runium

    # This will run tasks as seperate Threads.
    rn = Runium()
    # This will run tasks as seperate Processes.
    rn = Runium(mode='multiprocessing')


*************
pending_tasks
*************
``Runium.pending_tasks()``

Returns a dictionary with all the pending tasks that looks like this:

.. code-block::

    {
        task_id: task,
        task_id: task,
        …
    }
