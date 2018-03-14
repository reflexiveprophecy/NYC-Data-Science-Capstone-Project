# Git branch workflow and commands
In order to keep our git repo clean and organized, let’s use **branch** to organize our work. 
---
0. Prep work
  * In your local work directory, clone this git.
  `git clone https://github.com/reflexiveprophecy/NYC-Data-Science-Capstone-Project.git`
  * Check your current branch options and which branch you are on. 
  `git branch`
  You should see `*master` as the result.
1. Create a branch
  * `git checkout -b <branch name>`, here I use `git checkout -b testBranch`
  Now, do `git branch` again, you should see the both `master` and `testBranch`, with __**__ on the `testBranch`
2. Work with your branch
  * Work with your branch is the same as work with your `master` branch.
  * `add` and `commit` work just as before, you will update only your branch.
  * `push origin testBranch` will push your branch to our github repo. 
3. Update the `master` branch
  * You should only update the `master` branch when you have a function or section ready and tested.
  * You can update `master` in github project main page and click the `pull request`
  * For best practice, you should create a `branch` when develop a new function/section and delete that `branch` after `pull request`
4. Update Git branches from master
  * Sometimes, another team member may update the master branch when you are working on your branch. Here are two scenarios:
    - If the updated master version does not contain files you need, you can ignore the update.
    - If the updated master version contains some files you need, you need to update your branch from the master. You can click [here](https://stackoverflow.com/questions/3876977/update-git-branches-from-master) for a good reference how to perform the merge. 

