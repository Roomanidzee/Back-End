from app.classification_module.numpy_proceed import get_vectors_by_category
from gensim.models import Doc2Vec
import numpy as np

def get_model_ratio(model : Doc2Vec):

    print("Подсчитываем коэффициенты модели...")

    result = 0

    for i in range(0, 4):
        temp_list = get_vectors_by_category(model, i)
        result = np.add(result, temp_list)

    print("Подсчитано")

    return result