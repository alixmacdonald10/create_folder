import sys
import ctypes
from subprocess import Popen, PIPE, run
import os
import dotenv
from github import Github
import pygit2

# log current directory
creation_directory = os.getcwd()

# load in the dotenv file
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# get data from a .env file thats in .gitignore (for privacy - this hides the personal access token and path)
path = os.getenv("FILEPATH")
# access to token generated from github
token = os.getenv("TOKEN")
# access to github profile
username = os.getenv("USERNAME")


def mod_dotenv(key, new_value, file):
        os.environ[key] = new_value  # update local environment variable
        dotenv.set_key(file, key, os.environ[key])  # save to dotenv


def create_repo():
    # create github repository
    try:
        # set repo name
        global name
        name = str(input("What is the repo name?"))
        mod_dotenv('PROJECTNAME', name, dotenv_file)
        # create description
        global descrip
        descrip = str(input("What is the repo description?"))
        # return user creds from github
        global user
        user = Github(token).get_user()
        # create the repo in github
        global repo
        repo = user.create_repo(name, description=descrip)
        # location on local machine of repo
        global repo_dir
        repo_dir = os.path.join(path, name)
        mod_dotenv('REPODIR', repo_dir, dotenv_file)
        #Clone the newly created repo to local
        global repoClone
        repoClone = pygit2.clone_repository(repo.git_url, repo_dir)
        print("Successfully created repository!")
    except Exception as e:
        print('\nSome error occured while creating the repo!\n')
        print(e.message, e.args) 


def create_structure():
    # create local folders and files
    try:
        # navigate directory to new repo
        os.chdir(repo_dir)
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


def push_repo():
    try:
        # change current working directory to repo location on local
        #repo_dir = 'D:\\Scripts\\test'
        os.chdir(repo_dir)
        # run bash script to push repo
        sh_file = f'{os.path.join(creation_directory, "my_commands.sh")}'
        p1 = Popen(['C:\\Program Files\\Git\\git-bash.exe', sh_file], shell=True)
        p1.wait()
        print('Succesfully pushed repository to github!')
        
    except Exception as e:
        print('\nSome error occured while pushing the code!\n')
        print(e.message, e.args)
        

def open_vscode():
    p2 = Popen(f"code -a {repo_dir}", shell=True)
    p2.wait()
    print('Successfully opened VSCode!')


if __name__ == "__main__":

    # create the github repo
    create_repo()
    # create folder structure
    create_structure()
    # push repo to github
    push_repo()
    # open vscode
    open_vscode()
