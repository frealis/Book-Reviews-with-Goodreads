# Project 1

Web Programming with Python and JavaScript

- Set environment variables:

  $ $env:FLASK_APP = "application.py"
  $ $env:FLASK_DEBUG = "1"                    // optional
  $ $env:DATABASE_URL = "database URL"

  ... this project uses a Postgresql database hosted by Heroku, and can be found by logging into your account, selected your project from the dashboard, clicking on "Heroku Postgres" under "Installed add-ons" > Settings > View Credentials.

  ... you can see which environment variables have currently been set by typing:

    $ Get-ChildItem Env:

  ... once the environment variables have been set you can start a Flask server with:

  $ flask run

- Connect to the Postgres database from the command line:

  $ psql "database URL" (no quotes)

- Creating a Login Page: https://www.youtube.com/watch?v=eBwhBrNbrNI

  ... so the logic behind the login is that when you visit the home page "/" it checks to see if g.user exists -- this is a global variable that holds the username. Since it probably won't exist the first time someone visits a page, they get directed to login.html. Additionally, the before_request() function clears g.user everytime a request is made -- whether it's a GET request to go to another page, reload the same page, or a POST request.
  
  ... when a user hits the "Submit" button, any key:value pair within the session{} dictionary that has key="user" gets popped, and then an IF conditional checks to make sure that the password is valid. If it is, then whatever was typed into the Username field from the <form> gets put into the session{} dictionary as {"user": username} or something similar I guess, and is stored as a cookie.
  
  ... anyways, the before_request() function will load this key:value pair into the g.user variable, and the g.user variable is used to determine whether or not a user can view index.html. As long as {"user": username} exists within the session{} dictionary then the user has an active session.
