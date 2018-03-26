from sklearn.neural_network import MLPClassifier
from app.classification_module.prepare_ratio import get_model_ratio
from sklearn.metrics import classification_report as clsr
from app.classification_module.numpy_proceed import preprocess_array
from app.doc2vec_module.train_model import get_model_for_genre
from app.doc2vec_module.constants import FileConstants
from gensim.models import Doc2Vec
from app.doc2vec_module import load
from pathlib import Path
import numpy as np
import requests

def send_book(file_path: str, name: str, author: str, description: str) -> dict:
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                        hidden_layer_sizes=(15, 6), random_state=1)

    doc = load.get_doc_from_file(file_path)

    print("Получаем модель для книги")
    print("")
    check_model = get_model_for_genre([doc])

    print("Начинаем подгружать модели по жанрам")
    print(" ")

    prop_list = ["MODEL_ADVENTURE", "MODEL_ART", "MODEL_DETECTIVE", "MODEL_FANTASTIC", "MODEL_FANTASY", "MODEL_LOVE"]
    genre_coefs = ['coef_adventure', 'coef_art', 'coef_detective', 'coef_fantastic', 'coef_fantasy', 'coef_love']
    train_list = []

    result_dict = {}

    for item in prop_list:
        print("Модель: {0}".format(item))
        model_prop = getattr(FileConstants, item)
        model = Doc2Vec.load(model_prop.fget(FileConstants()))
        train = preprocess_array(get_model_ratio(model))
        train_list.append(train)
        print(" ")

    result_dict['name'] = name
    result_dict['author'] = author
    result_dict['description'] = description

    check_train = preprocess_array(np.array(check_model.docvecs[str(0)]))
    np_train_list = np.asarray(train_list)
    genre_labels = ['приключения', 'искусство', 'детектив', 'фантастика', 'фэнтези', 'любовь']

    counter = 0
    fix = [1, 2, 3, 4, 5, 6]

    clf.fit(np_train_list, fix)

    test = []

    for i in range(6):
        test.append(np.random.randint(200, size=20))

    test = np.asarray(test)

    for i in range(6):
        print("Расчёт для жанра \"{0}\"".format(genre_labels[counter]))
        check = test.copy()
        check[counter] = check_train
        temp = clf.predict(check)
        print(clsr(fix, temp))
        print((np.sum(temp) / np.size(temp)) / 10)

        counter += 1

    return result_dict

adventure_base_path = Path(__file__).parents[1].joinpath('books/train_books/adventure')
art_base_path = Path(__file__).parents[1].joinpath('books/train_books/art')
detective_base_path = Path(__file__).parents[1].joinpath('books/train_books/detective')
fantastic_base_path = Path(__file__).parents[1].joinpath('books/train_books/fantastic')
fantasy_base_path = Path(__file__).parents[1].joinpath('books/train_books/fantasy')
love_base_path = Path(__file__).parents[1].joinpath('books/train_books/love')

grant = "{0}\\{1}".format(str(adventure_base_path), "Дети капитана Гранта.txt")
blad = "{0}\\{1}".format(str(adventure_base_path), "Одиссея Капитана Блада.txt")
island = "{0}\\{1}".format(str(adventure_base_path), "Остров сокровищ.txt")
twist = "{0}\\{1}".format(str(adventure_base_path), "Приключения Оливера Твиста.txt")
duma = "{0}\\{1}".format(str(adventure_base_path), "Три мушкетёра.txt")

action_is_form = "{0}\\{1}".format(str(art_base_path), "Действие есть форма.txt")
lunch = "{0}\\{1}".format(str(art_base_path), "Завтрак у Sotheby's.txt")
notes = "{0}\\{1}".format(str(art_base_path), "Записки и выписки.txt")
bridge = "{0}\\{1}".format(str(art_base_path), "Мост через бездну.txt")

sokol = "{0}\\{1}".format(str(detective_base_path), "Мальтийский сокол.txt")
dost = "{0}\\{1}".format(str(detective_base_path), "Преступление и наказание.txt")
ghost = "{0}\\{1}".format(str(detective_base_path), "Призрак оперы.txt")
dog = "{0}\\{1}".format(str(detective_base_path), "Собака Баскервилей.txt")
morg = "{0}\\{1}".format(str(detective_base_path), "Убийство на улице Морг.txt")

stop = "{0}\\{1}".format(str(fantastic_base_path), "Автостопом по галактике.txt")
water = "{0}\\{1}".format(str(fantastic_base_path), "Двадцать тысяч лье под водой.txt")
mars = "{0}\\{1}".format(str(fantastic_base_path), "Марсианские хроники.txt")
flib = "{0}\\{1}".format(str(fantastic_base_path), "Флибустьер.txt")
world = "{0}\\{1}".format(str(fantastic_base_path), "Этот мир придуман не нами.txt")

alisa = "{0}\\{1}".format(str(fantasy_base_path), "Алиса в стране чудес.txt")
dragon = "{0}\\{1}".format(str(fantasy_base_path), "Время для драконов.txt")
garri = "{0}\\{1}".format(str(fantasy_base_path), "Гарри Поттер и Дары Смерти.txt")
lake = "{0}\\{1}".format(str(fantasy_base_path), "Озеро.txt")
fairytale = "{0}\\{1}".format(str(fantasy_base_path), "Сказка о силе.txt")

time = "{0}\\{1}".format(str(love_base_path), "Время жить и время умирать.txt")
oranges = "{0}\\{1}".format(str(love_base_path), "Любовь к трём апельсинам.txt")
crasy = "{0}\\{1}".format(str(love_base_path), "Любовь у помешанных.txt")
friends = "{0}\\{1}".format(str(love_base_path), "Три товарища.txt")
wind = "{0}\\{1}".format(str(love_base_path), "Унесённые ветром.txt")

api_url = 'https://soul-cloud-api.herokuapp.com/books'

files_dict = {
    grant : ['Дети капитана Гранта', 'Жюль Верн', 'История о поиске и самоотверженности'],
    blad : ['Одиссея Капитана Блада', 'Рафаэль Сабатини', 'Храбрый капитан - весёлые приключения'],
    island : ['Остров сокровищ', 'Роберт Луис Стивенсон', 'Все ищут сокровища старого пирата. Кто же их найдёт?'],
    twist : ['Приключения Оливера Твиста', 'Чарльз Диккенс', 'Печальная история сироты в Англии'],
    duma : ['Три мушкетёра', 'Александр Дюма', 'Рассказ на века'],

    action_is_form : ['Действие есть форма', 'Келлер Истерлинг', 'Популярное руководство к действию'],
    lunch : ['Завтрак у Sotheby\'s', 'Филип Хук', 'Вам это точно понравится'],
    notes : ['Записки и выписки', 'Михаил Гаспаров', 'Поможет в классификации окружающего мира'],
    bridge : ['Мост через бездну', 'Паола Волкова', 'Известная книга Паолы Волковой'],

    sokol : ['Мальтийский сокол', 'Дэшил Хаммет', 'Детективная история со множеством сюжетных поворотов'],
    dost : ['Преступление и наказание', "Фёдор Достоевский", 'Известная история на все времена'],
    ghost : ['Призрак оперы', 'Гастон Леру', ''],
    dog : ['Собака Баскервилей', 'Артур Конан Дойл', ''],
    morg : ['Убийство на улице Морг', 'Эдгар Аллан По', ''],

    stop : ['Автостопом по галактике', 'Дуглас Адамс', ''],
    water : ['Двадцать тысяч льё под водой', 'Жюль Верн', ''],
    mars : ['Марсианские хроники', 'Рэй Брэдбери', ''],
    flib : ['Флибустьер', 'Михаил Ахманов', ''],
    world : ['Этот мир придуман не нами', 'Шумил Павел', ''],

    alisa : ['Алиса в стране чудес', 'Льюис Кэрролл', ''],
    dragon : ['Время для драконов', 'Локхард Драко', ''],
    garri : ['Гарри Поттер и Дары Смерти', 'Джоан Роулинг', ''],
    lake : ['Озеро', 'Леонид Кудрявцев', ''],
    fairytale : ['Сказка о силе', 'Карлос Кастанеда', ''],

    time : ['Время жить и время умирать','Эрих Мария Ремарк', ''],
    oranges : ['Любовь к трём апельсинам','Карло Гоцци', ''],
    crasy : ['Любовь у помешанных','Чезаре Ломброзо', ''],
    friends : ['Три товарища','Эрих Мария Ремарк', ''],
    wind : ['Унесённые ветром','Маргарет Митчелл', '']

}

print("Начинаем отправлять данные")
print(" ")

counter = 0

for key, value in files_dict.items():

    if counter == 2:
        break

    temp = value
    print("Отправляем книгу {0} автора {1}".format(temp[0], temp[1]))
    print(" ")
    dict = send_book(key, temp[0], temp[1], temp[2])
    print(dict)
    #r = requests.post(api_url, dict)
    print(" ")
    counter += 1
