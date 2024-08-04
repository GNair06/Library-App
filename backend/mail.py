from flask import current_app as app
from flask_mail import Message, Mail


mail = Mail()

def init_app(app):
    mail.init_app(app)

def send_email(subject, rec, html_content):
    with app.app_context():
        msg = Message(subject, sender="admin@library.com", recipients=[rec])
        msg.html = html_content
        mail.send(msg)