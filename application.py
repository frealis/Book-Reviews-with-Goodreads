import os
import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, redirect, render_template, request, session, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Load environment variables
load_dotenv(find_dotenv())
DATABASE_URL = os.getenv("DATABASE_URL")
if not os.getenv("DATABASE_URL"):
  raise RuntimeError("DATABASE_URL is not set")
FLASK_APP = os.getenv("FLASK_APP")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")
GOODREADS_API_KEY = os.getenv("GOODREADS_API_KEY")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Make session['user'] available globally across multiple threads before every GET 
# or POST request using 'g', which is a Flask object that basically functions as
# a global variable
@app.before_request
def before_request():
  g.id = None
  g.user = None
  if 'user' and 'id' in session:
    g.id = session['id']
    g.user = session['user']

@app.route("/")
def index():
  if g.id and g.user:
    return render_template(
      "index.html", 
      id=session['id'],
      user=session['user']
    )
  return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    blank = "You must enter a username and a password."
    password = request.form.get('password')
    username = request.form.get('user_name')
    wrong = "Incorrect username or password."
    session.pop('user', None)
    session.pop('id', None)
    if username and password:
      # The db.execute method returns ResultProxy, which is a cursor/pointer. To 
      # retrieve the results you have to iterate over ResultProxy using a FOR loop, 
      # *.fetchall(), *.first(), or something similar.
      users = db.execute("SELECT * FROM users").fetchall()
      for user in users:
        if user.username == username and user.password == password:
          # If the username and password match a row in the database then store
          # the username and id in the "session" 
          session['user'] = user.username
          session['id'] = user.id
          return redirect(url_for('index'))
      return render_template("login.html", alert=wrong)
    return render_template("login.html", alert=blank)
  return render_template("login.html")

@app.route("/logout")
def logout():
  session.pop('user', None)
  session.pop('id', None)
  info = "You have successfully logged out."
  return render_template("login.html", alert=info)

@app.route("/register", methods=["POST"])
def register():
  username = request.form.get('register_user_name')
  password = request.form.get('register_password')
  info = "You must enter a username and a password."
  taken = "Username is already taken."
  if username and password:
    users = db.execute("SELECT * FROM users").fetchall()
    for user in users:
      if user.username == username:
        return render_template("login.html", alert=taken)
    insert_new_user = db.execute(
      'INSERT INTO users (username, password) '
      'VALUES (:username_key, :password_key)', 
      {"username_key": username, "password_key": password}
    )
    db.commit()
    # Once the user successfully registers an account then the username that was
    # retrieved from the <form> on the register.html page is assigned to the 
    # session variable, but the user ID is unknown since it is only created by the
    # database after the INSERT query. The next SELECT query tries to find it.
    # Afterwards, once the id is known then it is assigned to the session
    # dictionary.
    user_id = db.execute(
      'SELECT id FROM users WHERE username=:username',
      {"username": username}
    ).fetchall()
    session['id'] = user_id[0][0]
    session['user'] = username
    return render_template(
      "register.html", 
      user_id=session['id'],
      username=session['user'],
      session=session
    )
  return render_template("login.html", alert=info)

@app.route("/search", methods=["POST"])
def search():
  search_term = request.form.get('search_bar')
  matches = []
  no_results = ''
  if search_term:
    # Convert the user's search input and database results all to lowercase
    search_results = db.execute(
      'SELECT * FROM books '
      'WHERE LOWER(title) LIKE LOWER(:search_term) '
      'OR LOWER(author) LIKE LOWER(:search_term) '
      'OR LOWER(isbn) LIKE LOWER(:search_term)', 
      {"search_term": '%' + search_term + '%'}
    )
    # Add the search results to matches[] and later return that list search.html
    for search_result in search_results:
      matches.append(search_result)
    if matches == []:
      no_results = "There were no search results."
    return render_template(
      "search.html", 
      matches=matches, 
      search_term=search_term, 
      alert=no_results
    )
  else:
    return "Must enter a search term."

@app.route("/<int:id>", methods=["GET", "POST"])
def book(id):
  avg_rating = 0
  number_of_ratings = 0
  rating = request.form.get('rating')
  total_rating = 0
  user_review_exists = False
  write_review = request.form.get('write_review')
  error = 'Cannot submit more than 1 review.'
  if id:
    # Get all of the information on the book
    specific_book = db.execute(
      'SELECT * FROM books '
      'WHERE id=:id',
      {"id": id}
    ).fetchall()
    # Get user & review data
    user_reviews = db.execute(
      'SELECT r.user_id, r.book_id, r.rating, r.review, '
      'u.id, u.username '
      'FROM reviews as r '
      'JOIN users u ON u.id = r.user_id '
      'WHERE book_id=:id',
      {"id": id}
    ).fetchall()
    # Get the average rating
    for user_rating in user_reviews:
      total_rating = total_rating + user_rating.rating
      number_of_ratings += 1
    avg_rating = total_rating / number_of_ratings
    # Check to see if user has already reviewed a specific book
    for i in user_reviews:
        if i.username == g.user:
          user_review_exists = True
    # Run an INSERT query to add a review if the user hasn't entered one yet
    if request.method == "POST" and user_review_exists == False:
      insert_review = db.execute(
        'INSERT INTO reviews (user_id, book_id, rating, review) '
        'VALUES (:user_id_key, :book_id_key, :rating_key, :write_review_key)',
        {
          # The user_id_key value comes from the global 'id' variable that is tied
          # to a user's current, active session. The book_id_key value comes from 
          # the argument that gets passed to the book(id) function.
          "user_id_key": g.id, 
          "book_id_key": id, 
          "rating_key": rating,
          "write_review_key": write_review
        }
      )
    # Return an error message if the user has already submitted a review
    elif request.method == "POST" and user_review_exists == True:
      return render_template(
      "specificbook.html", 
      avg_rating=avg_rating,
      error=error,
      id=id,
      specific_book=specific_book,
      user_reviews=user_reviews
    )
    db.commit()
    # Return specificbook.html upon a GET request
    return render_template(
      "specificbook.html", 
      avg_rating=avg_rating,
      id=id, 
      specific_book=specific_book,
      user_reviews=user_reviews
    )

@app.route("/api/<string:isbn>")
def api(isbn):
  api_book = db.execute(
    'SELECT * FROM books b WHERE b.isbn=:isbn',
    {"isbn": isbn}
  ).fetchall()
  # Since db.execute(...).fetchall() returns a list of tuples
  api_book
  return render_template(
    "api.html",
    api_book=api_book,
    isbn=isbn
  )