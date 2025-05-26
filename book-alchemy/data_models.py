from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    death_date = db.Column(db.Date, nullable=True)
    books = db.relationship('Book', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return f"{self.name}"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    title = db.Column(db.String(120), nullable=False)
    publication_year = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return f"{self.title} (Author ID: {self.author_id})"