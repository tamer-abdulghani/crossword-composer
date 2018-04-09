import math
from models.direction import *
class Word:
    def __init__(self, dir, start,end):
        self.value = []
        self.start = start
        self.end = end
        self.direction = dir
        self.length = int(math.fabs((start.i - end.i) + (start.j - end.j)) +1)
        self.crossword_at_with = {}#dict()

        # initialize the value with 1 values
        for i in range(self.length):
            self.value.append('1')

    def add_crossword(self, at, newWord ):
        if at not in self.crossword_at_with:
            self.crossword_at_with[at] = newWord

    def set_value(self, newValue):
        self.value = []
        for c in newValue:
            self.value.append(c)

    def get_nb_conflicts(self):
        nb_conflicts = 0

        for at , word in self.crossword_at_with.items():

            if self.direction == Direction.Across:
                k1 = self.start.j
                k2 = word.start.i
                if self.value:
                    if self.value[at.j - k1] != word.value[at.i-k2]:
                        nb_conflicts+=1
            else:
                k1 = self.start.i
                k2 = word.start.j
                if self.value:
                    if self.value[at.i - k1] != word.value[at.j - k2]:
                        nb_conflicts+=1
        return nb_conflicts

    def get_indexes_with(self,at , cross):
        if self.direction == Direction.Across:
            index1 = at.j - self.start.j
            index2 = at.i - cross.start.i
            return index1,index2
        else:
            index1 = at.i - self.start.i
            index2 = at.j - cross.start.j
            return index1,index2

    def is_no_letters_at_intersects(self):
        for at, cross in self.crossword_at_with.items():
            i1,i2 = self.get_indexes_with(at,cross)
            if cross.value[i2] != '1':
                return False
        return True
    def get_letters_at_intersects(self):
        d = dict()
        for at, cross in self.crossword_at_with.items():
            i1,i2 = self.get_indexes_with(at,cross)
            if cross.value[i2] != '1':
                d[i1] = cross.value[i2]
        return d

    def __eq__(self, other):
        return self.start.i == other.start.i and self.start.j == other.start.j and self.end.i == other.end.i and self.end.j == other.end.j

    def print(self):
        print("Word start at (" + str(self.start.i) + "," + str(self.start.j) + ") and end at (" + str(self.end.i) + "," + str(self.end.j) + ")")
