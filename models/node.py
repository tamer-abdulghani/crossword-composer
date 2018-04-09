from helpers.gridbuilder import *
class Node(object):
    def __init__(self, list):
        self.words_list = list
        self.parent = None
        self.active_word = None
        self.g = 0
        self.h = 0
        self.f = 0

    def add_or_update_word_value(self,word_to_change, value):
        for w in self.words_list:
            if w == word_to_change:
                print("words are equal")
                w.set_value(value)

    def is_goal(self):
        nb_conflicts,nb_empty_values  = self.get_nb_conflicts_empty_words()
        if nb_conflicts == 0 and nb_empty_values == 0 :
            return True

        return False

    def get_nb_conflicts_empty_words(self):
        nb_conflicts = 0
        nb_empty_values = 0
        for word in self.words_list:
            nb_conflicts += word.get_nb_conflicts()
            if not word.value:
                nb_empty_values += 1

        return nb_conflicts, nb_empty_values

    def contains_word(self, value):
        for word in self.words_list:
            if ''.join(word.value) == value:
                return True
        return False

    def __gt__(self, other):
        return self.f >= other.f

    def __lt__(self, other):
        return self.f < other.f

