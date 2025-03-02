import matplotlib.pyplot as plt


def matrix_multiplication(matrix1, matrix2):
    rows_a = len(matrix1)
    cols_b = len(matrix2[0])
    common_dim = len(matrix2)
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(common_dim):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    return result


def ermit(P1, P4, R1, R4):
    t = 0.0
    highest_point = 1.0
    x_values, y_values, G = list(), list(), list()  # G - вектор Эрмитовой геометрии
    M = [[2, -2, 1, 1], [-3, 3, -2, -1], [0, 0, 1, 0], [1, 0, 0, 0]]
    P1 = list(map(int, P1))
    P4 = list(map(int, P4))
    R1 = list(map(int, R1))
    R4 = list(map(int, R4))
    G = [P1, P4, R1, R4]
    while t <= highest_point:
        T = [[t**3, t**2, t, 1]]
        P = matrix_multiplication(T, matrix_multiplication(M, G))
        x, y = P[0][0], P[0][1]
        x_values.append(x)
        y_values.append(y)
        t += 0.1
    return x_values, y_values


def graphic(x_values, y_values):
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label="Кривая Эрмита", color="gray", linewidth=2)
    plt.scatter(x_values, y_values, color="red", zorder=5)

    plt.title("График кривой Эрмита", fontsize=16)
    plt.xlabel("x(t)", fontsize=14)
    plt.ylabel("y(t)", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=12)
    plt.show()


def main():
    print("Введите граничное условие P1")
    P1 = input().split()
    print("Введите граничное условие P4")
    P4 = input().split()
    print("Введите граничное условие R1")
    R1 = input().split()
    print("Введите граничное условие R4")
    R4 = input().split()
    x_values, y_values = ermit(P1, P4, R1, R4)
    print(x_values, y_values)
    graphic(x_values, y_values)


if __name__ == '__main__':
    main()
