from __future__ import annotations
class row():
    def __init__(self, row):
        self.row = row
    def __add__(self, other: row):
        return row(list(self.row[i] + other.row[i] for i in range(len(self.row))))
    def __mul__(self, other: float):
        return row(list(x * other for x in self.row))
    def __getitem__(self, ind):
        return self.row[ind]
    def __len__(self):
        return len(self.row)

class matrix:
    def __init__(self, matrix):
        self.matrix = list(map(lambda x: row(x), matrix))
    def sum(self, row1, scalar1, row2, scalar2, dest):
        self.matrix[dest] = self.matrix[row1] * scalar1 + self.matrix[row2] * scalar2
    def __getitem__(self, item):
        return self.matrix[item]

class linear_equations():
    def __init__(self, equations, values):
        self.equations = matrix(equations)
        self.values = values
    def sum(self, row1, scalar1, row2, scalar2, dest):
        if dest in [row1, row2]:
            self.equations.sum(row1, scalar1, row2, scalar2, dest)
            self.values[dest] = self.values[row1] * scalar1 + self.values[row2] * scalar2
        else:
            ArithmeticError("Trying to store the sum of two rows in a third row")


def solve(equation, solutions):
    l1 = linear_equations(equation, solutions)
    for i in range(len(solutions)):
        for j in range(i + 1, len(solutions)):
            if l1.equations[i][i] != 0:
                l1.sum(i, -1 * l1.equations[j][i] / l1.equations[i][i], j, 1, j)
            else:
                return "can not be solved"
    if not all(list(not all(l1.equations[i][j] == 0 for j in range(len(l1.equations[i]))) for i in
                    range(len(l1.equations[0])))):
        return "can not be solved"
    solutions = []
    for i in range(len(l1.equations[0]) - 1, -1, -1):
        j = l1.values[i]
        for k in range(len(solutions)):
            j -= l1.equations[i][len(l1.equations[0]) - k - 1] * solutions[k]
        solutions.append(j / l1.equations[i][i])
    return (solutions[::-1])

def main():
    print(solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3]))
    print(solve([[4, -3, 1], [-2, 1, -3], [1, -1, 2]], [-8, -4, 2]))
    print(solve([[1, 1], [2, 2]], [1, 2]))

if __name__ == "__main__":
    main()
