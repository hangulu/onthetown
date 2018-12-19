# On The Town: Social Planning As A Search Problem

**On The Town (OTT)** is a web application that allows people in the same city, yet in different locations, to meet up in a location that is relatively equidistant from all of the people, and also satisfies users' preferences for type of activity, budget, and rating.

Given a set of users spread out in various locations and information on venues and activities in a desired destinations, *OTT* optimizes the process of meeting up with those that you care about. The problem of social planning here is well encoded as a search problem. The developers of *OTT* chose from a variety of search algorithms (including depth-first search, breadth-first search, uniform cost search, greedy search, and A\* search) to output a list of 7 places that not only satisfy users' preferences, but are also diverse in their offerings. Thus, *OTT* gives users a useful and varied set of options to execute.

The production version of *OTT* found here utilizes Greedy Search. All algorithms can be found in `algorithms.py`.

The following is an example of the expected behavior: imagine 6 friends scattered around New York City: uptown, downtown, midtown, etc. Based on the factors they decide, both through polls and preferences within their user profiles, *OTT* minimizes the distance that each will have to travel in order to satisfy their desires, while also satisfying other preferences and the goal of diversity. Given all of the users’ preferences, *OTT* outputs 7 locations. Then, the friends meet up and have a fun time.

The core features of this application rely on the [Google Places API](https://developers.google.com/places/web-service/intro), and [search algorithms](https://en.wikipedia.org/wiki/Search_algorithm). The stack is as follows:

* Backend: Python, Flask, SQL
* Frontend: HTML, JavaScript, CSS, Jinja2

***

### Installation

*OTT* runs on [Python 2.7](https://www.python.org/download/releases/2.7/), and requires the following packages:
* flask
* flask-session
* requests
* werkzeug
* requests-cache
* redis
* numpy
* scipy
* matplotlib
* pandas
* plotly

There are two ways to install these dependencies:
1. [Pipenv](https://pipenv.readthedocs.io/) [recommended]. Install Pipenv with `brew install Pipenv` if you're using Homebrew on MacOS or Linuxbrew on Linux, or `sudo dnf install pipenv` if you're using Fedora28. Otherwise, navigate [here](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) for more instructions. Next, navigate to the root directory of this repository and run `pipenv install` to install all dependencies at once and create a virtual environment for the project.
2. [pip](https://pip.pypa.io/en/stable/#). Download `pip` from with the following command in a Terminal window: `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`. Next, run `python get-pip.py`. Finally, navigate to the root directory of this repository and run `pip install -r requirements.txt` to install all dependencies at once.

To initialize the database to store users' information:
1. Ensure that you have deleted `users.db` in the `server/` directory.
2. Run `db_init.py`
3. Run `redis-server`

To be able to use the [Google Places API](https://developers.google.com/places/web-service/intro) and thus *OTT*, you must create a file called `config.py` and place the following line in it:

`api_key = "[YOUR GOOGLE PLACES API KEY]"`

Replace `[YOUR GOOGLE PLACES API KEY]` with your Google Places API key, which can be found [here](https://developers.google.com/places/web-service/get-api-key). Ensure that the API key is put in quotation marks, and that the file is saved in the root directory of the repository.

Finally, to run the web application, run `python app.py` in a new Terminal window.

***

### Algorithm Testing

`testing.py` includes tests of all the *OTT* algorithms. This file allows one to check if the parties and users are being instantiated correctly, to investigate the process of that data structure creation, and test each of the algorithms individually. To run this file, type `python testing.py` into a Terminal window.

While `testing.py` tests the basic functionality of the application, a Jupyter notebook file was included to perform robust simulations. `evaluation.ipynb` performs many simulations of each algorithm on random parties. This file was  used to generate the data used in the **Results** section of the accompanying paper. The data generated can also be found in the file `simulation_results.csv`. While there is an aspect of randomness to the data generation process (parties of random properties are instantiated), the data analysis process can be replicated by running the \texttt{analysis.ipynb} file, which utilizes the data the developers generated.

As mentioned in the **Results** and **Discussion** sections, *BFS* takes a very long time to run, so there were time limits imposed on its evaluation. These time limits are fungible, and one may also opt to not test *BFS* by removing or commenting out the lines of code that respond to its evaluation. For an idea of how long these may take, the developers performed overnight trials to gather the included data.

***

### Authors
**Hakeem Angulu**, Harvard College Class of 2020
[hangulu@college.harvard.edu](mailto:hangulu@college.harvard.edu)

**Louie Ayre**, Harvard College Class of 2020
[layre@college.harvard.edu](mailto:layre@college.harvard.edu)

**Amadou Camara**, Harvard College Class of 2020
[acamara@college.harvard.edu](mailto:acamara@college.harvard.edu)
