# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, session

from app.classification_module.numpy_proceed import preprocess_array
from app.classification_module.prepare_ratio import get_model_ratio
from app.doc2vec_module.constants import FileConstants
from app.doc2vec_module.train_model import get_model_for_genre
from app.models import Book, Genre
from app.doc2vec_module import load
from werkzeug.utils import secure_filename
from app import app
import os, requests


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
        books.append(Book(data[i]['id'], data[i]['name'], data[i]['author'], data[i]['description'], data[i]['mark']))

    for i in range(size1):
        genres.append(Genre(data1[i]['id'], data1[i]['name']))

    if len(data) == 0:
        books = None

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


@app.route('/analyse_book', methods = ['GET', 'POST'])
def analyse_book():
    if request.method == 'POST':
      file = request.files['file']

      if file and file.filename.split('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']:
              filename = secure_filename(file.filename)
              file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
              file.save(file_path)

              documents = load.get_doc_from_file(file_path)
              check_model = get_model_for_genre([documents])

              prop_list = ["MODEL_ADVENTURE", "MODEL_ART", "MODEL_DETECTIVE", "MODEL_FANTASTIC", "MODEL_FANTASY",
                           "MODEL_LOVE"]
              genre_labels = ['приключения', 'искусство', 'детектив', 'фантастика', 'фэнтези', 'любовь']
              train_list = []

              for item in prop_list:
                  print("Модель: {0}".format(item))
                  model_prop = getattr(FileConstants, item)
                  model = Doc2Vec.load(model_prop.fget(FileConstants()))
                  train = preprocess_array(get_model_ratio(model))
                  train_list.append(train)
                  print(" ")

              check_train1 = preprocess_array(np.array(check_model.docvecs[str(0)]))
              np_train_list = np.asarray(train_list)

              counter = 0

              labels = []

              for i in range(1, 7):
                  a = np.empty(6)
                  a.fill(i)
                  labels.append(a)

              labels = np.asarray(labels)
              print(np_train_list)
              print("======================")
              print(labels)

              clf.fit(np_train_list, [1, 2, 3, 4, 5, 6])

              test = []

              for i in range(6):
                  test.append(np.random.randint(200, size=20))

              test = np.asarray(test)

              for i in range(6):
                  print("Расчёт для жанра \"{0}\"".format(genre_labels[counter]))
                  check = test.copy()
                  check[counter] = check_train1
                  print(clf.predict(check))

                  counter += 1


      return redirect('имя файла с css')        
