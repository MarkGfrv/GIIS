import matplotlib.pyplot as plt


def ellips(center_coord, a, b):
    x_values, y_values = list(), list()
    a = int(a)
    b = int(b)
    x = int(center_coord[0])
    y = b
    limit = int(center_coord[1])
    x_values.append(x)
    y_values.append(y)
    delta = a**2 + b**2 - 2*b*(a**2)
    while y > limit:
        if delta > 0:
            d = 2 * (delta - x * (b ** 2)) - 1
            if d > 0:
                y -= 1
                delta = delta + (1 - 2 * y) * (a**2)
            else:
                x += 1
                y -= 1
                delta = delta + (2 * x + 1) * (b ** 2) + (1 - 2 * y) * (a ** 2)
            x_values.append(x)
            y_values.append(y)
        elif delta < 0:
            d = 2 * (delta + y * (a ** 2)) - 1
            if d > 0:
                x += 1
                y -= 1
                delta = delta + (2 * x + 1) * (b ** 2) + (1 - 2 * y) * (a ** 2)
            else:
                x += 1
                delta = delta + (2 * x + 1) * (b ** 2)
            x_values.append(x)
            y_values.append(y)
        elif delta == 0:
            x += 1
            y -= 1
            delta = delta + (2 * x + 1) * (b ** 2) + (1 - 2 * y) * (a ** 2)
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
    print("Введите через пробел координаты центра эллипса")
    center_coord = input().split()
    print("Введите значение малой полуоси эллипса(а)")
    b = input()
    print("Введите значение большой полуоси эллипса(b)")
    a = input()
    x_values, y_values = ellips(center_coord, a, b)
    graphic(x_values, y_values)


if __name__ == '__main__':
    main()