from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

################# db ##################    
basedir = os.path.abspath(os.path.dirname(__file__))
""" print("basedir") """
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

class Color(db.Model):
    __tablename__ = 'color'

    id = db.Column(db.Integer,primary_key=True)
    
    color = db.Column(db.Text)
    name = db.Column(db.Text)

    def __init__(self, name, color):
        self.name = name
        self.color = color
    def __repr__(self):
        return f"{self.name}:{self.color}"
        
################# db ##################   

########### views######## 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup_form', methods = ['GET'])
def signup_form():    
    return render_template('signup_form.html')

@app.route('/thank_you')
def thank_you():
    color = request.args.get('color')
    name = request.args.get('name')
    new_member = Color(name, color)
    db.session.add(new_member)
    db.session.commit()
    all_color = Color.query.all()
    return render_template('thank_you.html', color = color, name = name, all = all_color)
    
if __name__ == '__main__':
    app.run(debug=True) 