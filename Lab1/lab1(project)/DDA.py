import matplotlib.pyplot as plt

def Signum(argument):
    if argument > 0:
        return 1
    elif argument == 0:
        return 0
    else:
        return -1


def DDA(f_coord, s_coord):
    length = max(abs(float(s_coord[0]) - float(f_coord[0])), abs(float(s_coord[1]) - float(f_coord[1])))
    dx = (float(s_coord[0]) - float(f_coord[0])) / length
    dy = (float(s_coord[1]) - float(f_coord[1])) / length
    x1 = float(f_coord[0]) + 0.5 * Signum(dx)
    y1 = float(f_coord[1]) + 0.5 * Signum(dy)
    return length, dx, dy, x1, y1


def graphic(length, dx, dy, x1, y1):
    x_values = []
    y_values = []
    for i in range(0, int(length)):
        x = x1 + dx * i
        y = y1 + dy * i
        x_values.append(x)
        y_values.append(y)
        print(x, y)

    plt.figure(figsize=(12, 10))
    plt.plot(x_values, y_values, marker='o', label='точки DDA')
    plt.title('Алгоритм DDA')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    print("Введите через пробел координаты начала и конца первого отрезка")
    f_coord = input().split()
    print("Введите через пробел координаты начала и конца второго отрезка")
    s_coord = input().split()
    length, dx, dy, x1, y1 = DDA(f_coord, s_coord)
    graphic(length, dx, dy, x1, y1)


if __name__ == '__main__':
    main()

