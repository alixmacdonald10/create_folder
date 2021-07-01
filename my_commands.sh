#!/usr/bin/env

source .env

cd $REPODIR

git config --global url."https://github.com/".insteadOf git@github.com:
git config --global url."https://".insteadOf git://
 
git init
git add .
git commit -m "Project created, initial commit"
git branch -M main
git remote add origin https://github.com/$USERNAME/$PROJECTNAME.git
git push -u origin main