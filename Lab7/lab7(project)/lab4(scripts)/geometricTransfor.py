import matplotlib.pyplot as plt
from lab3Scripts.Ermit import matrix_multiplication
import math
from mpl_toolkits.mplot3d import Axes3D

class GeometricTransformations:
    def __init__(self, coordinates: list):
        self.coord = coordinates

    def get_figure_matrix(self):
        matrix = []
        for i in range(len(self.coord)):
            coord_list = [int(self.coord[i][0]), int(self.coord[i][1]), int(self.coord[i][2]), 1]
            matrix.append(coord_list)
        return matrix

    def moving(self, new_coords: list, figure_matrix: list):
        avgx, avgy, avgz = 0, 0, 0
        for i in range(len(figure_matrix)):
            avgx += figure_matrix[i][0]
            avgy += figure_matrix[i][1]
            avgz += figure_matrix[i][2]
        avgx, avgy, avgz = avgx / len(figure_matrix), avgy / len(figure_matrix), avgz / len(figure_matrix)
        center_coords = [avgx, avgy, avgz]
        Dx, Dy, Dz = (int(new_coords[0]) - center_coords[0], int(new_coords[1]) - center_coords[1],
                      int(new_coords[2]) - center_coords[2])
        T = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [Dx, Dy, Dz, 1]]
        M = matrix_multiplication(figure_matrix, T)
        return M

    def turn(self, angle: str, figure_matrix: list, axis: str):
        rad = math.radians(int(angle))
        sinQ = math.sin(rad)
        cosQ = math.cos(rad)
        M = []
        if axis == 'x' or axis == 'X':
            T = [[1, 0, 0, 0], [0, cosQ, sinQ, 0], [0, -sinQ, cosQ, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        elif axis == 'y' or axis == 'Y':
            T = [[cosQ, 0, -sinQ, 0], [0, 1, 0, 0], [sinQ, 0, cosQ, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        elif axis == 'z' or axis == 'Z':
            T = [[cosQ, sinQ, 0, 0], [-sinQ, cosQ, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        return M

    def scaling(self, coeffs: list, figure_matrix: list):
        Sx, Sy, Sz = float(coeffs[0]), float(coeffs[1]), float(coeffs[2])
        S = [[Sx, 0, 0, 0], [0, Sy, 0, 0], [0, 0, Sz, 0], [0, 0, 0, 1]]
        M = matrix_multiplication(figure_matrix, S)
        return M

    def display(self, figure_matrix: list, axis: str):
        M = []
        if axis == 'y0z':
            T = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        elif axis == 'x0z':
            T = [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        elif axis == 'x0y':
            T = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        return M

    def perspective_projection(self, figure_matrix: list, axis : str, project_distance: str):
        d = int(project_distance)
        M = []
        if axis == 'x' or axis == 'X':
            T = [[1, 0, 0, 1 / d], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        elif axis == 'y' or axis == 'Y':
            T = [[1, 0, 0, 0], [0, 1, 0, 1 / d], [0, 0, 1, 0], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        elif axis == 'z' or axis == 'Z':
            T = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1 / d], [0, 0, 0, 1]]
            M = matrix_multiplication(figure_matrix, T)
        for i in range(len(M)):
            last_element = M[i][-1]
            if last_element > 1:
                M[i] = [x / last_element for x in M[i]]
        return M

    def draw_figure_by_matrix(self, matrix):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = [row[0] for row in matrix]
        y = [row[1] for row in matrix]
        z = [row[2] for row in matrix]
        ax.scatter(x, y, z, c='r', marker='o')
        ax.plot(x + [x[0]], y + [y[0]], z + [z[0]], c='b')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()


def main():
    n = int(input("Введите количество вершин фигуры: "))
    coords = []
    for _ in range(n):
        print("Введите координаты точки:")
        coord = input().split()
        coords.append(coord)
    print(coords)
    gt = GeometricTransformations(coords)
    matrix = gt.get_figure_matrix()
    print(gt.get_figure_matrix())
    gt.draw_figure_by_matrix(matrix)
    turned_matrix = gt.turn(90, matrix, 'y')
    print(turned_matrix)
    gt.draw_figure_by_matrix(turned_matrix)
    scaled_matrix = gt.scaling(['0.25', '0.5', '1'], matrix)
    print(scaled_matrix)
    gt.draw_figure_by_matrix(scaled_matrix)
    moved_coord = ['0', '0', '0']
    moved_matrix = gt.moving(moved_coord, matrix)
    print(moved_matrix)
    display1 = gt.display(matrix, 'x')
    display2 = gt.display(matrix, 'y')
    display3 = gt.display(matrix, 'z')
    print(display1)
    print(display2)
    print(display3)
    new_coords = [['1', '1', '1'], ['1', '4', '3'], ['4', '4', '3'], ['4', '1', '1']]
    gt2 = GeometricTransformations(new_coords)
    new_matrix = gt2.get_figure_matrix()
    perspective_matrix = gt.perspective_projection(new_matrix, 'z', 2)
    print(perspective_matrix)
    gt.draw_figure_by_matrix(perspective_matrix)


if __name__ == '__main__':
    main()
