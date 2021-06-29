import sys
import subprocess
import os
from dotenv import load_dotenv
from github import Github


load_dotenv()
# get data from a .env file thats in .gitignore (for privacy - this hides the personal access token and path)
path = os.getenv("FILEPATH")
# access to token generated from github
token = os.getenv("TOKEN")


def create_structure():
    # create local folders and files
    try:
        # create master folder
        global name
        name = str(input("What is the repo name?"))
        global repo_dir
        repo_dir = os.path.join(path, name)
        os.mkdir(repo_dir)
        
        # create subfolders
        # list of subfolders to create
        sub_folders = [
            'notes'
        ]
        for folder in sub_folders:
            sub_path = os.path.join(repo_dir, folder)
            os.mkdir(sub_path)
            
        # create blank files in top level
        os.chdir(repo_dir)
        file_list = [
            'README.md',
            '.gitignore',
            'main.py',
            'test.py',
            '.env'
        ]
        for file in file_list:
            f = open(file, 'x')
            f.close()
        
    except Exception as e:
        print('\nSome error occured while creating the directory\n')
        print(e.message, e.args)


def create_repo():
    # create github repository
    try:
        global user
        user = Github(token).get_user()
        repo = user.create_repo(name)
        print("Successfully created repository!")
    except Exception as e:
        print('\nSome error occured while creating the repo!\n')
        print(e.message, e.args) 


def push_repo():
    try:
        current_path = repo_dir
        os.chdir(current_path)   
        subprocess.Popen([
            'C://Program Files//Git//git-bash.exe',
            'git init',
            'git add .',
            'git commit -m "project created, initial commit"',
            'git branch -M main',
            f'git remote add origin https:///github.com//{user}//{name}.git',
            'git push origin main'
            ],
            shell=True, 
        )
        print('Succesfully pushed repository to github!')
         
    except Exception as e:
        print('\nSome error occured while pushing the code!\n')
        print(e.message, e.args) 
        

def open_vscode():
    subprocess.Popen(f"code -a {repo_dir}", shell=True)


if __name__ == "__main__":
  
    # create folder structure and repo
    create_structure()
    # create the github repo
    create_repo()
    push_repo()
    # open vscode
    open_vscode()