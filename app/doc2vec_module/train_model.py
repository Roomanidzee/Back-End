from gensim.models import Doc2Vec


def get_model_for_genre(documents : list) -> Doc2Vec:
    model = Doc2Vec(documents, dm=1, alpha=0.9, size=20, min_alpha=0.025)

    print(" ")
    print("Начало обучения: ")
    print(" ")

    for epoch in range(300):
        print('Эпоха #{0}'.format(epoch))
        token_count = sum([len(document) for document in documents])
        model.train(documents, total_examples=token_count, epochs=model.iter)
        model.alpha -= 0.002
        model.min_alpha = model.alpha

    return model
