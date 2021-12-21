from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

## CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-library.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE
class Book(db.Model):
    # these are the column headings in the table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True)
    author = db.Column(db.String(250))
    rating = db.Column(db.Float)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


# this creates the database
db.create_all()


@app.route("/")
def home():
    # read database and put all records into a list
    books_library = db.session.query(Book).all()
    return render_template('index.html', all_books=books_library)


@app.route("/add", methods=["GET", "POST"])
def add():
    # there is a form on the add page, if the user clicks the submit, a POST method is called
    if request.method == "POST":
        # this pulls in the data from the form
        book_data = request.form
        # this creates an object in the database using the class Book and the information from the form the user entered
        new_book = Book(title=book_data["name"], author=book_data["author"], rating=book_data["rating"])
        # add the new information and commit to database
        db.session.add(new_book)
        db.session.commit()
        # redirect allows you to redirect user to a page after they click the button if the POST method is used
        return redirect(url_for('home'))
    # will just render the normal add.html page is the method == GET
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    # there is a form on the edit page, if the user clicks the button, a POST method is called
    if request.method == "POST":
        book_id = request.form['id']
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))
    # gets the book_id from the index or db
    book_id = request.args.get('id')
    # queries the book that is to be edited based on the book_id #
    book_selected = Book.query.get(book_id)
    return render_template('edit.html', book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)
