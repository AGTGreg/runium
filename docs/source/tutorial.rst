Tutorial: Intro to Runium
=========================

In this tutorial we are going to make an app that sends emails. For the sake of
simplicity, not real emails.

Create a Virtual Environment for our new app, then install Runium:

.. code-block:: console

    $ python3.7 -m venv rn_tutorial_venv
    ...
    $ cd rn_tutorial_venv/
    $ source ./bin/activate
    (rn_tutorial_venv)$ pip install runium

Create a new directory inside our project and name it ``email_client``.
Inside it, create two empty files and name them ``__init__.py`` and ``app.py``:

| rn_tutorial_venv
| └── email_client
|     ├── __init__.py
|     └── app.py
| ...

Now we will create the method that sends emails. In the real world sending
emails takes time so we will make it sleep for a bit to simullate this lag.

**app.py**

.. code-block:: python

    import time


    def send_email():
        print("Sending email...")
        time.sleep(1)
        print("Email sent successfully.")
        return True


    def do_other_stuff():
        print("Doing other stuff...")


    if __name__ == "__main__":
        send_email()
        do_other_stuff()

Now go ahead and run your app form inside its directory:

.. code-block:: console

    $ python app.py
    Sending email...
    Email sent successfully.
    Doing other stuff...

Ok that looks good. Our app sends the email and then it does other stuff.

But do you see the problem here?

Let's try to run the send_email() method 3 times.

**app.py**

.. code-block:: python

    if __name__ == "__main__":
        send_email()
        send_email()
        send_email()
        do_other_stuff()

.. code-block:: console

    $ python app.py
    Sending email...
    Email sent successfully.
    Sending email...
    Email sent successfully.
    Sending email...
    Email sent successfully.
    Doing other stuff...

Our entire app now has to wait for all 3 emails to be sent before executing
any other code. Thats 3 seconds in our case. It may not look too bad now but
what if we need to send 100 emails?

Our app would freeze for 100 seconds before executing any other code because it
has to wait for all those emails to be sent.

This is where concurrency comes in to save the day! If we send those emails
concurrently aka asynchronously, our app won't have to wait before executing
any other code. With Runium this is easy!

Edit your app.py file to run send_email() with Runium.

**app.py**

.. code-block:: python
    :emphasize-lines: 2,17,18,19,20

    import time
    from runium.core import Runium


    def send_email():
        print("Sending email...")
        time.sleep(1)
        print("Email sent successfully.")
        return True


    def do_other_stuff():
        print("Doing other stuff...")


    if __name__ == "__main__":
        rn = Runium()
        rn.run(send_email)
        rn.run(send_email)
        rn.run(send_email)
        do_other_stuff()

And now check the results:

.. code-block:: console

    $ python app.py
    Doing other stuff...
    Sending email...
    Sending email...
    Sending email...
    Email sent successfully.
    Email sent successfully.
    Email sent successfully.

Now you see? Our app does not have to wait at all! It can send all those emails
in the background and do other stuff at the same time.
