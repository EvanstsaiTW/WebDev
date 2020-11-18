from flask import Flask, render_template, request, session, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField,TextAreaField
from wtforms.validators import DataRequired


################# db ##################    
basedir = os.path.abspath(os.path.dirname(__file__))
""" print("basedir") """
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
db.create_all()
app.config['SECRET_KEY'] = 'mykey'

class Post(db.Model):
    __table_name = 'post'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    sex = db.Column(db.Text)
    title = db.Column(db.Text)
    content = db.Column(db.Text)

    def __init__(self, name, sex, title, content):
        self.name = name
        self.sex = sex
        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.name}:{self.sex},{self.title},{self.content}"
        
################# db ##################   

#######Form#############
class ContentForm(FlaskForm):
    name = StringField("Username: ", validators= [DataRequired()])
    sex = RadioField('Please choose your sex: ', choices= ['Male', 'Female'])
    title = StringField("Title: ", validators= [DataRequired()])
    content = TextAreaField("Your post")
    submit = SubmitField('submit')

class searchForm(FlaskForm):
    key = StringField("keywords", validators=[DataRequired()])
    submit = SubmitField('search!')

########### views######## 
@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/signup_form', methods = ['GET', 'POST'])
def signup_form():    
    form = ContentForm()
    if form.validate_on_submit():
        name = form.name.data
        sex = form.sex.data
        title = form.title.data
        content = form.content.data
        new_member = Post(name, sex, title, content)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('thank_you'))
    all_post = Post.query.all()
    return render_template('signup_form.html', form = form, all_post = all_post)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = searchForm()
    if form.validate_on_submit():
        key = form.key.data
        all_query = Post.query.all()
        print(all_query)
        result = []
        for ind in range(len(all_query)):
            if key in all_query[ind].content:
                result.append(all_query[ind])
        return render_template('search.html', form = form, query = result)
    return render_template('search.html', form = form)

    
@app.route('/thank_you')
def thank_you():
    all_post = Post.query.all()
    return render_template('thank_you.html', all = all_post)

if __name__ == '__main__':
    app.run(debug=True) 