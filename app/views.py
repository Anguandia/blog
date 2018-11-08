from app import app, db, forms
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, PostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    posts = Post.query.join().filter_by(ans_to=None).order_by(Post.timestamp.desc()).all()
    user=current_user
    user = current_user
    form = forms.PostForm(request.form)
    for post in posts:
        answers = Post.query.join().order_by(Post.timestamp.desc()).all()
     #   if answers:
      #      cur = answers[0].id
       # else:
        #    cur = 0
       # next = cur+1
        #quest=Post.query.filter_by(id=form.post.data)
    if form.validate_on_submit():
        post = Post(author = current_user, body=form.post.data, ans_to=form.questionID.data)
        db.session.add(post)
        db.session.commit()
        flash('success')
        return redirect(url_for('index'))
    return render_template('home.html', title='Home', form=form, posts=posts, user=user, answers=answers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(user, remember = form.remember_me.data)
            return redirect(url_for('index'))
    else:
        return render_template('login.html', form=form, title='login')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Sign Up successful')
        return redirect(url_for('index'))
    return render_template('sign_up.html', title='SignUp', form=form)

@app.route('/question', methods=['POST', 'GET'])
def question():
    form = PostForm()
    user = current_user
    if Post.query.all():
        cur = Post.query.all()[-1].id
        next = cur+1
    else:
        next = 1
    if form.validate_on_submit():
        post = Post(id=next, author = current_user, body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('Dear {}, your question has been posted'.format(user.username))
        return redirect(url_for('index'))
    return render_template('question.html', form=form, user=user, title='Question')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
