# Development/branch management methodology
Please see http://scottchacon.com/2011/08/31/github-flow.html

# Code reviews
Per the above document, code reviews are done via github's "pull" mechanism. After the pull has been created, 2 people must then review it, with the second (after approving of the changes) completing the pull request.

For documentation changes, only one approval is required (or none if it's trivial).

# Branches
To complete the MOC workflow:

1. Create a new branch

	git branch -b NEWBRANCH

1. Do your commits
1. Push back to github

	git push -u origin NEWBRANCH

1. Go to github and submit a pull request to the devel branch for comments

