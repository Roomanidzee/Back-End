from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    email = db.Column('user_email', db.String(120), unique=True)
    password = db.Column('user_password', db.String(128))

    books = relationship("Book", secondary="users_and_books")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return 'User{id = {0}, email = {1}}'.format(self.id, self.email)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column('book_id', db.Integer, primary_key=True)
    name = db.Column('book_name', db.String(120))
    author = db.Column('book_author', db.String(120))
    description = db.Column('book_description', db.Text())
    text_url = db.Column('book_text_url', db.String(120))
    coef_love = db.Column('book_coef_love', db.Numeric())
    coef_fantastic = db.Column('book_coef_fantastic', db.Numeric())
    coef_fantasy = db.Column('book_coef_fantasy', db.Numeric())
    coef_detective = db.Column('book_coef_detective', db.Numeric())
    coef_adventure = db.Column('book_coef_adventure', db.Numeric())
    coef_art = db.Column('book_coef_art', db.Numeric())

    users = relationship("User", secondary="users_and_books")

    def __init__(self, name, author, description, text_url, coef_love, coef_fantastic, coef_fantasy, coef_detective,
                 coef_adventure, coef_art):
        self.name = name
        self.author = author
        self.description = description
        self.text_url = text_url
        self.coef_love = coef_love
        self.coef_fantastic = coef_fantastic
        self.coef_fantasy = coef_fantasy
        self.coef_detective = coef_detective
        self.coef_adventure = coef_adventure
        self.coef_art = coef_art

    def __repr__(self):
        return "Book{id = {0}, name = {1}, author = {2}, text_url = {3}}".format(self.id, self.name,
                                                                                 self.author, self.text_url)

class UsersAndBooks(db.Model):
    __tablename__ = 'users_and_books'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), primary_key=True)
    mark = db.Column(db.Boolean)

    user = relationship(User, backref=backref("users_and_books", cascade="all, delete-orphan"))
    book = relationship(Book, backref=backref("users_and_books", cascade="all, delete-orphan"))

    def __init__(self, user_id, book_id, mark=False):
        self.user_id = user_id
        self.book_id = book_id
        self.mark = mark