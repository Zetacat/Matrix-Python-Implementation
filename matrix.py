from fractions import Fraction

class Matrix(object):
    calculated_det_record = {}
    
    def __init__(self, array):
        if len(array) > 1:
            for row in array[1:]:
                assert len(row) == len(array[0])

        self.content = array
        self.height = len(self.content)
        self.width = len(self.content[0])
        self.shape = (self.height, self.width)


    def __add__(self, matrix):
        new_array = []
        for i in range(self.height):
            new_row = []
            for j in range(self.width):
                new_row.append(self.content[i][j] + matrix.content[i][j])
            new_array.append(new_row)
        return Matrix(new_array)


    def __sub__(self, matrix):
        return self + (matrix * (-1))


    def __mul__(self, x):
        if type(x) == int:
            x = Fraction(x, 1)
        
        if type(x) == Fraction:
            new_array = []
            for i in range(self.height):
                new_row = []
                for j in range(self.width):
                    new_row.append(self.content[i][j] * x)
                new_array.append(new_row)
            return Matrix(new_array)
        
        elif type(x) == Matrix:
            assert self.width == x.height
            new_array = []
            for i in range(self.height):
                new_row = []
                for j in range(x.width):
                    product_sum = 0
                    for self_k, multiplier_k in zip(self.content[i], [row[j] for row in x.content]):
                        product_sum += self_k * multiplier_k
                    new_row.append(product_sum)
                new_array.append(new_row)
            return Matrix(new_array)


    def __rmul__(self, x):
        if type(x) != int:
            raise NotImplementedError
        return self * x


    def __pow__(self, power):
        result = IdentityMatrix(self.height)
        for _ in range(power):
            result = result * self
        return result


    def __str__(self):
        result = ""
        for row in self.content:
            for item in row:
                result += str(item) + "\t"
            result += "\n"
        return result


    def T(self):
        new_array = []
        for i in range(self.width):
            new_row = []
            for j in range(self.height):
                new_row.append(self.content[j][i])
            new_array.append(new_row)
        return Matrix(new_array)


    def det(self):
        assert self.height == self.width
        key = str(self)
        if key in Matrix.calculated_det_record:
            return Matrix.calculated_det_record[key]
        if self.height == 1:
            return self.content[0][0]
        product_sum = 0
        for j in range(self.width):
            product_sum += self.content[0][j] * self.cofactor(0, j)
        Matrix.calculated_det_record[key] = product_sum
        return product_sum


    def cofactor(self, row, col):
        new_array = []
        for i in range(self.height):
            if i == row:
                continue
            new_row = []
            for j in range(self.width):
                if j == col:
                    continue
                new_row.append(self.content[i][j])
            new_array.append(new_row)
        a = Matrix(new_array)
        return ((-1) ** (row + col)) * Matrix(new_array).det()


    def inverse(self):
        return self.adjoint() * (Fraction(1, 1) / self.det())


    def adjoint(self):
        new_array = []
        for i in range(self.height):
            new_row = []
            for j in range(self.width):            
                new_row.append(self.cofactor(i, j))
            new_array.append(new_row)
        return Matrix(new_array).T()


    def flatten(self):
        new_array = []
        for row in self.content:
            for element in row:
                new_array.append(element)
        return Matrix([new_array])


    def to_list(self):
        return self.content



class IdentityMatrix(Matrix):
    def __init__(self, size):
        array = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            array[i][i] = 1
        super(IdentityMatrix, self).__init__(array)



def test():
    A = Matrix([
            [1, 0], 
            [0, 1]
        ])
    B = Matrix([
            [1, 0], 
        ])
    C = Matrix([
            [1, 2, 3], 
            [4, 5, 6], 
            [7, 8, 9], 
        ])
    D = Matrix([
            [1, 2, 3], 
            [4, 5, 6], 
            [7, 2, 9], 
        ])
    E = Matrix([
            [1, 1, 1, 1], 
            [1, 1, 1, 1], 
            [1, 1, 1, 1], 
            [1, 1, 1, 1], 
        ])
    print(A)
    print(A + A)
    print(A - A)
    print(A * 2)
    print(2 * A)
    print(A * A)
    print(B.T())
    print(A.det())
    print(C.det())
    print(D.adjoint())
    print(D.inverse())
    print(E ** 4)
    print(A.flatten().to_list())


if __name__ == '__main__':
    test()