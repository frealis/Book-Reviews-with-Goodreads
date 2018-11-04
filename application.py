import os
from flask import Flask, g, redirect, render_template, request, session, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
  raise RuntimeError("DATABASE_URL is not set")

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
  g.user = None
  if 'user' in session:
    g.user = session['user']
    # g.id = session['id']

@app.route("/")
def index():
  if g.user:
    return render_template("index.html", user=session['user'])
  return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    blank = "You must enter a username and a password."
    password = request.form.get('password')
    username = request.form.get('user_name')
    wrong = "Incorrect username or password."
    session.pop('user', None)
    if username and password:
      # The db.execute method returns ResultProxy, which is a cursor/pointer. To 
      # retrieve the results you have to iterate over ResultProxy using a FOR loop, 
      # *.fetchall(), or *.first().
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
    insert = db.execute(
      'INSERT INTO users (username, password) '
      'VALUES (:username_key, :password_key)', 
      {"username_key": username, "password_key": password}
      )
    db.commit()
    # Once the user successfully registers an account, their username is assigned
    # to the session variable & their session is now active
    session['user'] = username
    return render_template("register.html", results=insert)
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
      alert=no_results)
  else:
    return "Must enter a search term."

@app.route("/<int:id>", methods=["GET", "POST"])
def book(id):
  rating = request.form.get('rating')
  user_review_exists = False
  write_review_val = request.form.get('write_review')
  error = 'Cannot submit more than 1 review.'
  if id:
    # Get all of the information on a book with 1 query
    specific_book = db.execute(
      'SELECT b.id, b.isbn, b.title, b.author, b.year, '
      'r.user_id, r.book_id, r.review,'
      'u.id, u.username '
      'FROM books as b '
      'JOIN reviews r ON r.book_id = b.id '
      'JOIN users u ON u.id = r.user_id '
      'WHERE book_id=:id',
      {"id": id}
      ).fetchall()
    # Check to see if user has already reviewed a specific book
    for i in specific_book:
        if i.username == g.user:
          user_review_exists = True
    # Run an INSERT query to add a review if the user hasn't entered one yet
    if request.method == "POST" and user_review_exists == False:
      insert_review = db.execute(
        'INSERT INTO reviews (user_id, book_id, review) '
        'VALUES (:user_id_key, :book_id_key, :write_review_key)',
        {
          # The user_id_key value comes from the global 'id' variable that is tied
          # to a user's current, active session. The book_id_key value comes from 
          # the argument that gets passed to the book(id) function.
          "user_id_key": g.id, 
          "book_id_key": id, 
          "write_review_key": write_review_val
        }
      )
    # Return an error message if the user has already submitted a review
    elif request.method == "POST" and user_review_exists == True:
      return render_template(
      "specificbook.html", 
      error=error,
      id=id,
      rating=rating,
      specific_book=specific_book
    )
    db.commit()
    # Return specificbook.html upon a GET request
    return render_template(
      "specificbook.html", 
      id=id, 
      rating=rating,
      specific_book=specific_book
    )