from workers import celery
from celery.schedules import crontab
from models import *
from datetime import datetime, timedelta
from flask import render_template
from mail import send_email
import redis

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # every 30 seconds
    sender.add_periodic_task(30, daily_reminder.s(), name="daily_reminder")
    sender.add_periodic_task(30, monthly_reminder.s(), name="monthly_reminder")
    # evry day at 12 am
    #sender.add_periodic_task(crontab(minute=10, hour=0), daily_reminder.s(), name="daily_reminder")
    # 1st of evry month
    # sender.add_periodic_task(crontab(minute=0, hour=0, day_of_month=1), monthly_reminder.s(), name="monthly_reminder")

@celery.task
def daily_reminder():
    subject = "This is a reminder to visit our app."
    one_day = datetime.now() - timedelta(hours=24)
    user_lst = User.query.filter(User.log < one_day).all()
    print(len(user_lst))
    for user in user_lst:
        print(f"Daily reminder for {user.name}, {user.email}")
        html = render_template('daily_reminder.html', user=user)
        send_email(subject=subject, rec=user.email, html_content=html)
        print(f"daily reminder to {user.name} sent successfully")
    return "success" 

@celery.task
def delete_expired_issues():
    try:
        # Calculate the date 5 days ago
        five_days_ago = datetime.now() - timedelta(days=5)
        # Query for issues older than 5 days
        expired_issues = Issue.query.filter(Issue.date < five_days_ago).all()
        # Delete the expired issues
        for issue in expired_issues:
            db.session.delete(issue)
        # Commit the changes to the database
        db.session.commit()
        return f"{len(expired_issues)} expired issues deleted successfully."
    
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"


@celery.task
def monthly_reminder():
    subject = "This is a monthly reminder"
    users = User.query.filter_by(role = "user").all()
    for user in users:
        issues = Issue.query.filter_by(user_id=user.id).all()
        lst = []
        for issue in issues:
            book = Book.query.filter_by(id=issue.book_id).first()
            lst.append({
                'date': issue.date.strftime("%d-%m-%Y %H:%M"),
                'book': book
            })
        html = render_template('monthly_reminder.html', user=user, lst=lst)
        send_email(subject=subject, rec=user.email, html_content=html)
    return "success"