# ECE653 : Assignment 0

Where it is recommended to name <REPO-NAME> as 'upstream'
for consistency. The URL can be obtained from GitLab.
Then the upstream code for each assignment can be obtained through:

```shell
git fetch <REPO-NAME>
```

Or

```shell
git fetch <REPO-NAME> <BRANCH-NAME>
```

Which in this case is the following:

```shell
git pull upstream master
```

Which fetches the code. Then merge the code with your current branch:

```shell
git merge <BRANCH-NAME>
```

Which in this case is:

```shell
git merge upstream/master
```

Once you have made changes, and have added them with a command such
as the following:

```shell
git add <NAME-OF-FILE>
```

A 'commit' will need to be made. Note that a 'commit' contains the changes.

```shell
git commit -m "ENTER A COMMIT MESSAGE HERE. THIS IS FOR YOUR OWN REFERENCE"
```

Note that the message is optional. It is a message for your own clarity.
However, you may find it useful to include meaningful messages
in case you need to refer to previous, older commits.

```shell
git commit
```

Once there is commit ready, it can be pushed onto the GitLab
Repository through the following

```shell
git push origin master
```

*NOTE* It is ~STRONGLY~ recommended that you go to GitLab and check to
make sure your code is visible on GitLab after pushing.

Note that you can see all of the modified files with:

```shell
git status
```

If you wish to practice using git, you may try the ["Learn Git Branching"](https://learngitbranching.js.org/) on the [https://try.github.io/](https://try.github.io/) webpage.
