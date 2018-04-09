import timeit
import copy
import math

from models.direction import Direction
from models.node import Node
from random import shuffle


class A_Star:
    def __init__(self, gb, collection):
        self.gb = gb
        self.collection = collection
        self.opened = dict()
        self.closed = set()
        self.starting_solver = StartingSolver.MostIntersects
        self.process_solver = ProcessSolver.MostIntersectsAnotherWord
        self.heuristic = AStarHeuristic.Basic
        self.guicontroller = None

        self.numberofpushes = 0

    def solve(self):
        start = timeit.default_timer()
        self.add_starting_nodes()

        while len(self.opened) > 0:
            print('stack size (unique f values): ', len(self.opened))
            f, current = self.stack_pop()
            self.closed.add(current)

            if current.is_goal():
                stop = timeit.default_timer()
                print('Done! \n Time needed',stop - start )
                timeneeded = stop - start
                soltion_as_grid = self.gb.get_full_grid_by_list_of_words(current.words_list)
                print('number of nodes generated: ', self.numberofpushes)
                return timeneeded,soltion_as_grid
            else:
                if self.guicontroller:
                    self.guicontroller.render_grid_in_gui(self.gb.get_full_grid_by_list_of_words(current.words_list))
                else:
                    self.gb.print_grid(self.gb.get_full_grid_by_list_of_words(current.words_list))

            children = self.get_children(current)

            for child in children:
                if child not in self.closed:
                    if self.is_in_stack(child):
                        print('hi')
                        if child.g > current.g + 10:
                            self.update_node(child, current)
                    else:
                        self.update_node(child, current)
                        self.stack_push(child)

        print('No solution found!!!')
        stop = timeit.default_timer()
        timeneeded = stop - start
        return timeneeded, None

    def stack_push(self, child):
        if child.f not in self.opened:
            self.opened[child.f] = []
        self.opened[child.f].append(child)
        self.numberofpushes += 1

    def stack_pop(self):
        minimum_f = max(self.opened, key=self.opened.get)
        print('size of stack f {},{}'.format(minimum_f,len(self.opened[minimum_f])))
        node = self.opened[minimum_f][-1]
        self.opened[minimum_f].remove(node)
        if len(self.opened[minimum_f]) == 0:
            self.opened.pop(minimum_f,None)

        return node.f,node

    def is_in_stack(self,child):
        if child.f in self.opened:
            if child in self.opened[child.f]:
                return True
        return False

    def update_node(self,new_node,current):
        # here i should calculate nodes best option to go with
        # for example: the node that has minimum number in dictionary
        new_node.parent = current
        new_node.g = current.g + 10000
        new_node.h = self.get_heuristic(new_node)
        new_node.parent = current
        new_node.f = new_node.h + new_node.g

    def get_heuristic(self, newnode):
        nb_poss_words_at_crosses = 0
        for at, cross in newnode.active_word.crossword_at_with.items():
            index1, index2 = newnode.active_word.get_indexes_with(at, cross)
            letter = newnode.active_word.value[index1]
            count_in_dic = self.collection.get_count_index_char_length(index2,letter,cross.length)
            if count_in_dic == 0:
                return 0
            nb_poss_words_at_crosses += count_in_dic
        return nb_poss_words_at_crosses

    def get_children(self,current):
        nodes = []
        # here we use the dictionary to get all words that have specific length
        if self.starting_solver == StartingSolver.LeastPossibilites:
            if self.process_solver == ProcessSolver.LeastPossibilitesActiveWord:
                letter, index, new_word = self.get_new_grid_word(current)
                if new_word is None:
                    min = 1000000
                    for word in current.words_list:
                        if word.value[0] == '1':
                            count = len(self.collection.dic_len_list[word.length])
                            if count < min:
                                min = count
                                current.active_word = word
                                new_word = word
                if new_word is None:
                    return []

                list_possible_new_words = self.collection.get_list_index_char_length(index,letter,new_word.length)

                for w in list_possible_new_words:
                    if not current.contains_word(w):
                        newnode = self.new_node_with_new_word(current,new_word,w)
                        if newnode not in self.closed:
                            nodes.append(newnode)
            elif self.process_solver == ProcessSolver.LeastPossibilitesAnotherWord:
                new_word = self.get_new_grid_word(current)
                # two cases here: the word is completely empty or there are some letters at the intersects
                if new_word.is_no_letters_at_intersects():
                    list_possible_new_words = self.collection.dic_len_list[new_word.length]
                    for w in list_possible_new_words:
                        if not current.contains_word(w):
                            newnode = self.new_node_with_new_word(current, new_word, w)
                            if newnode not in self.closed:
                                nodes.append(newnode)
                    return nodes
                else:
                    intersects_letters = new_word.get_letters_at_intersects()
                    list_possible_new_words = []
                    index = list(intersects_letters.keys())[0]
                    letter = intersects_letters[index]
                    intersects_letters.pop(index, None)
                    list_possible_new_words = self.collection.get_list_index_char_length(index, letter, new_word.length)

                    for index, letter in intersects_letters.items():
                        list_possible_new_words = list(filter(lambda x: x[index] == letter, list_possible_new_words))

                    for w in list_possible_new_words:
                        if not current.contains_word(w):
                            newnode = self.new_node_with_new_word(current, new_word, w)
                            if newnode not in self.closed:
                                nodes.append(newnode)
        elif self.starting_solver == StartingSolver.MostIntersects:
            if self.process_solver == ProcessSolver.MostIntersectsAnotherWord:
                new_word = self.get_new_grid_word(current)
                # two cases here: the word is completely empty or there are some letters at the intersects
                if new_word.is_no_letters_at_intersects():
                    list_possible_new_words = self.collection.dic_len_list[new_word.length]
                    for w in list_possible_new_words:
                        if not current.contains_word(w):
                            newnode = self.new_node_with_new_word(current, new_word, w)
                            if newnode not in self.closed:
                                nodes.append(newnode)
                    return nodes
                else:
                    intersects_letters = new_word.get_letters_at_intersects()
                    list_possible_new_words = []
                    index = list(intersects_letters.keys())[0]
                    letter = intersects_letters[index]
                    intersects_letters.pop(index,None)
                    list_possible_new_words = self.collection.get_list_index_char_length(index, letter, new_word.length)

                    for index,letter in intersects_letters.items():
                        list_possible_new_words = list(filter(lambda x: x[index] == letter, list_possible_new_words))

                    for w in list_possible_new_words:
                        if not current.contains_word(w):
                            newnode = self.new_node_with_new_word(current, new_word, w)
                            if newnode not in self.closed:
                                nodes.append(newnode)
            elif self.process_solver == ProcessSolver.MostIntersectsActiveWord:
                letter, index, new_word = self.get_new_grid_word(current)
                if new_word is None:
                    return []
                list_possible_new_words = self.collection.get_list_index_char_length(index, letter, new_word.length)

                for w in list_possible_new_words:
                    if not current.contains_word(w):
                        newnode = self.new_node_with_new_word(current, new_word, w)
                        if newnode not in self.closed:
                            nodes.append(newnode)

        return nodes

    def new_node_with_new_word(self,current, active_word, w_value):
        new_copy = copy.deepcopy(current)
        for w in new_copy.words_list:
            if self.do_have_same_positions (w, active_word):
                w.set_value(w_value)
                new_copy.active_word = w

        new_copy.f = self.get_heuristic(new_copy)
        return new_copy

    def do_have_same_positions(self,w,new_word):
        if w.start == new_word.start and w.end == new_word.end:
            return True
        return False

    def add_starting_nodes(self):
        if self.starting_solver == StartingSolver.LeastPossibilites:
            min = 1000000
            initial_node = Node(self.gb.words_list)
            # find the word with minimum possibilities in dictionary
            for word in initial_node.words_list:
                count = len(self.collection.dic_len_list[word.length])
                if count < min:
                    min = count
                    initial_node.active_word = word
            print("initial node active word length: {}",initial_node.active_word.length)

            possible_words = self.collection.dic_len_list[initial_node.active_word.length]
            for w in possible_words:
                newnode = self.new_node_with_new_word(initial_node,initial_node.active_word,w)
                self.stack_push(newnode)
        elif self.starting_solver == StartingSolver.MostIntersects:

            new_word = None
            max = 0
            initial_node = Node(self.gb.words_list)
            for word in initial_node.words_list:
                if word.value[0] == '1' and len(word.crossword_at_with) > max:
                    max = len(word.crossword_at_with)
                    new_word = word
                    print('max=', word.length)
            initial_node.active_word = new_word

            possible_words = self.collection.dic_len_list[initial_node.active_word.length]
            for w in possible_words:
                newnode = self.new_node_with_new_word(initial_node, initial_node.active_word, w)
                self.stack_push(newnode)


    def get_new_grid_word(self,current):
        if self.process_solver == ProcessSolver.LeastPossibilitesActiveWord:
            new_word = None
            min = 1000000
            letter = ''
            index = 0
            print('current Active: ', current.active_word.value, '-----------?????????')
            for at, word in current.active_word.crossword_at_with.items():
                # Don't check filled words already, ToDo: remove the values somewhere else when going back!

                print(word.value)
                if word.value[0] == '1':
                    word_count_in_dic = len(self.collection.dic_len_list[word.length])
                    if word_count_in_dic < min:
                        min = word_count_in_dic
                        new_word = word
                        if current.active_word.direction == Direction.Across:
                            k1 = current.active_word.start.j
                            k2 = word.start.i
                            letter = current.active_word.value[at.j - k1]
                            index = at.i - k2
                            print('oldWord: ({},{}), NewWord: ({},{}), At: ({},{})'.format(current.active_word.start.i,
                                                                                           current.active_word.start.j,
                                                                                           word.start.i, word.start.j, at.i,
                                                                                           at.j))
                        else:
                            k1 = current.active_word.start.i
                            k2 = word.start.j
                            letter = current.active_word.value[at.i - k1]
                            index = at.j - k2
                            print('oldWord: ({},{}), NewWord: ({},{}), At: ({},{})'.format(current.active_word.start.i,
                                                                                           current.active_word.start.j,
                                                                                           word.start.i,
                                                                                           word.start.j, at.i, at.j
                                                                                           ))
            # print (letter)
            # print (index)
            # print('new Selected: ', new_word.value, '-----------?????????')

            return letter, index, new_word
        elif self.process_solver == ProcessSolver.LeastPossibilitesAnotherWord:
            min = 1000000
            for word in current.words_list:
                if word.value[0] == '1':
                    count = len(self.collection.dic_len_list[word.length])
                    if count < min:
                        min = count
                        current.active_word = word
            return current.active_word
        elif self.process_solver == ProcessSolver.MostIntersectsActiveWord:
            new_word = None
            max = 0
            letter = ''
            index = 0
            print('current Active: ', current.active_word.value, '-----------?????????')

            for at, cross in current.active_word.crossword_at_with.items():
                if cross.value[0] == '1' and len(cross.crossword_at_with) > max:
                    max = len(cross.crossword_at_with)
                    new_word = cross
                    i1,i2 = current.active_word.get_indexes_with(at,cross)
                    letter = current.active_word.value[i1]
                    index = i2
                    print('max=', cross.length)
            current.active_word = new_word
            return letter, index, new_word

        elif self.process_solver == ProcessSolver.MostIntersectsAnotherWord:
            new_word = None
            max = 0
            for word in current.words_list:
                if word.value[0] == '1' and len(word.crossword_at_with) > max:
                    max = len(word.crossword_at_with)
                    new_word = word
                    print('max=', word.length)
            current.active_word = new_word
            return current.active_word


class StartingSolver:
    MostIntersects = 1,
    LeastPossibilites = 2

class ProcessSolver:
    MostIntersectsActiveWord= 1,
    MostIntersectsAnotherWord = 2,

    LeastPossibilitesActiveWord = 3
    LeastPossibilitesAnotherWord = 4

class AStarHeuristic:
    Basic = 1,
    Second = 2