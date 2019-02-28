# Python Demo Client
A fully working GUI Demo for the games on the aigaming.com platform.

## Getting Started with the Python Demo Client
If you're a seasoned python vet you can probably skip right over this introductory material. All you need to do is download the repository and start hacking!
If you're a little less confident, maybe give it a quick a skim, make sure you've got any additional packages downloaded, and then you should be good to go!
Finally, if you're a complete novice, fear not! This short guide should provide you with enough information to get up and running with the client!

### Setting up Python

#### Python
First, if you haven't already, you need to install python on your machine. Head over to https://www.python.org/downloads/ and download the latest version of Python 3 for your OS (as of writing, it's Python 3.6.3).

#### Pip
This should come with the latest version of python 3 in the link above but if not check out https://packaging.python.org/tutorials/installing-packages/ for instructions on how install pip. If you downloaded the latest version of python 3 using the link from the previous paragraph, you should already be good to go.

#### Packages
Now we have installed pip we can install the additional packages we require:

1. requests
2. pillow
3. tkinter (can't be installed via pip so it has been included in the download, or you can download separately from https://github.com/python/cpython/blob/3.6/Lib/tkinter/__init__.py)
For windows terminal: pip install package-name
For macOS and Linux terminal: pip3 install package-name

Staying on the same page the pip link took you to, you can scroll to the section 'Use pip for Installing' (or if you feel exceptionally lazy, follow this link https://packaging.python.org/tutorials/installing-packages/#use-pip-for-installing). This explains how to download packages from PyPI. The requests and pillow packages can be downloaded from here.

**Note:** we need to install the packages for Python 3, so make sure you use the command pip3 if you're on macOS or Linux.

We also require the json package. This should be installed by default on all platforms.

### Running the Client
This bit is really easy! Download the client from here, unzip the folder and then just pass the main.py file to the python interpreter!

For windows terminal:

python path-to-main.py
For macOS and Linux terminal:

python3 path-to-main.py

ADDING LOGIC

Coming up with the logic might not be easy, but adding it to your bot sure is! The only file you need to change is the appropriate _bot.py file. In there you should see the calculateMove() method. This is called by the client every time the server wants you to make a move. Start adding your own code here! We provide you with a random guessing bot to get you started. See our Quick Reference Guide for more details: https://www.aigaming.com/help.

### (Recommended) Setting up Your Development Environment
Now we have everything in place, all that is left is to set up our development environment. This really comes down to personal preference, some like to do all their coding in a lightweight text editor, and others like to use a fully featured IDE. A great IDE (that is also completely free) is PyCharm from JetBrains. Head over to https://www.jetbrains.com/pycharm and download the Community Edition of PyCharm which is the free version. The IDE is fairly easy to use, but be sure to check out https://www.jetbrains.com/help/pycharm/quick-start-guide.html for some introductory material to get you started.


### Command line parameters
usage: main.py [-h] [--botid BOTID] [--password PASSWORD]
                             [--gametype GAMETYPE] [--gamestyle GAMESTYLE]
                             [--timeout TIMEOUT] [--playanothergame]
                             [--dontplaysameuserbot] [--closeaftergame]

Set optional running parameters

optional arguments:

  -h, --help            show this help message and exit

  --botid BOTID         log in with this bot name

  --password PASSWORD   log in with this password

  --gametype GAMETYPE   play this gametype

  --gamestyle GAMESTYLE play this gamestyle

  --timeout TIMEOUT     have this timeout in milliseconds

  --playanothergame     Play another game when complete

  --dontplaysameuserbot Don't play another user in the same account

  --closeaftergame      Close the client once the game has completed (takes priority over playanothergame)

### Final Remarks
Hopefully now you're in place to get picking through the demo code. This should help you figure out how the API works, and ultimately starting work on your army of intelligent bots!
We look forward to seeing what you build!
