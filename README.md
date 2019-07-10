# Runium
Clean and simple task concurrency, scheduling and repetition for Python.

Runium is a Python library that makes it easy for you to run as many tasks as you want concurrently, at scheduled times and periodically.

You can add new tasks as you please, choose when and how to execute them and control Runium within those tasks. 

The main purpose of Runium is to make all these as clean and simple as possible. For example:
```python 
# Run a task concurrently every 10 seconds.
runium.run(task, every='10 seconds')
```
Interested? Read on!

## Features
- **Concurrency**: Run a task once or many times in its own Thread or Process.
- **Repetition**: Run tasks periodically on even time intervals. Optionally for a certain amount of times.
- **Scheduling**: Run tasks chron-style. At a certain date and time.
- **Callbacks**:	Runium tasks can accept callback functions which are executed when the task is complete.
- **Conditional Repeat**: You can tell Runium to repeat a task based on it's outcome. ie: Repeat if task has failed.
- **Simplicity and Readability**: You can achieve all the above by writing one line of code that is easy to read.
