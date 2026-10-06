# Pocket Tasks: a Git practice repository

A tiny Python task board with a deliberately prepared Git history and working tree.
Requires Git and Python 3; there are no dependencies or remote repositories.

```sh
python3 taskboard.py
python3 taskboard.py list --open
python3 taskboard.py list --completed
python3 taskboard.py summary
```

Start with **[DEMO.md](DEMO.md)** for the step-by-step exercises.

The initial `main` branch has seven commits. `demo/base` marks the first commit,
and `demo/start` marks the last. Three unstaged changes in `taskboard.py` and an
untracked `scratch.txt` are intentional: they are the first exercise.

## Try the task board

`list --open` shows unfinished tasks; `list --completed` shows finished tasks.
`summary` reports total, completed, open, and high-priority counts.
Priorities are displayed as LOW, MEDIUM, and HIGH.
