# Day 2 - Terminal, OS & Developer Environment

## Topics Covered

- Linux Terminal Fundamentals
- File and Folder Operations
- Process and Port Management
- Environment Variables and PATH
- Package Managers (pip, npm)
- Git Fundamentals and Version Control

## Commands Practiced

### Navigation
- pwd (Displays the current working directory.)
- ls (Lists files and folders in the current directory.)
- ls -la (Lists all files (including hidden files) with detailed information.)
- cd 	(Moves into the specified directory.)
- cd ..	(Moves one directory up.)
- cd ~	(Moves to the user's home directory.)
- clear	(Clears the terminal screen.)

### File & Folder Operations
- mkdir (Creates a new directory.)
- touch (Creates a new empty file.)
- cp source destination (Copies a file or directory.)
- mv old new (Moves or renames a file or directory.)
- rm file.txt	(Deletes a file.)
- rm -rf 	(Deletes a directory recursively.)
- rm -rf folder (Forcefully deletes a directory and its contents)
- cat file.txt (Displays the contents of a file.)
- echo "text" (Prints text to the terminal.)
- echo "text" > file.txt	Writes text to a file (overwrites existing content).
- echo "text" >> file.txt	Appends text to the end of a file.


### Process & Port Management
- ps aux (Displays all running processes.)
- kill PID	(Stops a process using its Process ID.)
- kill -9 PID (	Forcefully terminates a process.)
- lsof -i :8000 (Shows which process is using port 8000.)

### Environment Variables
-----An environment variable is a named value stored by the operating system that programs can access.

- export NAME=value  (Creates an environment variable for the current terminal session.)
- echo $PATH 	(Displays the system PATH variable.)
- echo $NAME (Displays the value of an environment variable.)
Remove a Variable - unset Name

### Package Managers
- pip install (	Installs a Python package.)
- pip uninstall package	Removes a Python package.
- pip list ( Lists installed Python packages.)
- pip freeze	Displays installed packages with versions.
- npm init -y (	Creates a default package.json file.)
- npm install (	Installs a Node.js package.)
- npm -v	(Displays the installed npm version.)
- npm uninstall package	Removes a package.
- pip freeze > requirements.txt	Saves installed packages to requirements.txt.

### Git Commands
- git init ( Initializes a new Git repository.)
- git status (Shows the current repository status.)
- git add . ( Stages all changes for commit.)
- git commit -m "Initial commit" ( Saves staged changes with a commit message.)
- git log --oneline ( Displays a compact commit history.)
- git checkout -b master ( For creating new branch and switch in it)
- git switch "branch-name" / git checkout "branch-name" ( Switches to an existing branch.)
- git branch branch-name (Creates a new branch)
- git clone <repo-url> 
- git pull (Downloads and merges the latest changes from the remote repository.)
-git push	(Uploads local commits to the remote repository.)
git restore file.txt	(Discards changes made to a file.
)
-git diff (Shows the changes made before committing.)

## Outcome

- Learned to work with the Linux terminal.
- Practiced file and folder management.
- Understood process and port management.
- Learned environment variables.
- Practiced Python and Node package management.
- Learned Git basics and version control.