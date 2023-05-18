from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from docx2pdf import convert
import tempfile
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/profiles'
db = SQLAlchemy(app)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(100), nullable=False)


@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    file = request.files['file']
    file_path = os.path.join(r'C:\Users\Murali\Downloads\File test', file.filename)
    file.save(file_path)
    pdf_filename = os.path.splitext(file.filename)[0] + '.pdf'
    pdf_path = os.path.join(r'C:\Users\Murali\Downloads\File test', pdf_filename)
    convert(file_path, pdf_path)
    new_file = Image(name=file.filename, path=pdf_path)
    db.session.add(new_file)
    db.session.commit()
    return 'Conversion successful'


if __name__ == '__main__':
    app.run(debug=True)
