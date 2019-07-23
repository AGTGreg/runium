Callbacks
=========

A callback is a function that is attached to a ``runium.core.Task`` object and
gets executed as soon as the task finishes.

Callbacks are executed in the same Thread/Process as the Task that calls them.
As a result they are non-blocking.


***********
on_finished
***********
``Task.on_finished(fn, updates_result=False)``

Accepts a callable with the task's success and error results as its only
arguments.

If the task was successfull (no exceptions were raised) then the success
argument will contain the task's return and the error argument will be
``None``.

If the task is unsuccessfull (an exception was raised) then the error argument
will contain the exception object and success will be ``None``.

Runs the callback after the task has been executed successfully or after an
exception was raised.

**Parameters**
    - **fn** -- The callable to be executed with success and error as its only arguments.
    - **updates_result** -- *(Optional)* If this is True then the task's result will be replaced with whatever is returned by the callable.

**Example:**

.. code-block:: python

    def send_email():
        print("Sending email...")
        return "Email sent."


    # The callback must have the success and error arguments.
    def callback(success, error):
        if success:
            return True
        elif error:
            return "An error occurred."


    # Attach the callback like this
    async_task = runium.new_task(send_email).on_finished(callback).run()


    # You may also choose to get the result of the callback instead of the task
    # by setting the parameter updates_result to True.
    async_task = runium.new_task(send_email).on_finished(
        callback, updates_result=True).run()

    # This will return True
    async_task.result()




**********
on_success
**********
``Task.on_success(fn, updates_result=False)``

Accepts a callable with the task's result as its only argument.
Runs the callback after the task has been executed successfully and no
exceptions were raised.

**Parameters**
    - **fn** -- The callable to be executed with success as its only argument.
    - **updates_result** -- *(Optional)* If this is True then the task's result will be replaced with whatever is returned by the callable.

**Example:**

.. code-block:: python

    def send_email():
        print("Sending email...")
        return "Email sent."


    # The callback must have the success argument.
    def callback(success):
        return ("Success!")

    # Attach the callback like this
    async_task = runium.new_task(send_email).on_success(callback).run()

    # This callback is often used together with on_error callback:
    async_task = runium.new_task(
        send_email
    ).on_success(
        callback
    ).on_error(
        error_callback
    ).run()


********
on_error
********
``Task.on_error(fn, updates_result=False)``

Accepts a callable with the task’s exception object as its only argument. Runs
the callback after an exception was raised by the task.

**Parameters**
    - **fn** -- The callable to be executed with error as its only argument.
    - **updates_result** -- *(Optional)* If this is True then the task’s result will be replaced with whatever is returned by the callable.

**Example:**

.. code-block:: python

    def send_email():
        raise Exception("Email was not sent.)


    # The callback must have the error argument.
    def callback(error):
        resend_email()


    # Attach the callback like this
    async_task = runium.new_task(send_email).on_error(callback).run()

    # This callback is often used together with on_success callback:
    async_task = runium.new_task(
        send_email
    ).on_success(
        callback
    ).on_error(
        error_callback
    ).run()


*******
on_iter
*******
``Task.on_iter(fn, updates_result=False)``

Accepts a callable with the task's success and error results as its only
arguments.

If the task was successfull (no exceptions were raised) then the
success argument will contain the task's return and the error
argument will be ``None``.

If the task is unsuccessfull (an exception was raised) then the error
argument will contain the exception object and success will be ``None``.

Runs the callback after the task has been executed successfully or after an
exception was raised.

The difference between this type of callback and all the others is that
the other callbacks will run only once after the task has been executed
no matter how many times we've set it to run. But an on_iter callback
will run on every iteration if the task is to be executed many times.

**Parameters**
    - **fn** -- The callable to be executed with success and error as its only arguments: fn(success, error)
    - **updates_result** -- *(Optional)* If this is True then the task's result will be replaced with whatever is returned by the callable.

**Example:**

.. code-block:: python

    # The callback must have the success and error arguments.
    def callback(success, error):
        if success:
            print(success)
            return True
        elif error:
            print(error)
            return "An error occurred."

    # The callback will be executed 3 times.
    async_task = runium.new_task(send_email).on_iter(callback).run(times=3)


*****************
add_done_callback
*****************

This is not a Runium method but since ``Task.run()`` returns a `Future`_
object, you can also add callbacks using this method. But you have to call
``run()`` first before using this method.
Read the documentation about it here: `add_done_callback()`_

.. _Future: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future
.. _add_done_callback(): https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.add_done_callback