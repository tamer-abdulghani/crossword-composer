from helpers.dictionary import *
from helpers.gridbuilder import *
from resources.samplegrids import *
from algorithms.a_star import *
from algorithms.csp import *

#building grid object, you can change to GRID_5_6 (use: words2.txt) or GRID_11_11
gb = GridBuilder(GRID_7_7)
gb.build_as_words_list()

#loading dictionary with necessary elements
dictionary = DictionaryCollection("resources/words.txt")
dictionary.load(gb.words_list)

def a_star():
    alg1 = A_Star(gb,dictionary)
    alg1.solve()

def csp_p():

    alg2 = csp(gb.words_list,dictionary)
    alg2.create_variables()
    alg2.create_constraints()

    time, solutions = alg2.get_solutions(100)
    print(time, solutions[0])

if __name__ == '__main__':
    a_star()
    #csp_p()
