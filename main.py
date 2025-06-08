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

    def __str__(self):
        return str(self.row)

    def __len__(self):
        return len(self.row)


class matrix:
    def __init__(self, matrix):
        self.matrix = list(map(lambda x: row(x), matrix))

    def sum(self, row1, scalar1, row2, scalar2, dest):
        self.matrix[dest] = self.matrix[row1] * scalar1 + self.matrix[row2] * scalar2

    def is_echelon(self):
        for i in range(len(self.matrix)):
            for k in range(i):
                if self.matrix[i][k] != 0:
                    return False
        return True

    def __getitem__(self, item):
        return self.matrix[item]

    def __str__(self):
        return "/" + str(list(f"{x:>2}" for x in self.matrix[0])) + "\\\n" + "\n".join(
            list("|" + str(list(map(lambda y: f"{y:>2}", x))) + "|" for x in self.matrix[1:-1])) + "\n\\" + str(
            list(map(lambda x: f"{x:>2}", self.matrix[-1]))) + "/"


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

    def __str__(self):
        return ("/" + str(list(f"{x:>4}" for x in self.equations[0])) + f"|{self.values[0]:>4}" + "\\" + ("\n"*(len(self.values)>2))+
                "\n".join(
                    list("|" + str(list(
                        map(lambda y: f"{y:>4}", self.equations[x + 1]))) + "|" + f"{str(self.values[x + 1]):>4}" + "|"
                         for x in range(len(self.equations[1:-1]))
                         )
                ) + "\n\\"
                + str(list(map(lambda x: f"{x:>4}", self.equations[-1]))) + f"|{self.values[-1]:>4}" + "/" + "\n")


def solve(equation, solutions):
    l1 = linear_equations(equation, solutions)
    print(l1)
    for i in range(len(solutions)):
        for j in range(i + 1, len(solutions)):
            #print(l1.equations[i][i])
            if l1.equations[i][i] != 0:
                l1.sum(i, -1 * l1.equations[j][i] / l1.equations[i][i], j, 1, j)
            else:
                return "can not be solved"

        #print(l1)
    #print(l1)

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
