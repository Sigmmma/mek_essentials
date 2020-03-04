# The runners

The runners here are .bat files because Windows hates really small EXE files
that execute commands.

Runners that use pythonw are ones that don't want the cmd window to show after
startup.
Ones that just use python do show the cmd window.

`%*` is used to pass on the calling args to the script we're executing.
This is to future proof for librarian and the likes.

We're using start so the cmd window can be released after execution.

msg is Window's messagebox command. It is useful because it is familiar to
people.
