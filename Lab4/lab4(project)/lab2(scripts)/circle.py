import matplotlib.pyplot as plt


def circle(center_coord, radius):
    x_values, y_values = list(), list()
    x = int(center_coord[0])
    R = int(radius)
    y = R
    limit = int(center_coord[1])
    delta = 2 - 2*R
    x_values.append(x)
    y_values.append(y)
    while y > limit:
        if delta > 0:
            d = 2*delta - 2*x - 1
            if d > 0:
                y -= 1
                delta = delta - 2*y + 1
            else:
                x += 1
                y -= 1
                delta = delta + 2*x - 2*y + 2
            x_values.append(x)
            y_values.append(y)
        elif delta < 0:
            d = 2*delta + 2*y - 1
            if d > 0:
                x += 1
                y -= 1
                delta = delta + 2*x -2*y + 2
            else:
                x += 1
                delta = delta + 2*x + 1
            x_values.append(x)
            y_values.append(y)
        elif delta == 0:
            x += 1
            y -= 1
            delta = delta + 2*x - 2*y + 2
            x_values.append(x)
            y_values.append(y)
    return x_values, y_values


def graphic(x_values, y_values):
    plt.figure(figsize=(8, 8))
    for x, y in zip(x_values, y_values):
        plt.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color='gray'
        )
    plt.axis('equal')
    plt.grid(visible=True, color='lightgray', linestyle='--', linewidth=0.5)
    plt.show()


def main():
    print("Введите через пробел координаты центра окружности")
    center_coord = input().split()
    print("Введите радиус окружности")
    radius = input()
    x_values, y_values = circle(center_coord, radius)
    graphic(x_values, y_values)
    print(x_values, y_values)


if __name__ == '__main__':
    main()