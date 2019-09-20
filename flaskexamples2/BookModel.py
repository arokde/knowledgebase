from flask import json
from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Float,nullable=False)
    isbn = db.Column(db.Integer)


    def add_book(param_name,param_price,param_isbn):
        new_book = Book(name=param_name,price=param_price,isbn=param_isbn)
        db.session.add(new_book)
        db.session.commit()

    def to_json(book):
        return {'name':book.name,'price':book.price,'isbn':book.isbn}

    def get_all_books():
        return [ Book.to_json(book) for book in Book.query.all()]

    def get_book(param_isbn):
        return Book.to_json(Book.query.filter_by(isbn=param_isbn).first())

    def delete_book(param_isbn):
        is_successful = Book.query.filter_by(isbn=param_isbn).delete()
        db.session.commit()
        return bool(is_successful)

    def update_book_price(param_isbn,param_price):
        book_to_update = Book.query.filter_by(isbn=param_isbn).first()
        book_to_update.price = param_price
        db.session.commit()

    def update_book_name(param_isbn, param_name):
        book_to_update = Book.query.filter_by(isbn=param_isbn).first()
        book_to_update.name = param_name
        db.session.commit()

    def replace_book(param_isbn, param_name, param_price):
        book_to_update = Book.query.filter_by(isbn=param_isbn).first()
        book_to_update.name = param_name
        book_to_update.price = param_price
        db.session.commit()

    def __repr__(self):
        book_object = {
            'name' : self.name,
            'price':self.price,
            'isbn':self.isbn
        }
        return json.dumps(book_object)
