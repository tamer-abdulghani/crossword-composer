import timeit

from constraint import *
from models.direction import *
from models.position import *
class csp:
    def __init__(self, variables, collection):
        self.solver = BacktrackingSolver(forwardcheck=True)# MinConflictsSolver() #
        self.problem = Problem(self.solver)
        self.variables = variables
        self.collection = collection

    def create_variables(self):
        for i,var in enumerate(self.variables):
            list_possible_words = self.collection.dic_len_list[var.length]
            #self.problem.addVariable("var_{}_{}".format(var.start.i,var.start.j) ,list_possible_words)
            #print(list_possible_words[0])
            self.problem.addVariable("var_%d" % i, list_possible_words)
            var.name = "var_%d" % i

    def create_constraints(self):
        nb = 0
        closed = []

        for i, var1 in enumerate(self.variables):
            for j, var2 in enumerate(self.variables):
                c1 = str("var_{}_var_{}".format(i, j))
                c2 = str("var_{}_var_{}".format(j, i))
                if var1 != var2 and self.isCrosswords(var1,var2) and c1 not in closed and c2 not in closed:
                    closed.append(c1)
                    closed.append(c2)
                    if var1.direction == Direction.Across:
                        at = Position(var1.start.i,var2.start.j)
                        self.problem.addConstraint(lambda v1, v2, i1 = at.j - var1.start.j, i2=at.i-var2.start.i : v1[i1] == v2[i2] ,("var_%d" % i, "var_%d" % j))
                    else:

                        at = Position(var2.start.i, var1.start.j)
                        self.problem.addConstraint(lambda v1, v2, i1=at.i - var1.start.i,i2 =at.j-var2.start.j : v1[i1] == v2[i2],
                                                   ("var_%d" % i, "var_%d" % j))
                    nb += 1
        print('number of constraints: ', nb)

        self.print_cons()
        self.problem.addConstraint(AllDifferentConstraint())

    def check(self,v1,v2,index1,index2):
        return v1[index1]==v2[index2]

    def print_cons(self):
        #for c in self.problem._constraints:
            #print(c)
        d,c,vc = self.problem._getArgs()
        '''
        print(d)
        print(c)

        print(vc)
        '''

    def isCrosswords(self, var1, var2):
        if var1.direction == Direction.Across:
            if var1.start.i >= var2.start.i and var1.start.i <= var2.end.i and var2.end.j <= var1.end.j and var2.end.j >= var1.start.j:
                return True
        else:
            if var2.start.i >= var1.start.i and var2.start.i <= var1.end.i and var1.end.j <= var2.end.j and var1.end.j >= var2.start.j:
                return True
        return False

    def get_solutions(self, nb):
        solutions = []

        if type(self.solver) is MinConflictsSolver:
            start = timeit.default_timer()
            solution = self.problem.getSolution()
            stop = timeit.default_timer()
            time_needed = stop - start
            solutions.append(solution)
            return time_needed, solutions
        else:
            print('backtrack solver')
            start = timeit.default_timer()
            iter = self.problem.getSolutionIter()
            count =0
            try:
                while count < nb:
                    solutions.append(next(iter))
                    count+=1
            except StopIteration:
                stop = timeit.default_timer()
                time_needed = stop - start
                return time_needed, solutions

            stop = timeit.default_timer()
            time_needed = stop - start
            return time_needed, solutions

    def get_solution_iter(self):
        return self.problem.getSolutionIter()