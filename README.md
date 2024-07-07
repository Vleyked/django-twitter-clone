# django-twitter-clone
This is a project built from scratch cloning formerly twitter basic functionality

# Quickstart
```bash
# 1. 
# Make sure you have the recommended python version
py --version # This works on Windows 
python --version # This works <sometimes> on Windows
python3.11 --version # This works in Linux based OS's like Mac and all Linux distros

# The ooutput from the previous command should be Python 3.11.X

# 2. 
# Starting a fresh virtual environemtns
py -m venv venv # Windows users
python3.11 -m venv venv # Linux/Mac Users



# 3. Installing the packages
pip install -r requirements

```

# You can clone this repo by
1. `cd ~`
2. `git clone https://github.com/Vleyked/django-twitter-clone.git`

# Useful git commands to navigate on this repo

```bash
# Switching to another branch
git switch <branch-name>
    git switch main
    git switch starting_point-exercise-templates

# Update the repository and its branches
git fetch

# Update one branch of the repo
git switch <that-branch> # This just switch to that branch
git pull origin <that-branch> # This updates a single branch
# Example
git switch end_point-exerise-templates
git pull origin end_point-exerise-templates

# Test your knowledge or practice

git switch <starting-point-branch>
git pull origin <start-point-branch> 

# Example
git switch starting_point-exercise-templates
git pull origin starting_point-exercise-templates
# Create a new branch called my_changes_exercise-templates
git checkout -b my-starting-point
... Do your changes in this repo to practice
# You will see the differences between the starting point and your work
git diff my_changes_exercise-templates end_point-exercise-templates
# You will see the differences between the starting point and the corrected work
git diff starting_point-exercise-templates end_point-exercise-templates
```
