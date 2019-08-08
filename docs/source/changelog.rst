Changelog
=========

*****
1.0.0
*****
* **Major change** -- ``on_iter`` callback is gone. Now the ``on_success`` and ``on_error`` callbacks run on every iteration.
* **BugFix** -- Set ``success`` for callbacks to ``True`` if the task callable executes successfully but returns ``None``.


********
>= 0.1.8
********
* **Feature** -- Basic functionality.
