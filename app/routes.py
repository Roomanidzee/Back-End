from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse
from flask import render_template, redirect, url_for, flash, request
from app.models import User
from app import app, db


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        validate_user = User.query.filter_by(username=form.username.data).first()
        if validate_user is None or not validate_user.check_password(form.password.data):
            flash('Неверный логин/пароль')
            return redirect(url_for('login'))
        login_user(validate_user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('my_books')
        return redirect(next_page)
    return render_template('main.html', title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for(''))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        check_user = User(email=form.email.data)
        check_user.set_password(form.password.data)
        db.session.add(check_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('my_books.html', title='Регистрация', form=form)