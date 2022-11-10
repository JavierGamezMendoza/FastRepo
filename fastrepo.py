import argparse
import sys
import os
import shutil
from config import User, Colors as c
from git import Repo
from github import Github

# FILE CONFIGURATION
version = "FastRepo 0.01 (https://github.com/javiergamezmendoza/FastRepo)"

# PARSER
parser = argparse.ArgumentParser(description=version,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-v", "--version", action="store_true", help="Shows project version")
subparsers = parser.add_subparsers(dest="command")

#NEW
parserNew = subparsers.add_parser("new", help="Add/Create repositories.")
parserNew.add_argument("-l", "--local", type=(str), dest="PATH", help="Creates a local git repository on the gived path")
parserNew.add_argument("-r", "--remote", type=(str), dest="REPONAME", help="Create a GitHub repository with the given name ")
parserNew.add_argument("-p", "--private", type=(bool), dest="PRIVATE", default=False,  help="Set to true if you want your Github Repo Private. ")
#SHOW
parserShow = subparsers.add_parser("show", help="Show existing repositories") #TODO
parserShow.add_argument("-r", "--remote", type=(str), dest="REPONAME", const="", nargs="?", help="Show the GitHub repositories of your account. ")
#REMOVE
parserRemove = subparsers.add_parser("remove", help="Remove existing repositories") #TODO

args = parser.parse_args()


# CREATE REPO // NEW --LOCAL
def createLocalRepo(path):
    gitPath = path + "/.git"
    if os.path.exists(gitPath):
        print(c.WARNING + "There is a .git folder in that path...")
        restart = input("Do you want to restart the repository? y/n: " + c.ENDC).lower()
        if restart == "y":
            shutil.rmtree(gitPath)
            repo = Repo.init(path)
            print("Repository has been deleted...")
            print(c.OKGREEN + "New repository created." + c.ENDC)
        else:
            print("Directory NOT deleted")
            repo = Repo(gitPath)
    else:
        Repo.init(gitPath)
    
    with repo.config_writer() as git_config:
            git_config.set_value('user', 'email', User.userMail)
            git_config.set_value('user', 'name', User.userName)
    return

#CREATE GITHUB REPO // NEW --REMOTE
def createRemoteRepo(repoName, private):
    try:
        github = Github(User.gitToken)  
        github.get_user(User.userName)
        authed = github.get_user()
        authed.create_repo( repoName,
                            description="An example of description",
                            has_issues=False,
                            has_projects=False,
                            has_wiki=False,
                            private=private
                        )  
        print(c.OKGREEN + "Repositorio created correctly." + c.ENDC)
    except: print(c.FAIL + "Something was wrong... Make sure of your config file and try again." + c.ENDC)

#SHOW  
def showRemoteRepo(repoName):
    github = Github(User.gitToken) 
    authed = github.get_user()
    if repoName == "":
        for repo in authed.get_repos():
            print(repo.name)
    else:
        try:
            repo = authed.get_repo(repoName)
            print(repo.name)
            print("--------------------------")
            print(c.UNDERLINE + c.WARNING + "COMMITS \n" + c.ENDC)
            for commit in repo.get_commits():
                print(c.OKGREEN + str(commit) + c.ENDC)
                print(commit.commit.author.date)
                print("--------------------------")
            print(c.UNDERLINE + c.WARNING + "BRANCHES \n" + c.ENDC)
            for branch in repo.get_branches():
                print (c.OKGREEN + str(branch) + c.ENDC)
                print (branch.commit)
                print("--------------------------")
        except:
            print(c.FAIL + "Some error ocurred... Try again." + c.ENDC)



########## MAIN ############

# SHOWS HELP IF NO ARGUMENTS
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)
if args.version:
    print(version)
if args.command == "new":
    if args.PATH:
        path = args.PATH
        createLocalRepo(path)
    if args.REPONAME:
        repoName = args.REPONAME
        print(repoName)
        private = args.PRIVATE
        createRemoteRepo(repoName, private)
elif args.command == "show":
    repoName = args.REPONAME
    if hasattr(args, "REPONAME"):
        showRemoteRepo(repoName)