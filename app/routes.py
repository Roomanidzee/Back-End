# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, session
from app import app
import uuid, requests

from app.models import Book, Genre


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
        return redirect('/')

    string_check = str(uuid.uuid4())
    session[string_check] = data['message']

    return redirect(url_for('get_books', token=data['message']))


@app.route('/logout/<token>')
def logout(token):
    session.pop(token, None)
    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    api_url = "{0}/{1}".format(app.config['API_URL'], 'register')

    r = requests.post(api_url, {
        'email': email,
        'password': password
    })

    data = r.json()

    if data['error_code'] == 0:
        flash('Вы успешно зарегистрировались!')
        string_check = uuid.uuid4()
        session[string_check] = data['message']
        return redirect(url_for('get_books', token=string_check))

    return redirect('/')


@app.route('/add_genre/<token>', methods=['POST'])
def add_genre_to_user(token):
    user_token = session.get(token)
    genres = request.form.getlist('genre_types')

    genre_api_url = "{0}/{1}".format(app.config['API_URL'], 'genres')
    resp = requests.get(genre_api_url)
    data = resp.json()
    genre_ids = [item['id'] for item in data]

    if len(genres) == 0:
        flash('Выберите жанр')
        return redirect('/')

    if len(genres) == 1:
        count = genre_ids.count(genres[0])

        if count == 0:
            flash('Данного жанра нет в нашей базе')
            return redirect('/')

        add_genre_api_url = "{0}/{1}/{2}/{3}".format(app.config['API_URL'], 'genres', genres[0], user_token)
        requests.post(add_genre_api_url)
        return redirect(url_for(get_books, token=token))

    for item in genres:
        count1 = genre_ids.count(item)

        if count1 == 0:
            flash('Некорректно отправлены данные')
            return redirect('/')

    for item in genres:
        add_genre_api_url = "{0}/{1}/{2}/{3}".format(app.config['API_URL'], 'genres', item, user_token)
        requests.post(add_genre_api_url)

    return redirect(url_for(get_books, token=token))


@app.route('/list_my_books/<token>', methods=['GET'])
def get_books(token):
    user_token = session.get(token)
    api_url = "{0}/{1}/{2}".format(app.config['API_URL'], 'books', user_token)
    genre_api_url = "{0}/{1}".format(app.config['API_URL'], 'genres')

    resp = requests.get(api_url)
    data = resp.json()
    print(data)

    resp1 = requests.get(genre_api_url)
    data1 = resp1.json()

    books = []
    genres = []

    size = len(data)
    size1 = len(data1)

    for i in range(size):
        books.append(Book(data[i]['id'], data[i]['name'], data[i]['author'], data[i]['description']))

    for i in range(size1):
        genres.append(Genre(data1[i]['id'], data1[i]['name']))


    return render_template('my_books.html', user_token=token, books=books, genres=genres)


@app.route('/list_new_books/<token>', methods=['GET'])
def get_new_books(token):
    user_token = session.get(token)
    book_api_url = "{0}/{1}", format(app.config['API_URL'], 'books')

    resp = requests.post(book_api_url, {
        'token': user_token
    })
    data = resp.json()
    books = []
    size = len(data)

    for i in range(size):
        books.append(Book(data[i]['id'], data[i]['name'], data[i]['author'], data[i]['description']))

    return render_template('new_books.html', user_token=token, books=books)


@app.route('/list_recommend_books/token', methods=['GET'])
def get_recommend_books(token):
    user_token = session.get(token)
    api_url = "{0}/{1}/{2}".format(app.config['API_URL'], 'books/recommended', user_token)

    resp = requests.post(api_url, {
        'token': user_token
    })
    data = resp.json()
    books = []
    size = len(data)

    for i in range(size):
        books.append(Book(data[i]['id'], data[i]['name'], data[i]['author'], data[i]['description']))

    return render_template('recomend_books.html', user_token=token, books=books)
