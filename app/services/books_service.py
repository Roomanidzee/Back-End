from app.classification_module.numpy_proceed import preprocess_array
from app.classification_module.prepare_ratio import get_model_ratio
from app.doc2vec_module.train_model import get_model_for_genre
from app.doc2vec_module.constants import FileConstants
from app.models import Book, Genre, Coefficients
from sklearn.neural_network import MLPClassifier
from werkzeug.utils import secure_filename
from app.doc2vec_module import load
from gensim.models import Doc2Vec
from flask import session
from app import app
import os, requests
import numpy as np


def get_books_for_user(token : str):
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

    return books, genres

def analyse_book_for_user(file) -> Coefficients:

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
    else:
        raise TypeError

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(15, 6), random_state=1)

    documents = load.get_doc_from_file(file_path)
    check_model = get_model_for_genre([documents])

    prop_list = ["MODEL_ADVENTURE", "MODEL_ART", "MODEL_DETECTIVE", "MODEL_FANTASTIC", "MODEL_FANTASY",
                 "MODEL_LOVE"]
    genre_labels = ['приключения', 'искусство', 'детектив', 'фантастика', 'фэнтези', 'любовь']
    key_labels = ['adventure', 'art', 'detective', 'fantastic', 'fantasy', 'love']
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
    labels = [1, 2, 3, 4, 5, 6]
    result_dict = {}

    clf.fit(np_train_list, labels)

    test = []

    for i in range(6):
        test.append(np.random.randint(200, size = 20))

    temp_var = test.copy()

    for i in range(6):

        print("Расчёт для жанра \"{0}\"".format(genre_labels[counter]))
        check = temp_var.copy()
        print(check)
        print("=========")
        print(check[i])
        check[i] = np.asarray(check_train1)
        test = clf.predict(check)
        result = (np.sum(test) / np.size(test)) / 10
        print(result)
        result_dict[key_labels[i]] = result
        counter +=1

    coefficients = Coefficients(result_dict['love'], result_dict['fantastic'], result_dict['detective'],
                                result_dict['adventure'], result_dict['art'], result_dict['fantasy'])

    return coefficients
