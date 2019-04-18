import json, os, requests
from dotenv import load_dotenv, find_dotenv
from flask import abort, Flask, g, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from string import Template

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
engine = create_engine(os.getenv("DATABASE_URL"))
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

# ==================== Handle INDEX route ====================
@app.route("/", methods=["GET", "POST"])
def index():
  if g.id and g.user:
    alert=''
    search_results_list = []
    search_results_message = ''
    search_term = ''

    # Handle POST requests
    if request.method == "POST":

      # This is a sort of hack using the *.get() method to get data that is not
      # normally returned by a standard POST request - it grabs the value of the
      # "value" attribute in a hidden <div> HTML element somewhere from whichever
      # page routed the client to this spot via a POST request. An AJAX request 
      # would probably be easier.
      # https://stackoverflow.com/questions/32022568/get-value-of-a-form-input-by-id-python-flask
      results_limit = request.form.get("results_limit", "")
      search_term = request.form.get('search_bar')

      # Check if a search term was submitted by client
      if search_term:

        # Show all search results (42 was arbitrarily chosen to represent 'all'),
        # and convert everything to lowercase to simplify matches
        if results_limit == 42:
          search_results = db.execute(
          'SELECT * FROM books '
          'WHERE LOWER(title) LIKE LOWER(:search_term) '
          'OR LOWER(author) LIKE LOWER(:search_term) '
          'OR LOWER(isbn) LIKE LOWER(:search_term) ',
          {"search_term": '%' + search_term + '%'})

        # Limit search results to a value selected by the client
        else:
          search_results = db.execute(
            'SELECT * FROM books '
            'WHERE LOWER(title) LIKE LOWER(:search_term) '
            'OR LOWER(author) LIKE LOWER(:search_term) '
            'OR LOWER(isbn) LIKE LOWER(:search_term) '
            'LIMIT :results_limit', 
            {"search_term": '%' + search_term + '%',
            "results_limit": results_limit}) 

        # Add the search results to search_results_list[] and return it to 
        # index.html, or create alert message if there are no search matches
        for search_result in search_results:
          search_results_list.append(search_result)
        if search_results_list == []:
          alert = "There were no search results."
        search_results_message=Template('Search results for "$search_term": ').substitute(search_term=search_term)
      
      # Create alert message if client submits a search with no search term
      else:
        alert="Must enter a search term."
    
    # Render index.html after a GET or POST request
    return render_template(
      "index.html", 
      search_results_list=search_results_list, 
      search_results_message=search_results_message, 
      alert=alert,
      user=g.user,)

  # Send client to login.html if there is no active session
  return render_template("login.html")

# ==================== Handle LOGIN route ====================
@app.route("/login", methods=["GET", "POST"])
def login():

  # Remove active session if it exists
  session.pop('user', None)
  session.pop('id', None)

  # Handle POST requests
  if request.method == "POST":
    error_blank = "Enter a username and a password >>"
    error_wrong = "Invalid username or password >>"
    password = request.form.get('password')
    username = request.form.get('user_name')

    # Check that the user entered both a username and a password
    if username and password:

      # The db.execute method returns ResultProxy, which is a cursor/pointer. To 
      # retrieve the results you have to iterate over ResultProxy using a FOR loop, 
      # *.fetchall(), *.first(), or something similar.
      users = db.execute("SELECT * FROM users").fetchall()
      for user in users:
        if user.username == username and user.password == password:

          # If the username and password match a row in the database then this 
          # indicates a valid username/password combination, so the next step
          # is to create an active session by storing the username and id in the 
          # session variable.
          session['user'] = user.username
          session['id'] = user.id
          return redirect(url_for('index'))
      
      # Send client back to login page if username/password combination does not 
      # exist.
      return render_template("login.html", alert=error_wrong)

    # Send client back to login page if username and/or password field is blank.
    return render_template("login.html", alert=error_blank)

  # Render login.html on a GET request.
  return render_template("login.html")

# ==================== Handle LOGOUT route ====================
@app.route("/logout")
def logout():

  # Remove active session if it exists.
  session.pop('user', None)
  session.pop('id', None)
  info = "You have successfully logged out."
  return render_template("login.html", alert=info)

# ==================== Handle REGISTER route ====================
@app.route("/register", methods=["POST"])
def register():

  # Remove active session if it exists.
  session.pop('user', None)
  session.pop('id', None)

  # Handle POST requests (which is currently the only allowed type of request).
  # Clients get to this route from login.html.
  if request.method == "POST":
    username = request.form.get('register_user_name')
    password = request.form.get('register_password')

    # Check that client entered both username and password.
    if username and password:

      # Check to see if the username is already taken, if so return to login.html.
      users = db.execute("SELECT * FROM users").fetchall()
      for user in users:
        if user.username == username:
          return render_template("login.html", alert="Username is already taken.")

      # Store username in database.
      db.execute(
        'INSERT INTO users (username, password) '
        'VALUES (:username_key, :password_key)', 
        {"username_key": username, "password_key": password})
      db.commit()

      # Once the user successfully registers an account then the username that was
      # retrieved from the <form> on the register.html page is assigned to the 
      # session variable, but the user ID is unknown since it is only created by 
      # the database after the INSERT query. This SELECT query tries to find it. 
      # Afterwards, once the id is known then it is assigned to the session
      # variable.
      user_id = db.execute(
        'SELECT id FROM users WHERE username=:username',
        {"username": username}).fetchall()
      session['id'] = user_id[0][0]
      session['user'] = username

      # Send the client to register.html to let them know that they have 
      # successfully registered.
      return render_template(
        "register.html", 
        user=session['user'])

    # Send client to login page if username and/or password field is blank.    
    return render_template("login.html", alert="You must enter a username and a password.")

# ==================== Handle BOOK route ====================
@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
  ratings_avg = 0
  ratings_count = 0
  ratings_sum = 0
  rating = request.form.get('rating-selection')
  user_review_exists = False
  write_review = request.form.get('write_review')
  error = ''

  # Check to make sure that a book_id value was entered in the URL
  if book_id:

    # Get information on the book
    specific_book = db.execute(
      'SELECT * FROM books '
      'WHERE id=:id',
      {"id": book_id}).fetchall()

    # Get user ratings & reviews
    user_reviews = db.execute(
      'SELECT r.user_id, r.book_id, r.rating, r.review, '
      'u.id, u.username '
      'FROM reviews as r '
      'JOIN users u ON u.id = r.user_id '
      'WHERE book_id=:id',
      {"id": book_id}).fetchall()
      
    # Get the average user rating
    for user_rating in user_reviews:
      ratings_sum = ratings_sum + user_rating.rating
      ratings_count += 1
    if ratings_count == 0:
      ratings_avg = 0
    else:
      ratings_avg = ratings_sum / ratings_count

    # Get Goodreads data via the Goodreads API
    goodreads_response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GOODREADS_API_KEY, "isbns": specific_book[0].isbn})
    goodreads_response_json = goodreads_response.json()
    goodreads_response_json_avg = goodreads_response_json['books'][0]['average_rating']
    goodreads_response_json_count = goodreads_response_json['books'][0]['work_reviews_count']

    # Handle POST requests
    if request.method == "POST":

      # Check to see if user has already reviewed a specific book
      for i in user_reviews:
          if i.username == g.user:
            user_review_exists = True

      # Run an INSERT query to add a review if the user hasn't entered one yet
      if user_review_exists == False:
        db.execute(
          'INSERT INTO reviews (user_id, book_id, rating, review) '
          'VALUES (:user_id_key, :book_id_key, :rating_key, :write_review_key)',
          {

            # The user_id_key value comes from the global 'id' variable that is 
            # tied to a user's current, active session. The book_id_key value 
            # comes from the argument that gets passed to the book(book_id) 
            # function. The rating and review are taken from the HTML form.
            "user_id_key": g.id, 
            "book_id_key": book_id, 
            "rating_key": rating,
            "write_review_key": write_review
          })
        db.commit()

        # Get -updated- user ratings & reviews
        user_reviews = db.execute(
          'SELECT r.user_id, r.book_id, r.rating, r.review, '
          'u.id, u.username '
          'FROM reviews as r '
          'JOIN users u ON u.id = r.user_id '
          'WHERE book_id=:id',
          {"id": book_id}).fetchall()

        # Reset the ratings values so that they can be re-calculated & updated
        ratings_avg = 0
        ratings_count = 0
        ratings_sum = 0

        # Get the -updated- average user rating
        for user_rating in user_reviews:
          ratings_sum = ratings_sum + user_rating.rating
          ratings_count += 1
        if ratings_count == 0:
          ratings_avg = 0
        else:
          ratings_avg = ratings_sum / ratings_count

      # Return an error message if the user has already submitted a review
      elif user_review_exists == True:
        error = 'Users may only submit 1 review per book.'

  # Render book.html after a GET or POST request
  return render_template(
    "book.html", 
    book_id=book_id, 
    error=error,
    goodreads_response_json_avg=goodreads_response_json_avg,
    goodreads_response_json_count=goodreads_response_json_count,
    ratings_avg=ratings_avg,
    ratings_count=ratings_count,
    specific_book=specific_book,
    user_reviews=user_reviews,
    user=g.user)

# ==================== Handle API requests ====================
@app.route("/api/<string:isbn>")
def api(isbn):

  # Search for the book by ISBN number and return 404 if not found. The
  # db.execute() method returns a ResultProxy, aka 'api_book', which is a pointer.
  try:
    api_book = db.execute(
      'SELECT * FROM books b '
      'WHERE b.isbn=:isbn', 
      {"isbn": isbn}).fetchall()[0] # *.first() returns None, not an exception
  except:
    return abort(404)

  # Since db.execute(...).fetchall() returns a list of tuples (although in this
  # case we are only extracting the first tuple, [0], from the list), but we need 
  # to return the book's data in json format, we can manually put everyting in 
  # json format by creating a dictionary of key:value pairs.
  api_dict = {}
  api_dict["isbn"] = api_book[1]
  api_dict["title"] = api_book[2]
  api_dict["author"] = api_book[3]
  api_dict["year"] = api_book[4]

  # Get Goodreads data and add it to api_dict{}
  res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": GOODREADS_API_KEY, "isbns": isbn})
  res_json = res.json()
  res_json_avg = res_json['books'][0]['average_rating']
  res_json_count = res_json['books'][0]['work_reviews_count']
  api_dict['average_score'] = res_json_avg
  api_dict['review_count'] = res_json_count

  # Use Flask's jsonify() function to convert dictionaries into JSON objects
  return jsonify(api_dict)