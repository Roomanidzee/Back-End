from app.doc2vec_module import load
from app.doc2vec_module.constants import FileConstants
from app.doc2vec_module.train_model import get_model_for_genre

prop_map = {
    'ADVENTURE_BOOK_TRAIN': 'MODEL_ADVENTURE',
    'ART_BOOK_TRAIN': 'MODEL_ART',
    'DETECTIVE_BOOK_TRAIN': 'MODEL_DETECTIVE',
    'FANTASTIC_BOOK_TRAIN': 'MODEL_FANTASTIC',
    'FANTASY_BOOK_TRAIN': 'MODEL_FANTASY',
    'LOVE_BOOK_TRAIN': 'MODEL_LOVE'
}

genre_labels = ['приключений', 'искусства', 'детектива', 'фантастики', 'фэнтези', 'любви']
count = 0

for key, value in prop_map.items():
    print(" ")
    print("Подгружаем свойство {0} с моделью {1}".format(key, value))

    prop = getattr(FileConstants, key)
    model_prop = getattr(FileConstants, value)

    documents = load.get_doc(prop.fget(FileConstants()))
    print("Получено документов для {0} : {1}, тип: {2}".format(genre_labels[count], len(documents), type(documents)))
    print(" ")

    print("Обучаем модель для {0}".format(genre_labels[count]))
    learn_model = get_model_for_genre(documents)
    print("Модель {0} обучена".format(genre_labels[count]))
    print(" ")

    learn_model.save(model_prop.fget(FileConstants()))
    print("Модель {0} сохранена".format(genre_labels[count]))
    print(" ")
    count +=1
