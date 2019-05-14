# Web Programming with Python and JavaScript - Project 1

# Overview
- This website is powered by Flask, styled with Boostrap 4, and uses a Heroku Postgres database. It allows visitors to search for 5000 books stored in its database, read and write reviews for those books, view ratings on the same books from a site called "Goodreads" (https://www.goodreads.com/), and retrieve book reviews and details through an API.

- This is project 1 for CS50 - Web Programming with Python and Javascript:

  https://docs.cs50.net/web/2018/x/projects/1/project1.html

# Development Setup & Configuration
- Environment variables are used to start the server, access the database, access the Goodreads API, and toggle development settings. Using Powershell you can set environment variables manually from the command line:

  $ $env:DATABASE_URL = "database URL"
  $ $env:FLASK_APP = "application.py"
  $ $env:GOODREADS_API_KEY = "goodsreads api key"
  $ $env:FLASK_ENV = "development"  // debugger + automatic reloader
  $ $env:FLASK_DEBUG = "1"          // debugger
  $ $env:FLASK_ENV = "production"   // turn off development (off by default)
  $ $env:SECRET_KEY = "secret key"  // encrypt session cookies
  $ Get-ChildItem Env:              // view environment variables

  ... or you can store the variables in a .env file within the root directory and retrieve them via dotenv: https://pypi.org/project/python-dotenv/#installation. Make sure to set FLASK_ENV = "production" (or just omit the FLASK_ENV variable entirely) in production.

- Start the Flask server:

  $ flask run

- Connect to the Heroku Postgres database from the command line (credentials are at Dashboard > cs50-book-review-w-goodreads > Heroku Postgres > Settings > Database Credentials/View Credentials) with either command:

  $ psql database_URL

  -or-

  $ heroku pg:psql <database-name> --app cs50-book-review-w-goodreads

# Login
_login.html, login.js_

- Creating a Login Page: https://www.youtube.com/watch?v=eBwhBrNbrNI

- Login & Sessions:

  1. The time between when a client logs on and logs off is called a "session", and Flask uses a "session object" to store information about a client during this time. So in Flask, a "session" is basically both a length of time and an object.

  2. When a client reigsters for a new account or signs in with an existing account, their username and user ID are stored in a "session object". A "session object" is basically a dictionary of key:value pairs used to represent an active session. Flask places the session object in a cookie and uses a "secret key" to encrypt it. When creating an instance of a Flask application within app.py/application.py its secret key can be set like this:

    > app = Flask(__name__)
    > app.secret_key = <secret key goes here>

    ... to generate a random key from the command line:

    $ python -c 'import os; print(os.urandom(16))'

  3. Flask has a special function called before_request() that runs before each request, including GET and POST requests. This web application uses it to assign session['user'] and session['id'] to g.user and g.id, respectively. The 'g' variable is a special Flask variable that persists between client requests, so it essentially acts like a global variable. The web application uses it to represent a client's active session.

# Importing Books to Database
_import.py, books.csv_

- Book information can be added to the database from a *.csv file using the import.py program located in the root folder. Alternatively, you could use the COPY command in Postgres:

  db=> \copy test (isbn, title, author, year) from 'books.csv' delimiter ',' csv;

  ... https://www.postgresql.org/docs/9.2/sql-copy.html

- Postgres tables sometimes lock up, preventing functions like UPDATE or ALTER TABLE. View possible locks on tables and their associated pid's in Postgres by running the following:

  db=> SELECT * FROM pg_locks WHERE relation=(SELECT oid FROM pg_class WHERE relname='table_name_goes_here');

  ... to get information on the actual queries that may be locking up the Postgres database, run this:

  db=>  SELECT pid, state, usename, query, query_start 
        FROM pg_stat_activity 
        WHERE pid in (
          SELECT pid FROM pg_locks l 
          JOIN pg_class t ON l.relation = t.oid 
          AND t.relkind = 'r' 
          WHERE t.relname = 'search_hit'
        );

  ... to kill any hanging queries there are two options:

  db=> SELECT pg_cancel_backend(pid);       // less forceful
  db=> SELECT pg_terminate_backend(pid);    // more forceful

  ... more resources on Postgres locks: 
  
    1. https://wiki.postgresql.org/wiki/Lock_Monitoring
    2. https://jaketrent.com/post/find-kill-locks-postgres/
    3. https://www.citusdata.com/blog/2018/02/15/when-postgresql-blocks/

# Search
_index.html, search-bar.html_

- The search function will search for matches or partial isbn, book title, or  author matches within the Heroku Postgres database and return the results. Clients can also limit the number of books that are returned from search results.

# Book Information Pages
book.html
- Each book has an assigned 'id' value, and when a client selects an individual book from the search results they are directed the specific book's information page via /book/<id>. The page displays the book's reviews and ratings that have been submitted to the site, as well as the book's average rating and number of ratings on goodreads.com which is accessed through a Goodreads API. 

# API Access
- If a client visits the /api/<isbn> route, the website returns a JSON response containing the book's title, author, publication year, ISBN, Goodreads reviews, and Goodreads average rating.

# Production
- Resources on deploying Flask applications:

  1. http://flask.pocoo.org/docs/1.0/tutorial/deploy/
  2. http://flask.pocoo.org/docs/1.0/config/


# Notes
- It's a good idea to add *.pyc to the .gitignore file, and additionally you can ask git to remove any *.pyc files that happen to already be tracked by git by running the following from the command line:

  $ git rm --cached *.pyc

  ... https://coderwall.com/p/wrxwog/why-not-to-commit-pyc-files-into-git-and-how-to-fix-if-you-already-did

- The flask_session folder should also be added to the .gitignore file.
