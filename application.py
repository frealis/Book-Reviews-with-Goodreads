import json, os, requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, g, redirect, render_template, request, session, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY")

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
# engine = create_engine(os.getenv("DATABASE_URL"))
engine = create_engine('postgres://hkctkuzxxzwyhg:1afb8f91941a789c9c54601c2836918e373512df10b27811fd471d6be951db46@ec2-50-17-227-28.compute-1.amazonaws.com:5432/d6lahufpt62238')
db = scoped_session(sessionmaker(bind=engine))

# Make session['user'] available globally across multiple threads before every GET 
# or POST request using 'g', which is a Flask object that basically functions as
# a global variable
# https://www.youtube.com/watch?v=eBwhBrNbrNI
@app.before_request
def before_request():
  g.id = None
  g.user = None
  if 'user' and 'id' in session:
    g.id = session['id']
    g.user = session['user']

@app.route("/", methods=["GET", "POST"])
def index():
  if g.id and g.user:
    if request.method == "POST":
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
        # Add the search results to matches[] and return it to search.html
        for search_result in search_results:
          matches.append(search_result)
        if matches == []:
          no_results = "There were no search results."
        return render_template(
          "index.html", 
          matches=matches, 
          search_term=search_term, 
          alert=no_results
        )
      else:
        return render_template(
          "index.html", 
          matches=matches, 
          search_term=search_term, 
          alert="Must enter a search term."
        )
    return render_template("index.html", id=session['id'], user=session['user'])
  return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  session.pop('user', None)
  session.pop('id', None)
  if request.method == "POST":
    error_blank = "Enter a username and a password >>"
    error_wrong = "Invalid username or password >>"
    password = request.form.get('password')
    username = request.form.get('user_name')
    if username and password:
      # The db.execute method returns ResultProxy, which is a cursor/pointer. To 
      # retrieve the results you have to iterate over ResultProxy using a FOR loop, 
      # *.fetchall(), *.first(), or something similar.
      users = db.execute("SELECT * FROM users").fetchall()
      for user in users:
        if user.username == username and user.password == password:
          # If the username and password match a row in the database then store
          # the username and id in the session variable.
          session['user'] = user.username
          session['id'] = user.id
          return redirect(url_for('index'))
      return render_template("login.html", alert=error_wrong)
    return render_template("login.html", alert=error_blank)
  return render_template("login.html")

@app.route("/logout")
def logout():
  session.pop('user', None)
  session.pop('id', None)
  info = "You have successfully logged out."
  return render_template("login.html", alert=info)

@app.route("/register", methods=["POST"])
def register():
  session.pop('user', None)
  session.pop('id', None)
  username = request.form.get('register_user_name')
  password = request.form.get('register_password')
  if username and password:
    # Check to see if the username is already stored in the database
    users = db.execute("SELECT * FROM users").fetchall()
    for user in users:
      if user.username == username:
        return render_template("login.html", alert="Username is already taken.")
    # Store username in database
    db.execute(
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
    # variable.
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
  return render_template("login.html", alert="You must enter a username and a password.")

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
    # Add the search results to matches[] and return it to search.html
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
    return render_template(
      "search.html", 
      matches=matches, 
      search_term=search_term, 
      alert="Must enter a search term."
    )

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
    # Get information on the book
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
    if number_of_ratings == 0:
      avg_rating = 0
    else:
      avg_rating = total_rating / number_of_ratings
    # Get Goodreads data via the Goodreads API
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GOODREADS_API_KEY, "isbns": specific_book[0].isbn})
    res_json = res.json()
    res_json_avg = res_json['books'][0]['average_rating']
    res_json_count = res_json['books'][0]['work_reviews_count']
    # Check to see if user has already reviewed a specific book
    for i in user_reviews:
        if i.username == g.user:
          user_review_exists = True
    # Run an INSERT query to add a review if the user hasn't entered one yet
    if request.method == "POST" and user_review_exists == False:
      db.execute(
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
      res=res,
      res_json_avg=res_json_avg,
      res_json_count=res_json_count,
      specific_book=specific_book,
      user_reviews=user_reviews
    )
    db.commit()
    # Get user & review data -again- so that new reviews show up as soon as they
    # are submitted by a user
    user_reviews = db.execute(
      'SELECT r.user_id, r.book_id, r.rating, r.review, '
      'u.id, u.username '
      'FROM reviews as r '
      'JOIN users u ON u.id = r.user_id '
      'WHERE book_id=:id',
      {"id": id}
    ).fetchall()
    # Return specificbook.html upon a GET request
    return render_template(
      "specificbook.html", 
      avg_rating=avg_rating,
      id=id, 
      res=res,
      res_json=res_json,
      res_json_avg=res_json_avg,
      res_json_count=res_json_count,
      specific_book=specific_book,
      user_reviews=user_reviews
    )

@app.route("/api/<string:isbn>")
def api(isbn):
  api_book = db.execute(
    'SELECT * FROM books b WHERE b.isbn=:isbn',
    {"isbn": isbn}
  ).first()
  # Since db.execute(...).fetchall() returns a list of tuples, but we need to 
  # return the book's data in json format, we can manually put everyting in json
  # format by creating a dictionary of key:value pairs
  api_json_format = {}
  api_isbn = api_book[1]
  api_title = api_book[2]
  api_author = api_book[3]
  api_year = api_book[4]
  api_json_format["isbn"] = api_isbn
  api_json_format["title"] = api_title
  api_json_format["author"] = api_author
  api_json_format["year"] = api_year
  # Get Goodreads data and add it to api_json_format{}
  res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GOODREADS_API_KEY, "isbns": isbn})
  res_json = res.json()
  res_json_avg = res_json['books'][0]['average_rating']
  res_json_count = res_json['books'][0]['work_reviews_count']
  api_json_format['average_score'] = res_json_avg
  api_json_format['review_count'] = res_json_count
  return render_template(
    "api.html",
    api_author=api_author,
    api_book=api_book,
    api_isbn=api_isbn,
    api_json_format=api_json_format,
    api_title=api_title,
    api_year=api_year,
    isbn=isbn
  )