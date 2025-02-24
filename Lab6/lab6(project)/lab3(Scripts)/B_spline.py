import matplotlib.pyplot as plt
from lab3Scripts.Ermit import matrix_multiplication


def b_spline(values):
    x_values, y_values, segments = list(), list(), list()
    P0, P1, P2 = values[0], values[1], values[2]
    M = [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]
    values.append(P0)
    values.append(P1)
    values.append(P2)
    values = [list(map(int, sublist)) for sublist in values]
    for i in range(len(values) - 3):
        temp_list = list()
        temp_list.append(values[i])
        temp_list.append(values[i + 1])
        temp_list.append(values[i + 2])
        temp_list.append(values[i + 3])
        segments.append(temp_list)
    for el in segments:
        P0 = el[0]
        P1 = el[1]
        P2 = el[2]
        P3 = el[3]
        G = [P0, P1, P2, P3]
        t = 0.0
        while t <= 1.0:
            T = [[t**3, t**2, t, 1]]
            P = matrix_multiplication(T, matrix_multiplication(M, G))
            P = [[item / 6 for item in sublist] for sublist in P]
            x = P[0][0]
            y = P[0][1]
            x_values.append(x)
            y_values.append(y)
            t += 0.1
    return x_values, y_values


def graphic(x_values, y_values):
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, color="gray", linewidth=2)
    plt.scatter(x_values, y_values, color="red", zorder=5)

    plt.title("График B-сплайна", fontsize=16)
    plt.xlabel("x(t)", fontsize=14)
    plt.ylabel("y(t)", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=12)
    plt.show()


def main():
    print("Введите количество точек:")
    n = int(input())
    values = list()
    for _ in range(n):
        print("Введите координаты точки")
        coords = input().split()
        values.append(coords)
    x_values, y_values = b_spline(values)
    print(x_values, y_values)
    graphic(x_values, y_values)


if __name__ == '__main__':
    main()
