import matplotlib.pyplot as plt

def vu(f_coord, s_coord):
    x0, y0 = int(f_coord[0]), int(f_coord[1])
    x1, y1 = int(s_coord[0]), int(s_coord[1])
    dx, dy = x1 - x0, y1 - y0
    values = []
    if abs(dx) >= abs(dy):
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        k = dy / dx       #угловой коэффициент
        for x in range(x0, x1 + 1):
            temp_list1 = []
            temp_list2 = []
            y = y0 + k*(x-x0)
            y_int = int(y)
            y_dec = y - y_int
            In_bot = 1 - y_dec
            In_top = y_dec
            temp_list1.append(x)
            temp_list1.append(y_int)
            temp_list1.append(In_bot)
            if x+1 <= x1 or y+1 <= y1:
                temp_list2.append(x)
                temp_list2.append(y_int + 1)
                temp_list2.append(In_top)
                values.append(temp_list1)
                values.append(temp_list2)
            else:
                values.append(temp_list1)
    else:
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        k = dx / dy       #угловой коэффициент
        for y in range(y0, y1 + 1):
            temp_list1 = []
            temp_list2 = []
            x = x0 + k*(y-y0)
            x_int = int(x)
            x_dec = x - x_int
            In_bot = 1 - x_dec
            In_top = x_dec
            temp_list1.append(x_int)
            temp_list1.append(y)
            temp_list1.append(In_bot)
            if x+1 <= x1 or y+1 <= y1:
                temp_list2.append(x_int + 1)
                temp_list2.append(y)
                temp_list2.append(In_top)
                values.append(temp_list1)
                values.append(temp_list2)
            else:
                values.append(temp_list1)
    return values


def graphic(values):
    plt.figure(figsize=(8, 8))
    x_start, y_start = values[0][0], values[0][1]
    x_end, y_end = values[-1][0], values[-1][1]
    plt.plot([x_start, x_end], [y_start, y_end], color='red', linewidth=1.5, label='Отрезок')
    for value in values:
        x, y, intensity = value
        plt.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color='black',
            alpha=intensity
        )
    plt.axis('equal')
    plt.grid(visible=True, color='lightgray', linestyle='--', linewidth=0.5)
    plt.show()


def main():
    print("Введите через пробел координаты начала и конца первого отрезка")
    f_coord = input().split()
    print("Введите через пробел координаты начала и конца второго отрезка")
    s_coord = input().split()
    values = vu(f_coord, s_coord)
    graphic(values)

if __name__ == '__main__':
    main()