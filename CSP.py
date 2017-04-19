
rows = ['A','B','C','D','E','F','G','H','I']


class CSP:
    def __init__(self, input_string):
        self.V = []
        self.D = {}
        self.C = set()
        self.init(input_string)

    def init(self, input_string):
        for i in range(9):
            for j in range(1, 10):
                n = 9 * i + j - 1
                self.V.append(rows[i]+str(j))
                if input_string[n] == '0':
                    domain = '123456789'
                else:
                    domain = input_string[n]
                self.D[rows[i]+str(j)] = domain
        self.build_constraints()

    def build_constraints(self):
        for v in self.V:
            neighbor = self.get_neighbors(v)
            for n in neighbor:
                self.C.add(v+','+n)

    def get_neighbors(self, var):
        neighbor = set()
        index = self.V.index(var)
        row = index // 9
        col = index % 9
        for i in range(1, 10):
            n_row = rows[row] + str(i)
            n_col = rows[i-1] + str(col+1)
            if n_row != var:
                neighbor.add(n_row)
            if n_col != var:
                neighbor.add(n_col)
        c_row = (row // 3) * 3
        c_col = (col // 3) * 3
        for i in range(c_row, c_row+3):
            for j in range(c_col, c_col+3):
                n_cube = rows[i] + str(j+1)
                if n_cube != var:
                    neighbor.add(n_cube)
        return neighbor

    def is_solved(self):
        solved = True
        for d in self.D.values():
            if len(d) > 1:
                solved = False
        return solved

    def mrv(self, assignment):
        unassigned_var = [x for x in self.D if x not in assignment]
        var = min(unassigned_var, key=lambda d: len(self.D[d]))
        return var

    def is_complete(self, assignment):
        complete = True
        for x in self.V:
            if x not in assignment:
                complete = False
        return complete

    def is_consistent(self, assignment, var, value):
        neighbor = self.get_neighbors(var)
        consistent = True
        for n in neighbor:
            if n in assignment and assignment[n] == value:
                consistent = False
        return consistent
