from celery_config import app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from DB import Database

users_db = Database('users')

@app.task
def send_email(subject, body, to_email):
    from_email = "your_email@example.com"
    password = "your_password"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

@app.task
def check_and_notify_users(properties):
    users = users_db.find_all()  # Fetch all users
    for user in users:
        for property in properties:
            if is_property_of_interest(property, user['criteria']):
                subject = "New Property Found"
                body = f"Property: {property}"
                send_email.delay(subject, body, user['email'])

def is_property_of_interest(property, criteria):
    return property['price'] < criteria['max_price'] and property['location'] == criteria['location']
