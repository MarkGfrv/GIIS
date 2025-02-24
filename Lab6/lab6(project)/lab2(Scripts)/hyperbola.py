import matplotlib.pyplot as plt

def hyperbola(a, b):
    a, b = int(a), int(b)
    x, y = a, 0
    limit = 2 * b
    x_values, y_values = list(), list()
    x_values.append(x)
    y_values.append(y)
    delta = (x ** 2) * (b ** 2) - (y ** 2) * (a ** 2) - (a ** 2) * (b ** 2)
    while y < limit:
        if delta > 0:
            d = 2 * (delta - x * (b ** 2)) - 1
            if d > 0:
                y += 1
                delta = delta - (a ** 2) * (2 * y + 1)
            else:
                x += 1
                y += 1
                delta = delta + (b ** 2) * (2 * x + 1) - (a ** 2) * (2 * y + 1)
            x_values.append(x)
            y_values.append(y)
        elif delta < 0:
            d = 2 * (delta + y * (a ** 2)) + 1
            if d > 0:
                x += 1
                y += 1
                delta = delta + (b ** 2) * (2 * x + 1) - (a ** 2) * (2 * y + 1)
            else:
                x += 1
                delta = delta + (b ** 2) * (2 * x + 1)
            x_values.append(x)
            y_values.append(y)
        elif delta == 0:
            x += 1
            y += 1
            delta = delta + (b ** 2) * (2 * x + 1) - (a ** 2) * (2 * y + 1)
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
    print("Введите значение большой полуоси гиперболы(а)")
    a = input()
    print("Введите значение малой полуоси гиперболы(b)")
    b = input()
    x_values, y_values = hyperbola(a, b)
    graphic(x_values, y_values)


if __name__ == '__main__':
    main()
