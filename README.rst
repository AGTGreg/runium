# Runium
Clean and simple task concurrency, scheduling and repetition for Python.

Runium is a Python library that makes it easy to write non-blocking, asynchronous tasks which can be scheduled to run at a specific time and/or periodically.

You can add new tasks as you please, choose when and how to execute them as Threads or Processes and attach callbacks to be executed as soon as the task is finished running.

One of the key features of Runium is that it makes all these easy, clean and simple. For example:
```python 
# Run a task asynchronously for 5 times every 10 seconds.
runium.run(task, times=5, every='10 seconds')
# Run a task asynchronously and then run a callback function.
runium.run(task).then_run(some_callback)
```
Interested? Read on!

## Features
- **Concurrency**: Run a task once or many times in its own Thread or Process.
- **Repetition**: Run tasks periodically on even time intervals. Optionally for a certain amount of times.
- **Scheduling**: Run tasks at a certain date and time.
- **Callbacks**:	Runium tasks can accept callback functions which are executed when the task is finished running.
- **Simplicity and Readability**: You can achieve all the above by writing one line of code that is easy to read.