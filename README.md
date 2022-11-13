# FastRepo
FastRepo is a python tool that allows create local and on cloud repositories in a few seconds.

## Requirements
You need to install Python, Pip and the requisites declared in requirements.txt

Install Python on [Python website](https://www.python.org/downloads/) for Windows or Mac and Linux.

On Ubuntu

```sh
$ sudo apt install python3
```

After that, you must install pip

On Windows and Mac, go to [this page](https://bootstrap.pypa.io/get-pip.py), copy the content of the page in a .py file, and execute it with the python3 command on a terminal.

On Ubuntu

```sh
$ sudo apt install python3-pip
```

Then, you can install the dependencies:

```sh
$ python3 -m venv env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
```

## Config

Edit the `config.py` and replace all the fields to your own data.

In `gitToken` field you must paste a GitHub token (classic) with repo and delete repo permissions. 
  
## Options

### New

`python3 fastrepo.py new [-l/--local local_path] [-r/--remote repo_name]`

It's allowed use `-l/--local` argument without `-r/--remote` argument and viceversa.

In remote repo creation, you can specify the number of repos with `-n/--number` argument

### Show

`python3 fastrepo.py show [-r/--remote repo_name]`

If don't add any repository name, it will show all the repositories of your account.

If you add a repository name, it will returns all the commits, branches and files information.

### Remove

`python3 fastrepo.py remove [-l/--local local_path] [-r/--remote repo_name(not case sensitive)]`

### Other arguments

`fastrepo -v/--version` to show Version

`fastrepo -h/--help` to show Help
