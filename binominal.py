from pysat.solvers import Glucose3
import time


def exactOneConstraint(variables: []):
    global customVariables
    clauses.append(variables)

    # Binomial encoding
    for i in range(len(variables) - 1):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])


def exactOneBinomial(variables: []):
    newClauses = [variables]
    for i in range(len(variables) - 1):
        for j in range(i + 1, len(variables)):
            newClauses.append([-variables[i], -variables[j]])
    return newClauses


def var(i: int, j: int, k: int):
    return (i - 1) * size * size + (j - 1) * size + k


def satSolving():
    g = Glucose3()
    for c in clauses:
        g.add_clause(c)

    satisfiable = g.solve()
    if not satisfiable:
        return None, satisfiable

    result = g.get_model()[:defaultVariables]
    result = [next(k + 1 for k, l in enumerate(result[i:i + size]) if l > 0) for i in
              range(0, len(result), size)]
    result = [result[i:i + size] for i in range(0, len(result), size)]
    return result, satisfiable


def solve():
    startTime = time.time()
    # Cell constraint
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            variables = [var(i, j, k) for k in range(1, size + 1)]
            exactOneConstraint(variables)

    # Row constraint
    for i in range(1, size + 1):
        for k in range(1, size + 1):
            variables = [var(i, j, k) for j in range(1, size + 1)]
            exactOneConstraint(variables)

    # Column constraint
    for j in range(1, size + 1):
        for k in range(1, size + 1):
            variables = [var(i, j, k) for i in range(1, size + 1)]
            exactOneConstraint(variables)

    # Block constraint
    for k in range(1, size + 1):
        for ii in range(1, blockSize + 1):
            for jj in range(1, blockSize + 1):
                variables = [var(i, j, k) for i in range((ii - 1) * blockSize + 1, ii * blockSize + 1) for j in
                             range((jj - 1) * blockSize + 1, jj * blockSize + 1)]
                exactOneConstraint(variables)

    numberOfClause = len(clauses)

    # Add clauses by input
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            k = input[i - 1][j - 1]
            if k and k.isdigit():
                clauses.append([var(i, j, int(k))])

    numberOfClauseTotal = len(clauses)

    result, satisfiable = satSolving()
    stopTime = time.time()
    return {
        'satisfiable': satisfiable,
        'result': result,
        'numberOfVariable': defaultVariables + customVariables,
        'numberOfClause': numberOfClause,
        'numberOfClauseTotal': numberOfClauseTotal,
        'timeInSecond': stopTime - startTime}


if __name__ == '__main__':
    blockSize = 3
    size = blockSize * blockSize
    defaultVariables = size ** 3
    customVariables = 0
    clauses = []
    input = []

    mode = 1

    with open("sudoku_9x9.txt", "r") as f:
        for line in f.readlines():
            input.append(line.strip().split(","))

    result = solve()

    print(result)
    if (result['satisfiable']):
        for row in result['result']:
            print(row)
