# Development/branch management methodology

Our workflow is based on [github flow][gf]. This document provides some
particulars, as well as a quick reference for some common operations.

# Code review

Per the above document, code review happens via github's "pull
request" mechanism. After the pull request has been created, 2 people
must then sign off on the change, with the second (after approving
of the changes) merging the pull request.

For documentation changes, only one signoff is required (or none if
the change is trivial).

# Branches
The MOC workflow is as follows:

1. Create a new local branch:

	git branch -b NEWBRANCH

2. Do your commits
3. Push back to github, on a new remote branch with the same name:

	git push -u origin NEWBRANCH

   the `-u` sets up a correspondence between the local and remote
   branches; thereafter you can just type `git push`.

4. Go to github and submit a pull request to the devel branch for
   comments.

[gf]: http://scottchacon.com/2011/08/31/github-flow.html
