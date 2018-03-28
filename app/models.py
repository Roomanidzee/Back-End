
class Book(object):

    def __init__(self, id, name, author, description, mark):
        self.id = id
        self.name = name
        self.author = author
        self.description = description
        self.mark = mark

    def __repr__(self):
        return "Book({0}, {1}, {2}, {3})".format(self.id, self.name, self.author, self.description, self.mark)

class Genre(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "Genre({0}, {1})".format(self.id, self.name)

class Coefficients(object):

    def __init__(self, coef_love, coef_fantastic, coef_detective, coef_adventure, coef_art, coef_fantasy):
        self.coef_love = coef_love
        self.coef_fantastic = coef_fantastic
        self.coef_detective = coef_detective
        self.coef_adventure = coef_adventure
        self.coef_art = coef_art
        self.coef_fantasy = coef_fantasy

    def __repr__(self):
        return "Coefficients(love = {0}, fantastic = {1}, detective = {2}, adventure = {3}, art = {4}, " \
               "fantasy = {5}".format(self.coef_love, self.coef_fantastic, self.coef_detective, self.coef_adventure,
                                      self.coef_art, self.coef_fantasy)
