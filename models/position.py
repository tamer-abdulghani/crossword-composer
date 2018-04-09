class Position:
    def __init__(self,i,j):
        self.i = i
        self.j = j

    def __hash__(self):
        return hash(str(self.i)+str(self.j))

    def __eq__(self, other):
        return str(self.i) == str(other.i) and str(self.j) == str(other.j)

    def print(self):
        print("({},{})".format(self.i,self.j))