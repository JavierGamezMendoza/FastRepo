# FastRepo
FastRepo is a python tool that allows create local and on cloud repositories in a few seconds.

## Requirements
You need to install Python, Pip and the requisites declared in requirements.txt

Install Python on [Python website](https://www.python.org/downloads/) for Windows or Mac and Linux.

On Ubuntu --> `sudo apt install python` or `sudo apt install python3`

After that, you must install pip

On Windows and Mac, go to [this page](https://bootstrap.pypa.io/get-pip.py), copy the content of the page in a .py file, and execute it with the python or python3 command on a terminal.

On Ubuntu --> `sudo apt install python-pip` or `sudo apt install python3-pip`

Then, you can install the dependencies:

`pip install -r requirements.txt` or `pip3 install -r requirements.txt` 
  
## Options

### New

`python fastrepo.py new [-l local_path] [-r remote_repository_name]`

It's allowed use -l argument without -r argument and viceversa.

### Show

`python fastrepo.py show [-r optional_name]`

If don't add any repository name, it will show all the repositories of your account.

If you add a repository name, it will returns all the commits and branches information.

### Remove

Remove command it's on development, not usable yet.

### Other arguments

`fastrepo --version/-v` to show Version

`fastrepo --help/-h` to show Help
