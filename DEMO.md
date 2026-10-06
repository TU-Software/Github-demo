# Git demonstration

Run commands from this directory. Begin with the exercises in this order.
The repository has no remote, so every exercise stays local.

## 1. Inspect and stage individual hunks: `git add -p`

```sh
git status --short
git log --oneline --decorate --graph
git diff -- taskboard.py
git add -p taskboard.py
```

You should see three separate hunks:

1. Rename the heading to “Pocket Tasks — demo edition”.
2. Sort the task list by title instead of ID.
3. Add a tip to the summary output.

Answer `y`, `n`, `y` to stage the heading and summary tip, leaving the sorting
change unstaged. `?` shows the available interactive commands; `q` exits.

```sh
git diff --cached   # What the next commit would contain
git diff           # What remains outside the index
git status --short # MM taskboard.py, plus ?? scratch.txt
```

`scratch.txt` is untracked, so this `git add -p taskboard.py` does not include it.
Optional: `git add -N scratch.txt` makes its contents visible to `git add -p`.

Before continuing, unstage the exercise and stash all work, including untracked files:

```sh
git restore --staged .
git stash push -u -m "add-p demo changes"
git status --short # Should be empty
```

## 2. Clean up commit history: `git rebase -i`

```sh
git rebase -i demo/base
```

Git opens your configured editor with the following six commits, oldest first
(the actual hashes will differ):

```text
pick <hash> feat: display readable priority labels
pick <hash> fix: correct the high-priority label typo
pick <hash> feat: filter open and completed tasks
pick <hash> WIP: jot down an abandoned banner experiment
pick <hash> feat: show high-priority task count in summary
pick <hash> docs: add task board usage examples
```

Change the second `pick` to `fixup` to combine the typo fix with its feature.
Change the fourth `pick` to `drop` to remove the abandoned experiment. Save and exit.
`fixup` discards the fix commit's message; `squash` would let you edit a combined message.

If no editor is configured, use `git -c core.editor=nano rebase -i demo/base`
(or replace `nano` with an installed editor of your choice).

```sh
git log --oneline --decorate --graph
git diff demo/start main # Only notes/banner-experiment.md should be removed
python3 taskboard.py summary
```

The history now contains five commits including the base, with the same app behavior.
`git rebase --abort` cancels a rebase that is still in progress. `demo/start`
preserves the original history so you can compare or retry the exercise.

## 3. Recover a lost commit: `git reflog`

Keep the working tree clean for this exercise; leave the stash parked until afterward.
Create a disposable branch and a real empty commit, then move the branch back:

```sh
git switch -c demo/reflog
git commit --allow-empty -m "demo: a commit to recover with reflog"
git reset --soft HEAD~1
git log --oneline -3 # The new commit has disappeared from this branch's log
git reflog -5       # It is still recorded in the local reflog
```

Immediately after that reset, `HEAD@{1}` is the lost commit:

```sh
git branch recovered-work 'HEAD@{1}'
git show --stat recovered-work
git log --oneline --all --decorate --graph
git switch main
```

If you ran other commands that moved HEAD, find the commit's hash in
`git reflog` and use `git branch recovered-work <hash>` instead.
`reset --soft` moves the branch while preserving the index and working files.
Reflogs are local and eventually expire; they are not a substitute for a backup.

The earlier rebase also appears in the reflog. Explore `git reflog show main`
to see its old and new branch tips.

## Restore the patch exercise

```sh
git stash list
git stash apply 'stash@{0}'
git status --short
```

This restores the three changes and `scratch.txt` while keeping a backup in the stash.
The rebase exercise does not overlap those edits, so they should apply cleanly.

To repeat the rebase exercise, stash any working changes first, then create a
fresh branch from the preserved starting point:

```sh
git stash push -u -m "park changes before retry"
git switch -c practice-again demo/start
git rebase -i demo/base
```

Use a new branch name each time. The original tags stay available throughout.
