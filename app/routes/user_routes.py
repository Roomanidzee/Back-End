# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, session
from app import app
import uuid, requests


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    api_url = app.config['API_URL'] + '/login'

    r = requests.post(api_url, {
        'email': email,
        'password': password
    })

    data = r.json()

    if data['error_code'] == 2:
        flash('Неверный логин/пароль')
        return redirect(url_for('index'))

    string_check = str(uuid.uuid4())
    session[string_check] = data['message']

    return redirect(url_for('get_books', token=string_check))


@app.route('/logout/<token>')
def logout(token):
    session.pop(token, None)
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    if not (password == password2):
        flash('Пароли не совпадают. Введите их ещё раз')
        return redirect(url_for('index'))

    api_url = "{0}/{1}".format(app.config['API_URL'], 'registration')

    r = requests.post(api_url, {
        'email': email,
        'password': password
    })

    data = r.json()
    print(data)

    if data['error_code'] == 3:
        flash('Данный логин занят. Зарегистрируйтесь с другим.')
        return redirect(url_for('index'))

    string_check = uuid.uuid4()
    session[string_check] = data['message']
    return redirect(url_for('get_books', token=string_check))
