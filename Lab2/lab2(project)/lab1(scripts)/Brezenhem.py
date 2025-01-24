import matplotlib.pyplot as plt

def brezenhem(f_coord, s_coord):
    x1 = int(f_coord[0])
    y1 = int(f_coord[1])
    dx = int(s_coord[0]) - x1
    dy = int(s_coord[1]) - y1
    x, y = x1, y1
    if dx >= dy:
        e = 2*dy - dx
    elif dy > dx:
        e = 2*dx - dy
    x_values = []
    x_values.append(x1)
    y_values = []
    y_values.append(y1)
    if dx >= dy:
        for i in range(1, dx+1):
            if e >= 0:
                y += 1
                e -= 2*dx
            x += 1
            e += 2*dy
            x_values.append(x)
            y_values.append(y)
    elif dy > dx:
        for i in range(1, dy+1):
            if e >= 0:
                y += 1
                e -= 2*dy
            x += 1
            e += 2*dx
            x_values.append(x)
            y_values.append(y)
    return x_values, y_values


def graphic(x_values, y_values):
    for i in range(len(x_values)):
        plt.plot([x_values[i], x_values[i] + 1], [y_values[i], y_values[i]], linestyle='-.', color='blue')
        plt.plot([x_values[i], x_values[i] + 1], [y_values[i] + 1, y_values[i] + 1], linestyle='-.', color='blue')
        plt.plot([x_values[i], x_values[i]], [y_values[i], y_values[i] + 1], linestyle='-.', color='blue')
        plt.plot([x_values[i] + 1, x_values[i] + 1], [y_values[i], y_values[i] + 1], linestyle='-.', color='blue')

    lower_left_x = x_values[::2]
    lower_left_y = y_values[::2]
    lower_left_x.append(x_values[-1] + 1)
    lower_left_y.append(y_values[-1] + 1)
    plt.plot(lower_left_x, lower_left_y, color='red', linestyle='-', linewidth=2, label='отрезок')

    plt.title("Отрезок по алгоритму Брезенхема")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def main():
    print("Введите через пробел координаты начала и конца первого отрезка")
    f_coord = input().split()
    print("Введите через пробел координаты начала и конца второго отрезка")
    s_coord = input().split()
    x_values, y_values = brezenhem(f_coord, s_coord)
    graphic(x_values, y_values)

if __name__ == '__main__':
    main()