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
