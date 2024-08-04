from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from marshmallow import fields
from datetime import datetime
import redis
# pip install -U flask-sqlalchemy marshmallow-sqlalchemy

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

# user ................................................................
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, unique=True, nullable=False)
    role = db.Column(db.Text, nullable=False, default="user")
    requests = db.relationship('Req', back_populates='user', cascade='all, delete-orphan')
    issues = db.relationship('Issue', back_populates='user', cascade='all, delete-orphan')
    log = db.Column(db.DateTime, default=datetime.now, nullable=False)
    req_count = db.Column(db.Integer, default=0)

    def __init__(self, email, name, password, role, log = datetime.now()):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.log = log

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'role')

user_schema = UserSchema() # when querying just 1 user
users_schema = UserSchema(many=True) # when querying many, example users from a cityA.

# section .....................................................................
class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    books = db.relationship('Book', back_populates='section', cascade='all, delete-orphan')

    def __init__(self, name):
        self.name = name

class SectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)

# book .........................................................................
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    pages = db.Column(db.Integer, default=0)
    section_id = db.Column(db.Integer, ForeignKey('section.id'), nullable=False)
    section = db.relationship('Section', back_populates='books')
    requests = db.relationship('Req', back_populates='book', cascade='all, delete-orphan')
    issues = db.relationship('Issue', back_populates='book', cascade='all, delete-orphan')

    def __init__(self, title, author, content, pages, section_id):
        self.title = title
        self.author = author
        self.content = content
        self.pages = pages
        self.section_id = section_id

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'author', 'pages', 'volume', 'section_id')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Request ....................................................................
class Req(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='requests')
    book = db.relationship('Book', back_populates='requests')

    def __init__(self, book_id, user_id):
        self.book_id = book_id
        self.user_id = user_id

class ReqSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book_id', 'user_id')

request_schema = ReqSchema()
requests_schema = ReqSchema(many=True)

# Issue ....................................................................
class Issue(db.Model):
    __tablename__ = 'issue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='issues')
    book = db.relationship('Book', back_populates='issues')
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __init__(self, book_id, user_id, date):
        self.book_id = book_id
        self.user_id = user_id
        self.date = date

class IssueSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book_id', 'user_id', 'date')

issue_schema = IssueSchema()
issues_schema = IssueSchema(many=True)

# .............................................................................