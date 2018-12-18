# On The Town: Social Planning As A Search Problem

**On The Town** is a web application that allows people in the same city, yet in different locations, to meet up in a location that is relatively equidistant from all of the people, and also satisfies users' preferences for type of activity, budget, and rating.

Given a set of users spread out in various locations and information on venues and activities in a desired destinations, OTT optimizes the process of meeting up with those that you care about. The problem of social planning here is well encoded as a search problem. OTT uses a variety of search algorithms (including depth-first search, breadth-first search, uniform cost search, greedy search, and A* search) to output a list of 7 places that not only satisfy users' preferences, but are also diverse in their offerings. Thus, OTT gives users a useful and varied set of options to execute.

The following is an example of the expected behavior: imagine 6 friends scattered around New York City: uptown, downtown, midtown, etc. Based on the factors they decide, both through polls and preferences within their user profiles, OTT minimizes the distance that each will have to travel in order to satisfy their desires, while also satisfying other preferences and the goal of diversity. Given all of the users’ preferences, OTT outputs 7 locations. Then, the friends meet up and have a fun time!

The core features of this application rely on the [Google Places API](https://developers.google.com/places/web-service/intro), and [search algorithms](https://en.wikipedia.org/wiki/Search_algorithm). The stack is as follows:

* Backend: Python, Flask, SQL
* Frontend: HTML, JavaScript, CSS, Jinja2

***

### Installation

OTT runs on [Python 2.7](https://www.python.org/download/releases/2.7/), and requires the following packages:
* flask
* flask-session
* requests
* werkzeug
* requests-cache
* redis

There are two ways to install these dependencies:
1. [Pipenv](https://pipenv.readthedocs.io/) [recommended]. Install Pipenv with `brew install Pipenv` if you're using Homebrew on MacOS or Linuxbrew on Linux, or `sudo dnf install pipenv` if you're using Fedora28. Otherwise, navigate [here](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) for more instructions. Next, navigate to the root directory of this repository and run `pipenv install` to install all dependencies at once and create a virtual environment for the project.
2. [pip](https://pip.pypa.io/en/stable/#). Download `pip` from with the following command in a Terminal window: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`. Next, run `python get-pip.py`. Finally, navigate to the root directory of this repository and run `pip install -r requirements.txt` to install all dependencies at once.

To initialize the database to store users' information:
1. Ensure that you have deleted `users.db` in the `server/` directory.
2. Run `db_init.py`
3. Run `redis-server`

Finally, to run the web application, run `python app.py` in a new Terminal window.

***

### Authors
**Hakeem Angulu**, Harvard College Class of 2020
[hangulu@college.harvard.edu](mailto:hangulu@college.harvard.edu)

**Louie Ayre**, Harvard College Class of 2020
[layre@college.harvard.edu](mailto:layre@college.harvard.edu)

**Amadou Camara**, Harvard College Class of 2020
[acamara@college.harvard.edu](mailto:acamara@college.harvard.edu)
