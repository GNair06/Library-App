from flask import Flask, request, Response, jsonify, render_template
from models import *
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
import workers, tasks
from flask_cors import CORS
from flask_mail import Mail, Message
from mail import send_email
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.figure import Figure
import base64
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import redis

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_DEFAULT_SENDER'] = 'sender@example.com'

mail = Mail(app)

celery = workers.celery
celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1'
)

celery.Task = workers.ContextTask
app.app_context().push()

# python app.py
# redis-server
# celery -A app.celery beat --max-interval 1 -l info
# celery -A app.celery worker --loglevel=INFO
# mailhog
# npm run serve

jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)
mail.init_app(app)
bcrypt = Bcrypt(app)
with app.app_context():
    db.create_all()

CORS(app, supports_credentials=True)

# revoke access of books which have been issued for more than 5 days..........................
celery.conf.beat_schedule = {
    'delete-expired-issues-every-day': {
        'task': 'tasks.delete_expired_issues',
        'schedule': timedelta(seconds=30), 
        # 'schedule': timedelta(days=1),
    },
}

# home page ..................................................................................
@app.route('/', methods = ['GET'])
def home():
    admin = User(email='admin@admin.com', name='admin', password='hello', role='admin')
    lib = User(email='lib@user.com', name='lib', password='hello', role='librarian')
    try:
        db.session.add(lib)
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message": "registration successful"}), 201
    except Exception as e:
        db.session.rollback()
    return 'hello world'

# testing mailhog ...........................................................................
@app.route('/send_email_test')
def send_email_test():
    msg = Message('Subject', recipients=['recipient@example.com'])
    msg.body = 'Body'
    mail.send(msg)
    return 'Email sent!'

# register page .............................................................
@app.route("/register", methods = ['GET', 'POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    if not email or not name or not password:
        return jsonify({"error": "required fields cannot be empty"}), 409


    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"error": "user already exists"}), 409
    
    new_user = User(email=email, name=name, password=password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "registration successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "error"}), 500
    
# login page ....................................................................
@app.route("/login", methods = ['GET', 'POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    this_user = User.query.filter_by(email=email).first()

    if not this_user:
        return jsonify({"error": "user not found"}), 404
    
    if not bcrypt.check_password_hash(this_user.password, password):
        return jsonify({"error": "incorrect password"}), 404
    
    access_token = create_access_token(identity={
        'id': this_user.id,
        'role': this_user.role,
    })
    this_user.log = datetime.now()
    return jsonify({"message": "login successful", "access_token": access_token}), 200

# logout ...................................................................................
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({'message': 'logout successful'})
    unset_jwt_cookies(resp)
    return resp, 200

# dashboard .................................................................................
@app.route("/dashboard")
@jwt_required()
def dashboard():
    this_user = get_jwt_identity()
    this_user = user_schema.dump(this_user)
    all_users = User.query.filter_by(id=this_user['id']).all()
    all_users = users_schema.dump(all_users)
    return jsonify({'all_users': all_users}), 200

# admin dashboard ........................................................................... 
@app.route("/admin_dashboard")
@jwt_required()
def admin_dashboard():
    this_user = get_jwt_identity()
    if this_user['role'] != 'admin':
        return jsonify({"error": "unauthorised access"}), 401
    return jsonify({"message": "welcome admin"}), 200

# librarian dashboard ........................................................................... 
@app.route("/librarian_dashboard")
@jwt_required()
def librarian_dashboard():
    this_user = get_jwt_identity()
    if this_user['role'] != 'librarian':
        return jsonify({"error": "unauthorised access"}), 401
    return jsonify({"message": "welcome librarian"}), 200

# user dashboard ........................................................................... 
@app.route("/user_dashboard")
@jwt_required()
def user_dashboard():
    this_user = get_jwt_identity()
    if this_user['role'] != 'user':
        return jsonify({"error": "unauthorised access"}), 401
    return jsonify({"message": "welcome user"}), 200

# view all users ............................................................................
@app.route("/view_all_users", methods=['GET'])
@jwt_required()
def view_all_users():
    this_user = get_jwt_identity()
    if this_user['role'] != 'admin':
        return jsonify({"error": "Unauthorized access, very protected route"}), 401
    all_users = User.query.filter_by(role='user').all()
    all_users = users_schema.dump(all_users)
    return jsonify({'all_users': all_users}), 200

# get user information .............................................................
@app.route("/get_user_data", methods=['GET'])
@jwt_required()
def get_user_data():
    user = get_jwt_identity()
    user_id = user['id']
    this_user = User.query.get(user_id)
    if not this_user:
        return jsonify({'message': "user doesn't exist."}), 404
    this_user = user_schema.dump(this_user)
    return jsonify(this_user), 200

# create section .......................................................................
@app.route("/create_section", methods=['POST'])
@jwt_required()
def create_section():
    this_user = get_jwt_identity()
    if this_user['role'] != 'librarian':
        return jsonify({"error": "Unauthorized access"}), 401
    data = request.json
    name = data.get('name')
    new_section = Section(name=name)
    db.session.add(new_section)
    db.session.commit()
    return jsonify({'message': 'Section created successfully!'}), 201

# view all sections ............................................................................
@app.route("/view_all_sections", methods=['GET'])
@jwt_required()
def view_all_sections():
    this_user = get_jwt_identity()
    all_sections = Section.query.all()
    all_sections = sections_schema.dump(all_sections)
    return jsonify({'all_sections': all_sections}), 200

# search section using id (read) ...........................................................................
@app.route("/section/<int:id>", methods=['GET'])
def get_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({"error": "section doesn't exist"}), 404
    return jsonify({"section": section_schema.dump(section)}), 200

# edit section ................................................................................
@app.route("/edit_section/<int:id>", methods=['PUT'])
@jwt_required()
def edit_section(id):
    this_user = get_jwt_identity()
    if this_user['role'] != 'librarian':
        return jsonify({"error": "unauthorized access"})
    section = Section.query.get(id)
    if not section:
        return jsonify({"error": "section doesn't exist"})
    data = request.json
    name = data.get('name')

    section.name = name
    db.session.commit()
    return jsonify({"message": "section updated successfully"}), 200

# delete section ...........................................................................................
@app.route("/delete_section/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_section(id):
    this_user = get_jwt_identity()
    if this_user['role'] != 'librarian':
        return jsonify({"error": "unauthorized access"})
    section = Section.query.get(id)
    if not section:
        return jsonify({"error": "section doesn't exist"})
    
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "section deleted successfully"}), 200

# delete book ...........................................................................................
@app.route("/delete_book/<int:id>", methods=['DELETE'])
@jwt_required()
def delete_book(id):
    this_user = get_jwt_identity()
    if this_user['role'] != 'librarian':
        return jsonify({"error": "unauthorized access"})
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "book doesn't exist"})
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "book deleted successfully"}), 200


# Add a book to a Section .....................................................................................
@app.route('/<int:section_id>/add_book', methods=['POST'])
@jwt_required()
def add_book(section_id):
    try:
        this_user = get_jwt_identity()
        if this_user['role'] == 'user':
            return jsonify({'error': 'Unauthorized access'}), 401

        data = request.json
        title = data.get('title')
        author = data.get('author')
        pages = data.get('pages')
        content = data.get('content')
        section_id = section_id
    
        if not title or not author or not pages or not content:
            return jsonify({'message': 'Missing required fields.'}), 400

        new_book = Book(title=title, author=author, pages=pages, content=content, section_id=section_id)

        db.session.add(new_book)
        db.session.commit()

        return jsonify({'message': 'Book has been added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# view all books ...............................................................................................
@app.route('/view_all_books', methods=['GET'])
def view_all_books():
    try:
        all_books = Book.query.all()
        if not all_books:    
            return jsonify({'message': 'Books not found.'}), 404
        all_books = books_schema.dump(all_books)
        return jsonify({'all_books': all_books}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# view all books of a section ...................................................................................
@app.route('/books_of_section/<int:section_id>', methods=['GET'])
def books_of_section(section_id):
    all_books = []
    try:
        books = Book.query.all()
        for book in books:
            if book.section_id == section_id:
                all_books.append(book)
        if not all_books:    
            return jsonify({'message': 'Books not found.'}), 404
        all_books = books_schema.dump(all_books)
        return jsonify({'all_books': all_books}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# search book using id (read) ..................................................................................
@app.route('/book/<int:book_id>', methods=['GET'])
def view_book(book_id):
    try:
        this_book = Book.query.get(book_id)
        if not this_book:
            return jsonify({'message': 'Book not found'}), 404   
        this_book = book_schema.dump(this_book)
        return jsonify({'book': this_book}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# view book content ..................................................................................
@app.route('/view_book_content/<int:book_id>', methods=['GET'])
def view_book_content(book_id):
    lst = []
    try:
        this_book = Book.query.get(book_id)
        if not this_book:
            return jsonify({'message': 'book not found!'}), 404   
        book = {
            'title': this_book.title,
            'author': this_book.author,
            'content': this_book.content,
        }
        return jsonify({'book': book}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# edit book .....................................................................................................
@app.route('/edit_book/<int:book_id>', methods=['PUT'])
@jwt_required()
def edit_book(book_id):
    try:
        this_user = get_jwt_identity()
        if this_user['role'] == 'user':
            return jsonify({'error': 'Unauthorised access'}), 401

        this_book = Book.query.get(book_id)
        if not this_book:
            return jsonify({'message': 'Book not found'}), 404

        data = request.json
        this_book.title = data.get('title', this_book.title)
        this_book.author = data.get('author', this_book.author)
        this_book.pages = data.get('pages', this_book.pages)
        this_book.content = data.get('content', this_book.content)

        db.session.commit()

        return jsonify({'message': 'Changes have been saved.'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# search for book using section .......................................................................
@app.route('/section_form', methods=['POST'])
def section_form():
    section_name = request.json.get('sectionName')
    section = Section.query.filter_by(name=section_name).first()
    if section is not None:
        return jsonify({'section_id': section.id}) 
    else:
        return jsonify({'message': 'Section not found.'}), 404

    
# Request an ebook .............................................................................
@app.route('/request_book/<int:id>', methods=['POST'])
@jwt_required()
def request_book(id):
    try:
        this_user = get_jwt_identity()
        user_id = this_user['id']
        this_user = User.query.filter_by(id=user_id).first()
        this_book = Book.query.filter_by(id=id).first()
        
        if not this_book:
            return jsonify({'message': 'Book not found'}), 404
        
        request = Req.query.filter_by(user_id=user_id, book_id=this_book.id).first()

        if not request:
            if this_user.req_count >= 5:
                print('Cannot request for more than 5 books.')
            else:
                new_request = Req(user_id=this_user.id, book_id=this_book.id)
                db.session.add(new_request)
                this_user.req_count += 1
                db.session.commit()
                return jsonify({'message': 'Request made successfully'}), 201
        else:
            return jsonify({'message': 'Request for this book already exists'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error!'}), 500
    
# Issue ebook .............................................................................
@app.route('/issue_book/<int:req_id>', methods=['POST'])
@jwt_required()
def issue_book(req_id):
    try:
        this_user = get_jwt_identity()
        user_id = this_user['id']
        this_user = User.query.filter_by(id=user_id).first()
        if this_user.role == 'user':
            return jsonify({'error': 'Unauthorised access'}), 401
        this_req = Req.query.get(req_id)
        book_id = this_req.book_id
        this_book = Book.query.get(book_id)
        this_user = User.query.filter_by(id=this_req.user_id).first()

        issue = Issue.query.filter_by(user_id=this_req.user_id, book_id=book_id).first()
        if not issue:
            new_issue = Issue(user_id=this_req.user_id, book_id=book_id, date = datetime.now())
            db.session.add(new_issue)
            req = Req.query.filter_by(id=req_id).first()
            db.session.delete(req)
            this_user.req_count -= 1
            db.session.commit()
            return jsonify({'message': 'Book issued successfully'}), 201
        else:
            return jsonify({'message': 'Book has already been issued'}), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Error!'}), 500
    
# reject request ...........................................................................................
@app.route("/reject_request/<int:id>", methods=['DELETE'])
@jwt_required()
def reject_request(id):
    this_user = get_jwt_identity()
    if this_user['role'] != 'librarian':
        return jsonify({"error": "unauthorized access"})
    req = Req.query.get(id)
    user = User.query.get(req.user_id)
    db.session.delete(req)
    user .req_count -= 1
    if (user.req_count < 0):
        user.req_count = 0
    db.session.commit()
    return jsonify({"message": "request rejected"}), 200

# view all requests ...............................................................................................
@app.route('/view_all_requests', methods=['GET'])
def view_all_requests():
    lst = []
    try:
        all_requests = Req.query.all()
        if not all_requests:    
            return jsonify({'message': 'No requests available.'}), 404
        for request in all_requests:
            book = Book.query.get(request.book_id)
            user = User.query.get(request.user_id)
            lst.append({
                        'id': request.id,
                        'pages': book.pages,
                        'user_id': request.user_id,
                        'user_name': user.name,
                        'book_id': request.book_id,
                        'title': book.title,
                        'author': book.author,
                        'content': book.content,
                    })
        return jsonify({'lst': lst}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# view all issues ...............................................................................................
@app.route('/view_all_issues', methods=['GET'])
def view_all_issues():
    lst = []
    try:
        all_issues = Issue.query.all()
        if not all_issues:    
            return jsonify({'message': 'No issues available.'}), 404
        for issue in all_issues:
            book = Book.query.get(issue.book_id)
            user = User.query.get(issue.user_id)
            lst.append({
                        'id': issue.id,
                        'pages': book.pages,
                        'user_id': issue.user_id,
                        'user_name': user.name,
                        'book_id': issue.book_id,
                        'title': book.title,
                        'author': book.author,
                        'content': book.content,
                        'date': issue.date
                    })
        return jsonify({'lst': lst}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# view my issues ...............................................................................................
@app.route('/view_my_issues', methods=['GET'])
def view_my_issues():
    lst = []
    try:
        all_issues = Issue.query.all()
        all_books = Book.query.all()
        if not all_issues:    
            return jsonify({'message': 'No issues available.'}), 404
        for issue in all_issues:
            for book in all_books:
                if issue.book_id == book.id:
                    lst.append({
                        'id': issue.id,
                        'pages': book.pages,
                        'user_id': issue.user_id,
                        'book_id': issue.book_id,
                        'title': book.title,
                        'author': book.author,
                        'content': book.content,
                        'date': issue.date
                    })

        return jsonify({'lst': lst}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# view my requests ...............................................................................................
@app.route('/view_my_requests', methods=['GET'])
def view_my_requests():
    lst = []
    try:
        all_requests = Req.query.all()
        all_books = Book.query.all()
        if not all_requests:    
            return jsonify({'message': 'No requests available.'}), 404
        for request in all_requests:
            for book in all_books:
                if request.book_id == book.id:
                    lst.append({
                        'id': request.id,
                        'author': book.author,
                        'pages': book.pages,
                        'user_id': request.user_id,
                        'book_id': request.book_id,
                        'title': book.title,
                        'content': book.content,
                    })

        return jsonify({'lst': lst}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'an error has occurred'}), 500
    
# revoke access ...........................................................................................
@app.route("/revoke_access/<int:id>", methods=['DELETE'])
@jwt_required()
def revoke_access(id):
    this_user = get_jwt_identity()
    if this_user['role'] != 'librarian':
        return jsonify({"error": "unauthorized access"})
    issue = Issue.query.get(id)
    
    db.session.delete(issue)
    db.session.commit()
    return jsonify({"message": "access revoked"}), 200

# statistics ...................................................................................................
@app.route("/statistics", methods=['GET', 'POST'])
def statistics():
    return jsonify({"message": "success"}), 200

# section graph .................................................................................................
@app.route("/section_graph", methods=['GET', 'POST'])
def section_graph():
    x, y = [], []
    all_sections = Section.query.all()
    for section in all_sections:
        x.append(section.name)
        y.append(len(section.books))
    xx = np.array(x)
    yy = np.array(y)

    fig = Figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(xx, yy)
    
    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<br><h3>Section Graph</h3><img src='data:image/png;base64,{data}'/>"

# request graph .................................................................................................
@app.route("/request_graph", methods=['GET', 'POST'])
def request_graph():
    x, y = [], []
    all_books = Book.query.all()
    for book in all_books:
        x.append(book.title)
        y.append(len(book.requests))
    xx = np.array(x)
    yy = np.array(y)

    fig = Figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(xx, yy)
    
    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<br><h3>Requested Books Graph</h3><img src='data:image/png;base64,{data}'/>"

# issue graph .................................................................................................
@app.route("/issue_graph", methods=['GET', 'POST'])
def issue_graph():
    x, y = [], []
    all_books = Book.query.all()
    for book in all_books:
        x.append(book.title)
        y.append(len(book.issues))
    xx = np.array(x)
    yy = np.array(y)

    fig = Figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.bar(xx, yy)
    
    buf = BytesIO()
    fig.savefig(buf, format="png")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<br><h3>Issued Books Graph</h3><img src='data:image/png;base64,{data}'/>"

# ............................................................................................................

if __name__ == '__main__':
    app.run(debug=True)
