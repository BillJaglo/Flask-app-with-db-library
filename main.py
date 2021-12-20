from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

all_books = []


@app.route('/')
def home():
    return render_template('index.html', books_list=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_data = request.form
        all_books.append(
            {"title": book_data["name"],
             "author": book_data["author"],
             "rating": book_data["rating"],
             }
        )
        # redirect allows you to redirect user to a page after they click the button if the POST method is used
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
