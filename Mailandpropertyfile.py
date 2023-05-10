from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import smtplib
import configparser

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/E_mail'
db = SQLAlchemy(app)


class Mail(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.String(50))
    receiver = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    body = db.Column(db.String(500))

    def __init__(self, sender, receiver, subject, body):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body


with app.app_context():
    db.create_all()


@app.route('/send_mail', methods=['POST'])
def mail_send():
    receiver = request.json['receiver']
    subject = request.json['subject']
    body = request.json['body']
    message = Mail(sender='vijaymvj114@gmail.com', receiver=receiver, subject=subject, body=body)
    db.session.add(message)
    db.session.commit()

    try:
        config = configparser.ConfigParser()
        config.read('config.properties')
        smtp_username = config.get('SMTP', 'username')
        smtp_password = config.get('SMTP', 'password')
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        email_message = f"From:{message.sender}\nTo:{receiver}\nsubject:{subject}\n\nbody:{body}"
        server.sendmail(message.sender, receiver, email_message)
        server.quit()
        return jsonify(f"E-mail send from {message.sender} to the {receiver} successfully")
    except Exception as e:
        return jsonify(f"Error in sending mail:{str(e)}")


if __name__ == '__main__':
    app.run(debug=True)
