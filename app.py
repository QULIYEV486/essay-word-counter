from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///text2.db"
db.init_app(app)
import os
from werkzeug.utils import secure_filename 



UPLOAD_FOLDER ='./static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from sqlalchemy import desc


class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=True)
    text = db.Column(db.String(10000), nullable = True)
     

    def __init__(self, count, text):
        self.count = count
        self.text = text
        


@app.route("/", methods = ['GET', 'POST'])
def addnews():
    if request.method == "GET":
        return render_template('index.html')
    else:
        replacements = [('!', ''), ('?', ''), ('.', ''), (',', '')]
        text = request.form['text']
        text2 = request.form['text']
        for char, replacement in replacements:
            if char in text:
                text2 = text.replace(char, replacement)
        text_list = text2.split()
        count = len(text_list)

        print(text_list)
         
         
        new_text = Text(count, text, )
        db.session.add(new_text)
        db.session.commit()
        return redirect(url_for('text'))


@app.route("/texts", methods = ['GET', 'POST'])
def text():
    texts = Text.query.order_by(desc(Text.id))
    # Text.query.filter(Text.id == text).delete()
    
    return render_template('texts.html', texts=texts)

         

@app.route('/deletenote/<int:id>')
def deletenote(id):
    texts = Text.query.get(id)
    db.session.delete(texts)
    db.session.commit()
    return redirect(url_for('text'))


    


    
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)