import argparse
import sys
import os
from config import User
from git import Repo
from github import Github

# FILE CONFIGURATION
version = "FastRepo 0.01 (https://github.com/javiergamezmendoza/FastRepo)"

# PARSER
parser = argparse.ArgumentParser(description=version,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-v", "--version", action="store_true", help="Shows project version")
subparsers = parser.add_subparsers(dest="command")

parserNew = subparsers.add_parser("new", help="Add/Create repositories.")
parserNew.add_argument("-l", "--local", type=(str), dest="PATH", help="Creates a local git repository on the gived path")
parserNew.add_argument("-r", "--remote", type=(str), dest="REPONAME", help="Create a GitHub repository with the given name ")
parserNew.add_argument("-p", "--private", type=(bool), dest="PRIVATE", default=False,  help="Set to true if you want your Github Repo Private. ")

parserShow = subparsers.add_parser("show", help="Show existing repositories") #TODO
parserRemove = subparsers.add_parser("remove", help="Remove existing repositories") #TODO

args = parser.parse_args()


# CREATE REPO // NEW --LOCAL
def createLocalRepo(path):
    with Repo.config_writer() as git_config:
            git_config.set_value('user', 'email', User.userMail)
            git_config.set_value('user', 'name', User.userName)
    if os.path.exists(path, "/.git"):
        print("There is a .git folder in that path...")
        restart = input("Do you want to restart the repository? Y/n")
        if restart:
            os.remove(path, "/.git")
    else:
        newRepo = Repo.init(path, "/.git")
    return

#CREATE GITHUB REPO // NEW --REMOTE
def createRemoteRepo(repoName, private):
    github = Github(User.gitToken)  
    user = github.get_user(User.userName)
    authed = github.get_user()
    print(private)
    authed.create_repo( repoName,
                        description="An example of description",
                        has_issues=False,
                        has_projects=False,
                        has_wiki=False,
                        private=private
                      )  
    

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

# MAIN

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