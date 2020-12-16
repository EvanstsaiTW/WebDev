# users/views.py
from flask import render_template, redirect, request, url_for, flash, abort, Blueprint
from flask_login import login_user,login_required,logout_user, current_user
from projectKanpai import db 
# init grab db
from projectKanpai.models import User, BlogPost
from projectKanpai.users.forms import RegistrationForm, LoginForm, UpdateUserForm

#users view
users = Blueprint('users', __name__)

# register user
@users.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        # one second
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

 
#login user
@users.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    a = User.query.filter_by().all()
    for i in a:
        print(i.username)
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()  
        print("--------here---------")   
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
                next = url_for('core.index') # to app function

            return redirect(next)
    print("not login")   
    return render_template('login.html', form=form)

#logout user
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))
#account user's list of post -- dashboard
@users.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()
    user = User.query.filter_by(username = current_user.username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user)
    number = len(blog_posts.all())
    # update
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', form=form, user = user, blog_posts=blog_posts, num = number)


# user's list of blog posts
@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()
    ).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)



