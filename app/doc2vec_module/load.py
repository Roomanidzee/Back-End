import os
import re
import codecs

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models.doc2vec import TaggedDocument
from gensim.utils import to_unicode


def get_doc_list(folder_name):
    doc_list = []
    file_list = [folder_name + '\\' + name for name in os.listdir(folder_name) if name.endswith('txt')]
    for file in file_list:
        st = codecs.open(file, 'r', 'utf-8').read()
        doc_list.append(st)
    print('Количество документов в папке {1} - {0} .....'.format(len(file_list), folder_name))
    return doc_list


def get_doc(folder_name):
    doc_list = get_doc_list(folder_name)

    print(" ")
    print("Начинаем обрабатывать тексты из папки {0}...".format(folder_name))

    tokenizer = RegexpTokenizer(r'\w+')
    ru_stop = stopwords.words('russian')
    ru_stop.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])

    paragraph_stemmer = PorterStemmer()
    tagged_doc = []
    texts = []

    for index, i in enumerate(doc_list):
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        stopped_tokens = [i for i in tokens if i not in ru_stop]

        number_tokens = [re.sub(r'[\d]', ' ', i) for i in stopped_tokens]
        number_tokens = ' '.join(number_tokens).split()

        stemmed_tokens = [paragraph_stemmer.stem(i) for i in number_tokens]
        length_tokens = [i for i in stemmed_tokens if len(i) > 1]
        texts.append(length_tokens)

        td = TaggedDocument(to_unicode(str.encode(' '.join(stemmed_tokens))).split(), str(index))
        tagged_doc.append(td)

    print("Тексты из папки {0} обработаны".format(folder_name))
    print(" ")

    return tagged_doc

def get_doc_from_file(file_path):

    print("Загружаем файл {0}".format(file_path))
    file_content = codecs.open(file_path, 'r', 'utf-8').read()
    print("Успешно загружен")

    print(" ")
    print("Начинаем обрабатывать обрабатывать файл {0}...".format(file_path))

    tokenizer = RegexpTokenizer(r'\w+')
    ru_stop = stopwords.words('russian')
    ru_stop.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])

    paragraph_stemmer = PorterStemmer()
    texts = []

    raw = file_content.lower()

    tokens = tokenizer.tokenize(raw)

    stopped_tokens = [i for i in tokens if i not in ru_stop]

    number_tokens = [re.sub(r'[\d]', ' ', i) for i in stopped_tokens]
    number_tokens = ' '.join(number_tokens).split()

    stemmed_tokens = [paragraph_stemmer.stem(i) for i in number_tokens]
    length_tokens = [i for i in stemmed_tokens if len(i) > 1]
    texts.append(length_tokens)

    td = TaggedDocument(to_unicode(str.encode(' '.join(stemmed_tokens))).split(), str(0))

    return td


