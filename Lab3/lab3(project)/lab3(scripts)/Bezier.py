import matplotlib.pyplot as plt
from lab3Scripts.Ermit import matrix_multiplication


def bezier(P1, P2, P3, P4):
    t = 0.0
    highest_point = 1.0
    x_values, y_values = list(), list()
    M = [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]
    P1 = list(map(int, P1))
    P2 = list(map(int, P2))
    P3 = list(map(int, P3))
    P4 = list(map(int, P4))
    G = [P1, P2, P3, P4]
    while t <= highest_point:
        T = [[t**3, t**2, t, 1]]
        P = matrix_multiplication(T, matrix_multiplication(M, G))
        x = P[0][0]
        y = P[0][1]
        x_values.append(x)
        y_values.append(y)
        t += 0.1
    return x_values, y_values


def graphic(x_values, y_values):
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label="Кривая Безье", color="gray", linewidth=2)
    plt.scatter(x_values, y_values, color="red", zorder=5)

    plt.title("График кривой Безье", fontsize=16)
    plt.xlabel("x(t)", fontsize=14)
    plt.ylabel("y(t)", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=12)
    plt.show()


def main():
    print("Введите граничное условие P1")
    P1 = input().split()
    print("Введите граничное условие P2")
    P2 = input().split()
    print("Введите граничное условие P3")
    P3 = input().split()
    print("Введите граничное условие P4")
    P4 = input().split()
    x_values, y_values = bezier(P1, P2, P3, P4)
    print(x_values, y_values)
    graphic(x_values, y_values)


if __name__ == '__main__':
    main()