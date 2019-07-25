Contributing to Runium
======================

It is great you want to contribute! Let's make Runium great together! If you
wish to add new features or fix a bug, you will have to follow some procedures
and rules in order to get your changes accepted. This is to keep the code base
nice and clean.

********************
Contribution Process
********************

* Fork the project on Github

* Clone the fork to your local machine

* Make the changes to the project

* Run the test suite with tox (if you changed any code)

* Commit if you haven’t already

* Push the changes to your Github fork

* Make a pull request on Github

***************
Getting started
***************

First create a **Virtual Environment** with **Python 3.7** which is the default
version used in Runium.

.. code-block:: console

    $ python3.7 venv -m runium-env

Then clone Runium inside the Virtual Environment and start coding!

**********
Code style
**********

We use PEP 8 rules and flake8. Basically if you use flake8 you're good. This
applies to all text files (source code, tests, documentation). Just follow the
surrounding code style as closely as possible.

*******
Testing
*******

Running the test suite is done using the **tox**. This will test the code base
against all supported Python versions and performs some code quality checks
using flake8 as well.

Any nontrivial code changes must be accompanied with the appropriate tests.
The tests should not only maintain the coverage, but should test any new
functionality or bug fixes reasonably well. If you’re fixing a bug, first make
sure you have a test which fails against the unpatched codebase and succeeds
against the fixed version. Naturally, the test suite has to pass on every
Python version. If setting up all the required Python interpreters seems like
too much trouble, make sure that it at least passes on the lowest supported
version of both Python. The full test suite is always run against each pull
request, but it’s a good idea to run the tests locally first.

**************************
Building the documentation
**************************

You will find all the documentation files inside ``docs/source/``.
We use **ReStructuredText** (.rst) for the docs files and **Sphinx** to compile
them so if you want to contibute to the docs you'll have to install this as
well: ``pip install Sphinx``.

If you want to add a new file add it inside ``docs/source/`` then include it in
the toctree inside ``index.rst`` and build the decumentation locally to make
sure it works:

.. code-block:: console

    $ make clean
    $ makde html

The documentation you just build will be inside ``docs/build/``.
