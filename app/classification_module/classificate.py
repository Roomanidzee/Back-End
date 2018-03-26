from app.classification_module.prepare_ratio import get_model_ratio
from app.classification_module.numpy_proceed import preprocess_array
from app.doc2vec_module.train_model import get_model_for_genre
from app.doc2vec_module.constants import FileConstants
from sklearn.neural_network import MLPClassifier
from gensim.models import Doc2Vec
from app.doc2vec_module import load
from pathlib import Path
import numpy as np


# Пример работы для отдельных книг
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(15, 6), random_state=1)


#path_to_check1 = Path(__file__).parents[1].joinpath('books/test_book/Дети Капитана Гранта.txt')
#documents1 = load.get_doc_from_file(str(path_to_check1))

path_to_check1 = Path(__file__).parents[1].joinpath('books/test_book/Гарри Поттер и Дары Смерти.txt')
documents1 = load.get_doc_from_file(str(path_to_check1))

print("Получаем модель для книги")
print("")
check_model1 = get_model_for_genre([documents1])
#check_model2 = get_model_for_genre([documents2])

print("Начинаем подгружать модели по жанрам")
print(" ")

prop_list = ["MODEL_ADVENTURE", "MODEL_ART", "MODEL_DETECTIVE", "MODEL_FANTASTIC", "MODEL_FANTASY", "MODEL_LOVE"]
genre_labels = ['приключения', 'искусство', 'детектив', 'фантастика', 'фэнтези', 'любовь']
train_list = []

for item in prop_list:
    print("Модель: {0}".format(item))
    model_prop = getattr(FileConstants, item)
    model = Doc2Vec.load(model_prop.fget(FileConstants()))
    train = preprocess_array(get_model_ratio(model))
    train_list.append(train)
    print(" ")

check_train1 = preprocess_array(np.array(check_model1.docvecs[str(0)]))
np_train_list = np.asarray(train_list)

counter = 0
counter1 = 0

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
    test.append(np.random.randint(200, size = 20))

test = np.asarray(test)

for i in range(6):
    print("Расчёт для жанра \"{0}\"".format(genre_labels[counter]))
    check = test.copy()
    check[counter] = check_train1
    print(clf.predict(check))

    counter +=1
