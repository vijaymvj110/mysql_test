from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/profiles'

db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    path = db.Column(db.String(100))

    def __init__(self, name, path):
        self.name = name
        self.path = path


with app.app_context():
    db.create_all()


def create_uploads_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify('No image file found')

    image_file = request.files['image']

    if image_file.filename == '':
        return jsonify('No image file selected')

    filename = image_file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(file_path)

    image = Image(name=filename, path=file_path)
    db.session.add(image)
    db.session.commit()
    return jsonify('Image uploaded successfully')


if __name__ == '__main__':
    app.run(debug=True)
