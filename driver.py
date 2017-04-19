from sys import argv
from copy import *
from CSP import *


def AC3(csp):
    queue = list(csp.C)
    while len(queue) > 0:
        constraint = queue.pop(0)
        Xi = constraint[0:2]
        Xj = constraint[3:]
        if revise(csp, Xi, Xj):
            if len(csp.D[Xi]) == 0 or len(csp.D[Xj]) == 0:
                return False
            neighbor = csp.get_neighbors(Xi) - {Xj}
            for Xk in neighbor:
                queue.append(Xk+','+Xi)
    if csp.is_solved():
        result = ''
        for v in sorted(csp.D):
            result += csp.D[v]
        return result
    return False


def revise(csp, Xi, Xj):
    revised = False
    x_domain = copy(csp.D[Xi])
    y_domain = csp.D[Xj]
    for x in x_domain:
        if x == y_domain:
            csp.D[Xi] = csp.D[Xi].replace(x, '')
            revised = True
    return revised


def BTS_search(csp):
    assignment = {}
    return backtrack(assignment, csp)


def backtrack(assignment, csp):
    if csp.is_complete(assignment):
        return assignment
    var = csp.mrv(assignment)
    for value in csp.D[var]:
        if csp.is_consistent(assignment, var, value):
            new_csp = deepcopy(csp)
            assignment[var] = value
            new_csp.D[var] = value
            check = forward_check(new_csp, assignment, var, value)
            if check:
                result = backtrack(assignment, new_csp)
                if result:
                    return result
        del assignment[var]
    return False


def forward_check(csp, assignment, var, value):
    neighbor = csp.get_neighbors(var)
    for n in neighbor:
        if n not in assignment:
            csp.D[n] = csp.D[n].replace(value, '')
            if len(csp.D[n]) == 0:
                return False
    return True


def main():
    input_string = argv[1]
    sudoku = CSP(input_string=input_string)
    output = open('output.txt', 'w')
    if AC3(sudoku):
        # print(AC3(sudoku))
        output.write(AC3(sudoku))
    else:
        assignment = BTS_search(sudoku)
        # print(''.join(assignment[x] for x in sorted(assignment)))
        output.write(''.join(assignment[x] for x in sorted(assignment)))
    output.close()

if __name__ == '__main__':
    main()
