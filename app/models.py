
class Book(object):

    def __init__(self, id, name, author, description):
        self.id = id
        self.name = name
        self.author = author
        self.description = description

    def __repr__(self):
        return "Book({0}, {1}, {2}, {3})".format(self.id, self.name, self.author, self.description)

class Genre(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Genre({0}, {1})".format(self.id, self.name)
