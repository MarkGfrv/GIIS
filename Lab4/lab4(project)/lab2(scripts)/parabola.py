import matplotlib.pyplot as plt


def parabola(p):
    p = int(p)
    x, y = 0, 0
    x_values, y_values = list(), list()
    x_values.append(x)
    y_values.append(y)
    while x < 11:
        deltaH = (y ** 2) - (2 * p) * (x + 1)
        deltaV = (y + 1) * (y + 1) - 2 * p * x
        deltaD = (y + 1) * (y + 1) - (2 * p) * (x + 1)
        if ((abs(deltaD) < abs(deltaH) and abs(deltaD) < abs(deltaV)) or
                (abs(deltaD) == abs(deltaH) and abs(deltaD) < abs(deltaV)) or
                (abs(deltaD) == abs(deltaV)) and abs(deltaD) < abs(deltaH)):
            x += 1
            y += 1
            x_values.append(x)
            y_values.append(y)
        elif abs(deltaH) < abs(deltaD) and abs(deltaH) < abs(deltaV):
            x += 1
            x_values.append(x)
            y_values.append(y)
        elif abs(deltaV) < abs(deltaD) and abs(deltaV) < abs(deltaH):
            y += 1
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
    print('Введите значение фокального параметра(p)')
    p = input()
    x_values, y_values = parabola(p)
    print(x_values, y_values)
    graphic(x_values, y_values)


if __name__ == '__main__':
    main()
