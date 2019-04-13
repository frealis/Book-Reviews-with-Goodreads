# Web Programming with Python and JavaScript - Project 1

# Overview
- The website is powered by Flask, styled with Boostrap 4, and uses a Heroku Postgres database. It allows visitors to search for 5000 books stored in its database, read and write reviews for those books, view ratings on the same books from a site called "Goodreads" (https://www.goodreads.com/), and retrieve book reviews and details through an API.

- https://docs.cs50.net/web/2018/x/projects/1/project1.html

# Setup & Configuration
- Flask needs to know which file is used to start the server/run the application, and additionally the database URL and Goodreads API key need to be set. These can be set using environment variables. Using Powershell you can set environment variables manually from the command line:

  $ $env:DATABASE_URL = "database URL"
  $ $env:FLASK_APP = "application.py"
  $ $env:FLASK_DEBUG = "1"  // optional
  $ $env:GOODREADS_API_KEY = "goodsreads api key"

  ... or you can store the variables in a .env file within the root directory and retrieve them via dotenv: https://pypi.org/project/python-dotenv/#installation

  ... in Powershell you can see which environment variables have currently been set by typing:

    $ Get-ChildItem Env:

- Start the Flask server:

  $ flask run

- Connect to the Heroku Postgres database from the command line (credentials are at Dashboard > cs50-book-review-w-goodreads > Heroku Postgres > Settings > Database Credentials/View Credentials) with either command:

  $ psql database_URL

  -or-

  $ heroku pg:psql <database-name> --app cs50-book-review-w-goodreads

# Login

- Creating a Login Page: https://www.youtube.com/watch?v=eBwhBrNbrNI

- Login process:

  1. When a client visits the home page "/" the web application checks to see if g.user exists -- 'g' in Flask is a global variable, and in this web application it represents an active session (assuming that there is one). If no session exists then the client gets directed to login.html so that they can register/log in and create an active session.
  
  2. After loggin in, any key:value pair within the session{} dictionary that has key="user" gets popped (in case the client had previously logged in), and then the database is checked to make sure that the password is valid. If it is, then whatever username was submitted from the username field in the <form> is stored in the session{} dictionary.
  
  ... the before_request() function will assign session['user'] to g.user, and the g.user variable is used to determine whether or not a client has an active session and is able to view index.html. As long as {"user": username} exists within the session{} dictionary then the client has an active session.

- Another note: it's a good idea to add *.pyc to the .gitignore file, and additionally you can ask git to remove any *.pyc files that happen to already be tracked by git by running the following from the command line:

  $ git rm --cached *.pyc

  ... https://coderwall.com/p/wrxwog/why-not-to-commit-pyc-files-into-git-and-how-to-fix-if-you-already-did

- The flask_session folder should also be added to the .gitignore file.