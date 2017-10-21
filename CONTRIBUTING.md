# Contributing

Contributions to the project are welcome! Just open an [issue] or send a pull
request. After review/acceptance, the change will be incorporated as soon as
possible.

## Submitting a pull request

When submitting changes, you can use whatever workflow you're more comfortable
with.

### Using Github's web interface

The easiest way to submit a change is to just edit the page directly on the
Github interface. Check out the step-by-step instructions (with screenshots) on
[Github Help].

### Using the command line

Alternatively, you can do most of the process from the command line:

- [fork the repository] on the github web interface

- clone your fork locally:  
  `git clone https://github.com/{your_username}/SublimeJsPrettier.git 'JsPrettier' && cd JsPrettier`

- create a feature branch, e.g. named after the command you plan to edit:  
  `git checkout -b {branch_name}`

- make your changes (edit existing files or create a new one)

- commit the changes:  
  `git commit --all -m "{commit_message}"`

- push to your fork:  
  `git push origin {branch_name}`

- go to the github page for your fork, and click the green pull request button.

> **NOTE:** Please send only related changes in the same pull request. Typically
> a pull request will include changes in a single file.

### Commit message

For the commit message, please follow the
*[The seven rules of a great Git commit message]*.

[issue]: https://github.com/jonlabelle/SublimeJsPrettier/issues
[Github Help]: https://help.github.com/articles/editing-files-in-another-user-s-repository/
[The seven rules of a great Git commit message]: https://chris.beams.io/posts/git-commit/#seven-rules
[fork the repository]: https://github.com/jonlabelle/SublimeJsPrettier/fork
