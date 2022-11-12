import argparse
import sys
import os
import shutil
from config import User, Colors as c
from git import Repo
from github import Github




# FILE CONFIGURATION
class conf():
    name = "FastRepo"
    version = "FastRepo 0.04 (https://github.com/javiergamezmendoza/FastRepo)"
    license = ""
    author = "Javier Gámez"
    author_email='javiergammen@gmail.com'




# PARSER
parser = argparse.ArgumentParser(description=conf.version,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-v", "--version", action="store_true", help="Shows project version")
subparsers = parser.add_subparsers(dest="command")

#NEW
parserNew = subparsers.add_parser("new", help="Add/Create repositories.")
parserNew.add_argument("-l", "--local", type=(str), dest="PATH", help="Creates a local git repository on the gived path.")
parserNew.add_argument("-r", "--remote", type=(str), dest="REPONAME", help="Create a GitHub repository with the given name.")
parserNew.add_argument("-p", "--private", type=(bool), dest="PRIVATE", default=False,  help="Set to 'True' if you want your Github Repo Private.")
parserNew.add_argument("-n", "--number", type=(int), dest="NUMBER",default=1, help="Set how many repositories create (REPONAME[NUMBER]).")
#SHOW
parserShow = subparsers.add_parser("show", help="Show existing repositories")
parserShow.add_argument("-r", "--remote", type=(str), dest="REPONAME", const="", nargs="?", help="Show the GitHub repositories of your account. ")
#REMOVE
parserRemove = subparsers.add_parser("remove", help="Remove existing repositories")
parserRemove.add_argument("-l", "--local", type=(str), dest="PATH", help="Remove a local git repository on the gived path.")
parserRemove.add_argument("-r", "--remote", type=(str), dest="REPONAME", help="Remove a GitHub repository with the given name (The name is not case sensitive). ")


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

#CREATE //MULTIPLE OR SINGLE// GITHUB REPO/S // NEW --REMOTE
def createRemoteRepos(repoName, repoNumber, private):
    for i in range(repoNumber):
        finalRepoName = repoName + str(i+1) if repoNumber > 1 else repoName
        if repoExist(finalRepoName):
            print(c.FAIL + "The repository "+ finalRepoName + " already exists." + c.ENDC)
        else:
            try:
                authed.create_repo( finalRepoName,
                                    description="An example of description",
                                    has_issues=False,
                                    has_projects=False,
                                    has_wiki=False,
                                    private=private
                                )
                print(c.OKGREEN + f"Repository {finalRepoName} created correctly." + c.ENDC)
            except: print(c.FAIL + "Something was wrong... Make sure of your config file and try again." + c.ENDC)

def deleteRemoteRepos(repoName):
        if repoExist(repoName):
            print(repoName)
            print(c.WARNING + f"This action will delete the {repoName} repository." + c.ENDC)
            if input("Are you sure? y/N: ") =="y":
                # try:
                    repo = authed.get_repo(repoName)
                    repo.delete()
                    print(c.OKGREEN + f"The repository {repoName} has been deleted."+ c.ENDC)
                # except:
                #     print("Something was wrong... Try again")
        else:
            print(c.FAIL + f"Repository {repoName} not found." + c.ENDC)



# CHECK IF REPO EXISTS IN GITHUB
def repoExist(repoName):
    try:
        authed.get_repo(repoName)
        return True
    except:
        return False

#SHOW
# SHOW ALL REPOS
def showRemoteRepos():
    for repo in authed.get_repos():
        print(c.OKGREEN + str(repo.name) + c.ENDC)

# SHOW ONE REPO DETAILS
def showRemoteRepo(repoName):
        try:
            repo = authed.get_repo(repoName)
            print("\n" + c.UNDERLINE + c.WARNING + repo.name + c.ENDC)
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
            print(c.UNDERLINE + c.WARNING + "FILES \n" + c.ENDC)
            for content in repo.get_contents(""):
                print (c.OKGREEN + str(content.path) + c.ENDC)
        except:
            print(c.FAIL + "Some error ocurred... Try again." + c.ENDC)



########## MAIN ############

# SHOWS HELP IF NO ARGUMENTS
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

github = Github(User.gitToken)
github.get_user(User.userName)
authed = github.get_user()

if args.version:
    print(version)
    sys.exit(1)
if args.command == "new":
    if args.PATH:
        path = args.PATH
        createLocalRepo(path)
    if args.REPONAME:
        repoName = args.REPONAME
        repoNumber = args.NUMBER
        private = args.PRIVATE
        createRemoteRepos(repoName, repoNumber, private)
elif args.command == "show":
    repoName = args.REPONAME
    if repoName == "":
        showRemoteRepos()
    elif hasattr(args, "REPONAME"):
        showRemoteRepo(repoName)
elif args.command == "remove":
    if args.PATH:
        gitPath = args.PATH
        print("This action will remove any repository on the given path.")
        if input("Are you sure? y/N").lower() == "y":
            shutil.rmtree(gitPath)
    if args.REPONAME:
        repoName = args.REPONAME
        deleteRemoteRepos(repoName)


