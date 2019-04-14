import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Create the database engine, get database URL from .env
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
  with open("books.csv") as f:
    reader = csv.reader(f)
    print(reader)
    for isbn, title, author, year in reader:
      db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn_key, :title_key, :author_key, :year_key)", {"isbn_key": isbn, "title_key": title, "author_key": author, "year_key": year})
      print(f"Added ISBN: {isbn}, '{title}' by {author}, {year}.")
    db.commit()

if __name__ == "__main__":
  main()