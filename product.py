from pysat.solvers import Glucose3
import math
import time

def exact_one(variables: []):
    global variables_count1

    clauses.append(variables)
    p = math.ceil(math.sqrt(len(variables)))
    q = math.ceil(len(variables) / p)

    fromIndex = variables_count + variables_count1
    variables_count1 += p + q

    for i in range(1, p):
        for j in range(i + 1, p + 1):
            clauses.append([-(fromIndex + i), -(fromIndex + j)])

    for i in range(1, q):
        for j in range(i + 1, q + 1):
            clauses.append([-(fromIndex + p + i), -(fromIndex + p + j)])

    for i, var in enumerate(variables):
        r = int(i / q) + 1
        c = i % q + 1
        clauses.append([-var, fromIndex + r])
        clauses.append([-var, fromIndex + p + c])


def encode(i: int, j: int, k: int):
    return (i - 1) * size * size + (j - 1) * size + k


def handle_cell_constraint():
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            variables = [encode(i, j, k) for k in range(1, size + 1)]
            exact_one(variables)


def handle_row_constraint():
    for i in range(1, size + 1):
        for k in range(1, size + 1):
            variables = [encode(i, j, k) for j in range(1, size + 1)]
            exact_one(variables)


def handle_column_constraint():
    for j in range(1, size + 1):
        for k in range(1, size + 1):
            variables = [encode(i, j, k) for i in range(1, size + 1)]
            exact_one(variables)


def handle_block_constraint():
    for k in range(1, size + 1):
        for ii in range(1, block + 1):
            for jj in range(1, block + 1):
                variables = [encode(i, j, k) for i in
                             range((ii - 1) * block + 1, ii * block + 1) for j in
                             range((jj - 1) * block + 1, jj * block + 1)]
                exact_one(variables)


def add_clues():
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            k = clues[i - 1][j - 1]
            if k and k.isdigit():
                clauses.append([encode(i, j, int(k))])


def sat_solver():
    g = Glucose3()
    for c in clauses:
        g.add_clause(c)

    satisfiable = g.solve()
    if not satisfiable:
        return None, satisfiable

    result = g.get_model()[:variables_count]
    result = [next(k + 1 for k, l in enumerate(result[i:i + size]) if l > 0) for i in
              range(0, len(result), size)]
    result = [result[i:i + size] for i in range(0, len(result), size)]
    return result, satisfiable


def solve():
    startTime = time.time()
    handle_cell_constraint()
    handle_row_constraint()
    handle_column_constraint()
    handle_block_constraint()
    numberOfClause = len(clauses)

    print()
    add_clues()

    result, satisfiable = sat_solver()
    numberOfClauseTotal = len(clauses)
    stopTime = time.time()
    return {
        'satisfiable': satisfiable,
        'result': result,
        'numberOfVariable': variables_count + variables_count1,
        'numberOfClause': numberOfClause,
        'numberOfClauseTotal': numberOfClauseTotal,
        'timeInSecond': stopTime - startTime}

    # for row in result:
    #     print(row)


# block = 3
# size = block * block
# variables_count = size ** 3
# variables_count1 = 0
#
# fileName = "sudoku_16x16.txt"
# clues = []
# clauses = []
#
# with open(fileName, "r") as f:
#     for line in f.readlines():
#         if not line.strip():
#             continue
#         clue = line.strip().split(",")
#         clues.append(clue)
#
# solve()
if __name__ == '__main__':
    block = 5
    size = block * block
    variables_count = size ** 3
    variables_count1 = 0
    clues = []
    clauses = []
    input = []

    mode = 1

    with open("sudoku_25x25.txt", "r") as f:
        for line in f.readlines():
                if not line.strip():
                    continue
                clue = line.strip().split(",")
                clues.append(clue)

    result = solve()

    print(result)
    if (result['satisfiable']):
        for row in result['result']:
            print(row)
