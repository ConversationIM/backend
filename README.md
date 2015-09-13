# ConversationIM API

The back-end services supporting ConversationIM are stored here.

## Setup

We will be using Flask to develop our API. As such, we should configure a virtual environment.

#### Python Version

Full support for Python 3 is not ready for all libraries that we will be utilizing in this project. As such,
please be sure that you have a Python 2.x distribution installed on your system. Version 2.7.x is
preferred, and a version greater than 2.5.x is required. If you do not know how to check your Python version, you can simply type `python` from
the command line.

#### Virtualenv

From the command line, navigate to your projects directory or another directory that will contain your software projects. Then, type the following:

```
virtualenv -p [path_to_python_2.x] messenger
```

Be sure to replace `[path_to_python_2]` with the path to Python 2.x that you have installed. This is only necessary if you have multiple Python versions installed -- if you only have Python 2.x installed, you can omit the `-p` flag entirely. If you get an error at any time, check to make sure you have virtualenv on your PATH.

Change directory into your newly-created virtual environment. Then, clone the repository. You will probably want to clone with the following, so that you have an appropriately-named sub-directory:

```
git clone [path_to_repository] project
```

#### Activating and Deactivating the Virtual Environment

Whenever you are working with this project, you will need to change directory into the root of your virtual environment and run:

```
source bin/activate
```

Make sure that your virtual environment is activated before you continue and/or begin working. Once you are done, you can simply type `deactivate` to deactivate your virtual environment.

#### Dependencies

A file containing all required dependencies is contained in the `project` directory. To install these dependencies, simply run:

```
pip install -r requirements.txt
```

## Starting Up

With your virtualenv active, change directory so that you are in the `project` directory, and run the following:

```
python api.py
```

You'll find a server running on your loopback interface (localhost), using port 5000.
