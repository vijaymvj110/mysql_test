from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import smtplib

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/mail"
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))
    receiver = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    body = db.Column(db.String(500))

    def __init__(self, sender, receiver, subject, body):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body


class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "sender", "receiver", "subject", "body")


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route('/send_email', methods=['POST'])
def send_email():
    sender = request.json['sender']
    receiver = request.json['receiver']
    subject = request.json['subject']
    body = request.json['body']

    message = Message(sender=sender, receiver=receiver, subject=subject, body=body)
    db.session.add(message)
    db.session.commit()

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'vijaymvj114@gmail.com'
        smtp_password = 'vlfueujrluobmqie'

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        email_message = f"From:{sender}\nTo:{receiver}\nSubject:{subject}\n\nbody: {body}"

        server.sendmail(sender, receiver, email_message)
        server.quit()
        return jsonify(f'Email sent from {sender} to {receiver} successfully')
    except Exception as e:
        return jsonify(f'Error sending mail:{str(e)}')


if __name__ == '__main__':
    app.run(debug=True)
