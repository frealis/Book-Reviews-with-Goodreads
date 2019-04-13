# Web Programming with Python and JavaScript - Project 1

# Overview
- The website is powered by Flask, styled with Boostrap 4, and uses a Heroku Postgres database. It allows visitors to search for 5000 books stored in its database, read and write reviews for those books, view ratings on the same books from a site called "Goodreads" (https://www.goodreads.com/), and retrieve book reviews and details through an API.

- https://docs.cs50.net/web/2018/x/projects/1/project1.html

# Setup & Configuration
- Flask needs to know which file is used to start the server/run the application, and additionally the database URL and Goodreads API key need to be set. These can be set using environment variables. Using Powershell you can set environment variables manually from the command line:

  $ $env:DATABASE_URL = "database URL"
  $ $env:FLASK_APP = "application.py"
  $ $env:GOODREADS_API_KEY = "goodsreads api key"

  ... or you can store the variables in a .env file within the root directory and retrieve them via dotenv: https://pypi.org/project/python-dotenv/#installation

  ... in Powershell you can see which environment variables have currently been set by typing:

    $ Get-ChildItem Env:

- Enable development/debugging features w/traceback:

  $ $env:FLASK_ENV = "development"  // debugger + automatic reloader
  $ $env:FLASK_DEBUG = "1"          // debugger

  ... make sure to disable these in production mode.

- Start the Flask server:

  $ flask run

- Connect to the Heroku Postgres database from the command line (credentials are at Dashboard > cs50-book-review-w-goodreads > Heroku Postgres > Settings > Database Credentials/View Credentials) with either command:

  $ psql database_URL

  -or-

  $ heroku pg:psql <database-name> --app cs50-book-review-w-goodreads

# Login

- Creating a Login Page: https://www.youtube.com/watch?v=eBwhBrNbrNI

- Login & Sessions:

  1. The time between when a client logs on and logs off is called a "session", and Flask uses a "session object" to store information about a client during this time. So in Flask, a "session" is basically both a length of time and an object.

  2. When a client reigsters for a new account or signs in with an existing account, their username and user ID are stored in a "session object". A "session object" is basically a dictionary of key:value pairs used to represent an active session. Flask places the session object in a cookie and uses a "secret key" to encrypt it. When creating an instance of a Flask application within app.py/application.py (or whatever the name of the controller file is) its secret key can be set like this:

    > app = Flask(__name__)
    > app.secret_key = <secret key goes here>

    ... to generate a random key from the command line:

    $ python -c 'import os; print(os.urandom(16))'

  3. Flask has a special function called before_request() that runs before each request, including GET and POST requests. This web application uses it to assign session['user'] and session['id'] to g.user and g.id, respectively. The 'g' variable is a special Flask variable that persists between client requests, so it essentially acts like a global variable. The web application uses it to represent a client's active session.

# Importing Books to Database

- Book information can be added to the database from a *.csv file using the import.py program located in the root folder. 

# Search

- The search "engine" will search for matches or partial matches within the Heroku Postgres database and return the results.

# Book Information Pages

- 





- Another note: it's a good idea to add *.pyc to the .gitignore file, and additionally you can ask git to remove any *.pyc files that happen to already be tracked by git by running the following from the command line:

  $ git rm --cached *.pyc

  ... https://coderwall.com/p/wrxwog/why-not-to-commit-pyc-files-into-git-and-how-to-fix-if-you-already-did

- The flask_session folder should also be added to the .gitignore file.