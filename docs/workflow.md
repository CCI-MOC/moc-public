# Development/branch management methodology
Please see http://scottchacon.com/2011/08/31/github-flow.html

# Code reviews
Per the above document, code reviews are done via github's "pull" mechanism. After the pull has been created, 2 people must then review it, with the second (after approving of the changes) completing the pull request.

For documentation changes, only one approval is required (or none if it's trivial).

# Branches
The MOC workflow is as follows:

1. Create a new local branch

	git branch -b NEWBRANCH

2. Do your commits
3. Push back to github, on a new remote branch with the same name.

	git push -u origin NEWBRANCH

   the `-u` sets up a correspondence between the local and remote
   branches; thereafter you can just type `git push`.

4. Go to github and submit a pull request to the devel branch for
   comments.

