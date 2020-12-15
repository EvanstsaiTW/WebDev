#app.py
from myproject import app,db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User, Post
from myproject.forms import LoginForm, RegistrationForm, ContentForm, SearchForm

        
@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/post_form', methods = ['GET', 'POST'])
def post_form():    
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
    return render_template('post_form.html', form = form, all_post = all_post)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
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

# project 2: 
@app.route('/welcome_user')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome') # to app function

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# python app.py to start the program
if __name__ == '__main__':
    app.run(debug=True) 
