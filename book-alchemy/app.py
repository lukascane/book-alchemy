from flask import Flask, render_template, request, redirect, url_for
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite'
db.init_app(app)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form['birthdate']
        death_date_str = request.form['date_of_death']

        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        death_date = datetime.strptime(death_date_str, '%Y-%m-%d').date() if death_date_str else None

        new_author = Author(name=name, birth_date=birth_date, death_date=death_date)
        db.session.add(new_author)
        db.session.commit()
        return render_template('add_author.html', message='Author added successfully!')
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        new_book = Book(title=title, isbn=isbn, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        return render_template('add_book.html', authors=authors, message='Book added successfully!')
    return render_template('add_book.html', authors=authors)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/author/<int:author_id>')
def author_detail(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('author_detail.html', author=author)

@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('home', message=f'Author "{author.name}" and their books deleted successfully!'))

@app.route('/search_results')
def search_results():
    query = request.args.get('query')
    if query:
        search = f"%{query}%"
        results = Book.query.filter(db.func.lower(Book.title).like(search.lower())).all()
        return render_template('home.html', books=results, authors=Author.query.all())
    else:
        return redirect(url_for('home'))

@app.route('/')
def home():
    books = Book.query.all()
    authors = Author.query.all()
    message = request.args.get('message')
    return render_template('home.html', books=books, authors=authors, message=message)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)