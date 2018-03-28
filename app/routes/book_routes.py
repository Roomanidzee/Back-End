# -*- coding: utf-8 -*-
from app.services.books_service import get_books_for_user, analyse_book_for_user
from flask import render_template, redirect, url_for, flash, request, session
from app.models import Book
from app import app
import requests


@app.route('/add_genre/<token>', methods=['POST'])
def add_genre_to_user(token):
    user_token = session.get(token)
    genres = request.form.getlist('genre_types')

    genre_api_url = "{0}/{1}".format(app.config['API_URL'], 'genres')
    resp = requests.get(genre_api_url)
    data = resp.json()
    genre_ids = []

    size = len(data)

    for i in range(size):
        genre_ids.append(data[i]['id'])

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

    count1 = 0
    for item in genres:
        count1 += genre_ids.count(item)

    for item in genres:
        add_genre_api_url = "{0}/{1}/{2}/{3}".format(app.config['API_URL'], 'genres', item, user_token)
        requests.post(add_genre_api_url)

    return redirect(url_for('get_books', token=token))


@app.route('/list_my_books/<token>', methods=['GET'])
def get_books(token):
    books, genres = get_books_for_user(token)
    return render_template('my_books.html', user_token=token, books=books, genres=genres)


@app.route('/list_new_books/<token>', methods=['GET'])
def get_new_books(token):
    book_api_url = "{0}/{1}".format(app.config['API_URL'], 'books')

    resp = requests.get(book_api_url)
    data = resp.json()
    books = []
    size = len(data)

    for i in range(size):
        books.append(Book(data[i]['id'], data[i]['name'], data[i]['author'], data[i]['description'], ''))

    return render_template('new_books.html', user_token=token, books=books)


@app.route('/list_recommend_books/<token>', methods=['GET'])
def get_recommend_books(token):
    user_token = session.get(token)
    api_url = "{0}/{1}/{2}".format(app.config['API_URL'], 'books/recommended', user_token)

    resp = requests.get(api_url, {
        'token': user_token
    })
    data = resp.json()
    books = []
    size = len(data)

    for i in range(size):
        books.append(Book(data[i]['id'], data[i]['name'], data[i]['author'], data[i]['description'], ''))

    return render_template('recomend_books.html', user_token=token, books=books)


@app.route('/add_book/<token>', methods=['POST'])
def add_book_to_user(token):
    user_token = session.get(token)
    api_url = "{0}/books/{1}/{2}".format(app.config['API_URL'], request.form['book_id'], user_token)
    requests.post(api_url)

    return redirect(url_for('get_books', token=token))


@app.route('/analyse_book', methods=['GET'])
def analyse_book():
    return render_template("setBook.html")


@app.route('/display_coefficients', methods = ['POST'])
def display_coefficients():

    book_author = request.form['book_author']
    book_title = request.form['book_title']
    book_description = request.form['book_description']
    book_content = request.files['file']

    book = Book('', book_title, book_author, book_description, '')
    coefficients = analyse_book_for_user(book_content)

    return render_template("results.html", book = book, coefficients = coefficients)


@app.route('/send_coefficients', methods = ['POST'])
def send_coefficients():

    result_dict = {}
    result_dict['name'] = request.form['title']
    result_dict['author'] = request.form['author']
    result_dict['description'] = request.form['description']
    result_dict['coef_adventure'] = request.form['adventure']
    result_dict['coef_art'] = request.form['art']
    result_dict['coef_detective'] = request.form['detective']
    result_dict['coef_fantastic'] = request.form['fantastic']
    result_dict['coef_fantasy'] = request.form['fantasy']
    result_dict['coef_love'] = request.form['love']

    print(result_dict)
    api_url = 'https://soul-cloud-api.herokuapp.com/books'
    requests.post(api_url, result_dict)

    return redirect(url_for('index'))
