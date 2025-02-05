import tkinter as tk
from tkinter import Menu, Button, Toplevel, Label, Entry, Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from lab1Scripts.DDA import DDA
from lab1Scripts.Brezenhem import brezenhem
from lab1Scripts.Vu import vu
from lab2Scripts.circle import circle
from lab2Scripts.ellips import ellips
from lab2Scripts.hyperbola import hyperbola
from lab2Scripts.parabola import parabola
from lab3Scripts.Ermit import ermit
from lab3Scripts.Bezier import bezier
from lab3Scripts.B_spline import b_spline
import time


def graphic(length, dx, dy, x1, y1, canvas):
    x_values = []
    y_values = []
    for i in range(0, int(length)):
        x = x1 + dx * i
        y = y1 + dy * i
        x_values.append(x)
        y_values.append(y)

    figure = plt.Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(x_values, y_values, marker='o', label='точки DDA')
    ax.set_title('Алгоритм DDA')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)
    ax.legend()

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack()


def brezenhem_graphic(x_values, y_values, canvas):
    figure = plt.Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)

    for i in range(len(x_values)):
        ax.plot([x_values[i], x_values[i] + 1], [y_values[i], y_values[i]], linestyle='-.', color='blue')
        ax.plot([x_values[i], x_values[i] + 1], [y_values[i] + 1, y_values[i] + 1], linestyle='-.', color='blue')
        ax.plot([x_values[i], x_values[i]], [y_values[i], y_values[i] + 1], linestyle='-.', color='blue')
        ax.plot([x_values[i] + 1, x_values[i] + 1], [y_values[i], y_values[i] + 1], linestyle='-.', color='blue')

    ax.plot(
        [x_values[0], x_values[-1]],
        [y_values[0], y_values[-1]],
        color='red', linestyle='-', linewidth=2, label='прямая'
    )

    ax.set_title("Отрезок по алгоритму Брезенхема")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()

    canvas_graph = FigureCanvasTkAgg(figure, canvas)
    canvas_graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def brezenhem_debug(f_coord, s_coord, canvas, info_label):
    x1, y1 = int(f_coord[0]), int(f_coord[1])
    x2, y2 = int(s_coord[0]), int(s_coord[1])
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1

    x, y = x1, y1
    x_values, y_values = [x], [y]
    if dx >= dy:
        e = 2 * dy - dx
        steps = dx
    else:
        e = 2 * dx - dy
        steps = dy

    figure = Figure(figsize=(5, 5), dpi=100)
    ax = figure.add_subplot(111)

    def draw_grid():
        ax.set_xticks(range(min(x1, x2) - 2, max(x1, x2) + 3))
        ax.set_yticks(range(min(y1, y2) - 2, max(y1, y2) + 3))
        ax.grid(visible=True, color="gray", linestyle="--", linewidth=0.5)
        ax.set_xlim(min(x1, x2) - 2, max(x1, x2) + 2)
        ax.set_ylim(min(y1, y2) - 2, max(y1, y2) + 2)
        ax.set_aspect("equal")

    draw_grid()
    ax.plot([x, x + 1], [y, y], linestyle="-.", color="blue")
    ax.plot([x, x + 1], [y + 1, y + 1], linestyle="-.", color="blue")
    ax.plot([x, x], [y, y + 1], linestyle="-.", color="blue")
    ax.plot([x + 1, x + 1], [y, y + 1], linestyle="-.", color="blue")

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()

    step = 0

    def update_graph():
        nonlocal x, y, e, step
        if step >= steps:
            ax.plot(
                [x1, x2], [y1, y2], color="red", linestyle="-", linewidth=2, label="Прямая"
            )
            ax.legend()
            canvas_widget.draw()
            return

        if dx >= dy:
            if e >= 0:
                y += sy
                e -= 2 * dx
            x += sx
            e += 2 * dy
        else:
            if e >= 0:
                x += sx
                e -= 2 * dy
            y += sy
            e += 2 * dx

        x_values.append(x)
        y_values.append(y)

        ax.plot([x, x + 1], [y, y], linestyle="-.", color="blue")
        ax.plot([x, x + 1], [y + 1, y + 1], linestyle="-.", color="blue")
        ax.plot([x, x], [y, y + 1], linestyle="-.", color="blue")
        ax.plot([x + 1, x + 1], [y, y + 1], linestyle="-.", color="blue")

        info_label.config(
            text=f"Итерация: {step + 1}/{steps}\nТекущая точка: ({x}, {y})\nЗначение ошибки: {e}"
        )

        canvas_widget.draw()
        step += 1
        canvas.after(1000, update_graph)

    update_graph()


def wu_graphic(values, canvas):
    figure = Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    x_start, y_start = values[0][0], values[0][1]
    x_end, y_end = values[-1][0], values[-1][1]

    ax.plot([x_start, x_end], [y_start, y_end], color='red', linewidth=1.5, label='Отрезок')

    for value in values:
        x, y, intensity = value
        ax.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color='black',
            alpha=intensity
        )

    ax.set_title("Алгоритм Ву")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack()


def wu_debug(f_coord, s_coord, canvas, info_label):
    x0, y0 = int(f_coord[0]), int(f_coord[1])
    x1, y1 = int(s_coord[0]), int(s_coord[1])
    dx, dy = x1 - x0, y1 - y0
    values = []

    if abs(dx) >= abs(dy):
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        k = dy / dx  # угловой коэффициент
        for x in range(x0, x1 + 1):
            y = y0 + k * (x - x0)
            y_int = int(y)
            y_dec = y - y_int
            In_bot = 1 - y_dec
            In_top = y_dec
            values.append((x, y_int, In_bot))
            values.append((x, y_int + 1, In_top))
    else:
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        k = dx / dy  # угловой коэффициент
        for y in range(y0, y1 + 1):
            x = x0 + k * (y - y0)
            x_int = int(x)
            x_dec = x - x_int
            In_bot = 1 - x_dec
            In_top = x_dec
            values.append((x_int, y, In_bot))
            values.append((x_int + 1, y, In_top))

    figure = Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.set_title("Пошаговый алгоритм Ву")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack()

    for i, (x, y, intensity) in enumerate(values):
        ax.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color='black',
            alpha=intensity
        )

        info_label.config(
            text=f"Шаг {i + 1}/{len(values)}\nТекущая точка: ({x}, {y})\nИнтенсивность: {intensity:.2f}"
        )

        canvas_widget.draw()
        canvas.update()
        time.sleep(0.8)



def open_cda_window():
    cda_window = Toplevel()
    cda_window.title("Алгоритм ЦДА")
    cda_window.geometry("630x600")

    frame_point1 = tk.Frame(cda_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата X1:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата Y1:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(cda_window)
    frame_point2.pack(pady=5)

    # Поле ввода для координаты X2
    lbl_x2 = Label(frame_point2, text="Координата X2:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y2
    lbl_y2 = Label(frame_point2, text="Координата Y2:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(cda_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val = []
            seg2_val.append(entry_x2.get())
            seg2_val.append(entry_y2.get())
            length, dx, dy, nx1, ny1 = DDA(seg1_val, seg2_val)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            graphic(length, dx, dy, nx1, ny1, canvas_frame)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(cda_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def open_brezenhem_window():
    brezenhem_window = Toplevel()
    brezenhem_window.title("Алгоритм Брезенхема")
    brezenhem_window.geometry("630x600")

    frame_point1 = tk.Frame(brezenhem_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата X1:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата Y1:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(brezenhem_window)
    frame_point2.pack(pady=5)

    # Поле ввода для координаты X2
    lbl_x2 = Label(frame_point2, text="Координата X2:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y2
    lbl_y2 = Label(frame_point2, text="Координата Y2:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(brezenhem_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val = []
            seg2_val.append(entry_x2.get())
            seg2_val.append(entry_y2.get())
            x_values, y_values = brezenhem(seg1_val, seg2_val)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            brezenhem_graphic(x_values, y_values, canvas_frame)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(brezenhem_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def open_wu_window():
    wu_window = Toplevel()
    wu_window.title("Алгоритм Ву")
    wu_window.geometry("630x600")

    frame_point1 = tk.Frame(wu_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата X1:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата Y1:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(wu_window)
    frame_point2.pack(pady=5)

    # Поле ввода для координаты X2
    lbl_x2 = Label(frame_point2, text="Координата X2:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y2
    lbl_y2 = Label(frame_point2, text="Координата Y2:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(wu_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val = []
            seg2_val.append(entry_x2.get())
            seg2_val.append(entry_y2.get())
            values = vu(seg1_val, seg2_val)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            wu_graphic(values, canvas_frame)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(wu_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def open_brezenhem_debug_window():
    brezenhem_window = Toplevel()
    brezenhem_window.title("Алгоритм Брезенхема")
    brezenhem_window.geometry("630x730")

    frame_point1 = tk.Frame(brezenhem_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата X1:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата Y1:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(brezenhem_window)
    frame_point2.pack(pady=5)

    # Поле ввода для координаты X2
    lbl_x2 = Label(frame_point2, text="Координата X2:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y2
    lbl_y2 = Label(frame_point2, text="Координата Y2:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(brezenhem_window, bg="white", width=300, height=150)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(brezenhem_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val = []
            seg2_val.append(entry_x2.get())
            seg2_val.append(entry_y2.get())
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            brezenhem_debug(seg1_val, seg2_val, canvas_frame, info_label)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(brezenhem_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def open_wu_debug_window():
    wu_window = Toplevel()
    wu_window.title("Алгоритм Ву")
    wu_window.geometry("630x600")

    frame_point1 = tk.Frame(wu_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата X1:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата Y1:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(wu_window)
    frame_point2.pack(pady=5)

    # Поле ввода для координаты X2
    lbl_x2 = Label(frame_point2, text="Координата X2:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y2
    lbl_y2 = Label(frame_point2, text="Координата Y2:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(wu_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(wu_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val = []
            seg2_val.append(entry_x2.get())
            seg2_val.append(entry_y2.get())
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            wu_debug(seg1_val, seg2_val, canvas_frame, info_label)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(wu_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def circle_graphic(x_values, y_values, canvas):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    for x, y in zip(x_values, y_values):
        ax.fill([
            x, x + 1, x + 1, x
        ], [
            y, y, y + 1, y + 1
        ], color="gray")

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()


def open_circle_window():
    circle_window = Toplevel()
    circle_window.title("Алгоритм Брезенхема для генерации окружности")
    circle_window.geometry("630x600")

    frame_point1 = tk.Frame(circle_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата центра X:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата центра Y:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(circle_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра p
    lbl_x2 = Label(frame_point2, text="Радиус окружности R:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(circle_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(circle_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val = entry_x2.get()
            x_values, y_values = circle(seg1_val, seg2_val)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            circle_graphic(x_values, y_values, canvas_frame)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(circle_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def circle_debug(center_coord, radius, canvas, info_label):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    def draw_grid():
        ax.grid(visible=True, color="gray", linestyle="--", linewidth=0.5)
        ax.set_aspect("equal")

    draw_grid()

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()

    x = int(center_coord[0])
    y = int(radius)
    delta = 2 - 2 * int(radius)
    limit = int(center_coord[1])

    x_values, y_values = [x], [y]
    step = 0

    def update_circle():
        nonlocal x, y, delta, step
        if y < limit:
            return

        ax.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color="gray",
        )
        canvas_widget.draw()
        info_label.config(
            text=f"Шаг {step + 1}: Точка ({x}, {y})\nОшибка (delta): {delta}"
        )

        if delta > 0:
            d = 2 * delta - 2 * x - 1
            if d > 0:
                y -= 1
                delta = delta - 2 * y + 1
            else:
                x += 1
                y -= 1
                delta = delta + 2 * x - 2 * y + 2
        elif delta < 0:
            d = 2 * delta + 2 * y - 1
            if d > 0:
                x += 1
                y -= 1
                delta = delta + 2 * x - 2 * y + 2
            else:
                x += 1
                delta = delta + 2 * x + 1
        elif delta == 0:
            x += 1
            y -= 1
            delta = delta + 2 * x - 2 * y + 2

        x_values.append(x)
        y_values.append(y)

        step += 1
        canvas.after(1000, update_circle)

    update_circle()


def open_circle_debug_window():
    circle_window = Toplevel()
    circle_window.title("Алгоритм Брезенхема для генерации окружности")
    circle_window.geometry("630x600")

    frame_point1 = tk.Frame(circle_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата центра X:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата центра Y:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(circle_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра p
    lbl_x2 = Label(frame_point2, text="Радиус окружности R:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(circle_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(circle_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val = entry_x2.get()
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            circle_debug(seg1_val, seg2_val, canvas_frame, info_label)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(circle_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def ellips_graphic(x_values, y_values, canvas):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    for x, y in zip(x_values, y_values):
        ax.fill([
            x, x + 1, x + 1, x
        ], [
            y, y, y + 1, y + 1
        ], color="gray")

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()


def open_ellips_window():
    ellips_window = Toplevel()
    ellips_window.title("Алгоритм Брезенхема для генерации эллипса")
    ellips_window.geometry("630x600")

    frame_point1 = tk.Frame(ellips_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата центра X:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата центра Y:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(ellips_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра a
    lbl_x2 = Label(frame_point2, text="Значение большой полуоси a:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для параметра b
    lbl_y2 = Label(frame_point2, text="Значение малой полуоси b:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(ellips_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(ellips_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val1 = entry_x2.get()
            seg2_val2 = entry_y2.get()
            x_values, y_values = ellips(seg1_val, seg2_val1, seg2_val2)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            ellips_graphic(x_values, y_values, canvas_frame)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(ellips_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def ellips_debug(center_coord, a, b, canvas, info_label):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    def draw_grid():
        ax.grid(visible=True, color="gray", linestyle="--", linewidth=0.5)
        ax.set_aspect("equal")

    draw_grid()

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()

    a = int(a)
    b = int(b)
    x = int(center_coord[0])
    y = b
    delta = a ** 2 + b ** 2 - 2 * b * (a ** 2)
    limit = int(center_coord[1])

    x_values, y_values = [x], [y]
    step = 0

    def update_ellipse():
        nonlocal x, y, delta, step
        if y < limit:
            return

        ax.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color="gray",
        )
        canvas_widget.draw()

        info_label.config(
            text=f"Шаг {step + 1}: Точка ({x}, {y})\nОшибка (delta): {delta}"
        )
        if delta > 0:
            d = 2 * (delta - x * (b ** 2)) - 1
            if d > 0:
                y -= 1
                delta = delta + (1 - 2 * y) * (a ** 2)
            else:
                x += 1
                y -= 1
                delta = delta + (2 * x + 1) * (b ** 2) + (1 - 2 * y) * (a ** 2)
        elif delta < 0:
            d = 2 * (delta + y * (a ** 2)) - 1
            if d > 0:
                x += 1
                y -= 1
                delta = delta + (2 * x + 1) * (b ** 2) + (1 - 2 * y) * (a ** 2)
            else:
                x += 1
                delta = delta + (2 * x + 1) * (b ** 2)
        elif delta == 0:
            x += 1
            y -= 1
            delta = delta + (2 * x + 1) * (b ** 2) + (1 - 2 * y) * (a ** 2)

        x_values.append(x)
        y_values.append(y)
        step += 1
        canvas.after(1000, update_ellipse)
    update_ellipse()


def open_ellips_debug_window():
    ellips_window = Toplevel()
    ellips_window.title("Алгоритм Брезенхема для генерации эллипса")
    ellips_window.geometry("630x600")

    frame_point1 = tk.Frame(ellips_window)
    frame_point1.pack(pady=5)

    # Поле ввода для координаты X1
    lbl_x1 = Label(frame_point1, text="Координата центра X:")
    lbl_x1.pack(side=tk.LEFT, padx=5)
    entry_x1 = Entry(frame_point1, width=10)
    entry_x1.pack(side=tk.LEFT, padx=5)

    # Поле ввода для координаты Y1
    lbl_y1 = Label(frame_point1, text="Координата центра Y:")
    lbl_y1.pack(side=tk.LEFT, padx=5)
    entry_y1 = Entry(frame_point1, width=10)
    entry_y1.pack(side=tk.LEFT, padx=5)

    frame_point2 = tk.Frame(ellips_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра a
    lbl_x2 = Label(frame_point2, text="Значение большой полуоси a:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для параметра b
    lbl_y2 = Label(frame_point2, text="Значение малой полуоси b:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(ellips_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(ellips_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            seg1_val = []
            seg1_val.append(entry_x1.get())
            seg1_val.append(entry_y1.get())
            seg2_val1 = entry_x2.get()
            seg2_val2 = entry_y2.get()
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            ellips_debug(seg1_val, seg2_val1, seg2_val2, canvas_frame, info_label)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(ellips_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def hyperbola_graphic(x_values, y_values, canvas):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    for x, y in zip(x_values, y_values):
        ax.fill([
            x, x + 1, x + 1, x
        ], [
            y, y, y + 1, y + 1
        ], color="gray")

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()


def open_hyperbola_window():
    hyperbola_window = Toplevel()
    hyperbola_window.title("Алгоритм Брезенхема для генерации гиперболы")
    hyperbola_window.geometry("630x600")

    frame_point2 = tk.Frame(hyperbola_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра a
    lbl_x2 = Label(frame_point2, text="Значение большой полуоси a:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для параметра b
    lbl_y2 = Label(frame_point2, text="Значение малой полуоси b:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(hyperbola_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(hyperbola_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            a = entry_x2.get()
            b = entry_y2.get()
            x_values, y_values = hyperbola(a, b)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            hyperbola_graphic(x_values, y_values, canvas_frame)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(hyperbola_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def hyperbola_debug(a, b, canvas, info_label):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    def draw_grid():
        ax.grid(visible=True, color="gray", linestyle="--", linewidth=0.5)
        ax.set_aspect("equal")

    draw_grid()

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()

    a, b = int(a), int(b)
    x, y = a, 0
    limit = 2 * b
    delta = (x ** 2) * (b ** 2) - (y ** 2) * (a ** 2) - (a ** 2) * (b ** 2)

    x_values, y_values = [x], [y]
    step = 0

    def update_hyperbola():
        nonlocal x, y, delta, step
        if y >= limit:
            return

        ax.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color="gray",
        )
        canvas_widget.draw()
        info_label.config(
            text=f"Шаг {step + 1}: Точка ({x}, {y})\nОшибка (delta): {delta}"
        )
        if delta > 0:
            d = 2 * (delta - x * (b ** 2)) - 1
            if d > 0:
                y += 1
                delta = delta - (a ** 2) * (2 * y + 1)
            else:
                x += 1
                y += 1
                delta = delta + (b ** 2) * (2 * x + 1) - (a ** 2) * (2 * y + 1)
        elif delta < 0:
            d = 2 * (delta + y * (a ** 2)) + 1
            if d > 0:
                x += 1
                y += 1
                delta = delta + (b ** 2) * (2 * x + 1) - (a ** 2) * (2 * y + 1)
            else:
                x += 1
                delta = delta + (b ** 2) * (2 * x + 1)
        elif delta == 0:
            x += 1
            y += 1
            delta = delta + (b ** 2) * (2 * x + 1) - (a ** 2) * (2 * y + 1)

        x_values.append(x)
        y_values.append(y)
        step += 1
        canvas.after(1000, update_hyperbola)
    update_hyperbola()


def open_hyperbola_debug_window():
    hyperbola_window = Toplevel()
    hyperbola_window.title("Алгоритм Брезенхема для генерации гиперболы")
    hyperbola_window.geometry("630x600")

    frame_point2 = tk.Frame(hyperbola_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра a
    lbl_x2 = Label(frame_point2, text="Значение большой полуоси a:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    # Поле ввода для параметра b
    lbl_y2 = Label(frame_point2, text="Значение малой полуоси b:")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=10)
    entry_y2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(hyperbola_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(hyperbola_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            a = entry_x2.get()
            b = entry_y2.get()
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            hyperbola_debug(a, b, canvas_frame, info_label)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(hyperbola_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def parabola_graphic(x_values, y_values, canvas):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    for x, y in zip(x_values, y_values):
        ax.fill([
            x, x + 1, x + 1, x
        ], [
            y, y, y + 1, y + 1
        ], color="gray")

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()


def open_parabola_window():
    parabola_window = Toplevel()
    parabola_window.title("Алгоритм Брезенхема для генерации параболы")
    parabola_window.geometry("630x600")

    frame_point2 = tk.Frame(parabola_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра p
    lbl_x2 = Label(frame_point2, text="Значение фокального параметра p:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(parabola_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(parabola_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            p = entry_x2.get()
            x_values, y_values = parabola(p)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            parabola_graphic(x_values, y_values, canvas_frame)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(parabola_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def parabola_debug(p, canvas, info_label):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    def draw_grid():
        ax.grid(visible=True, color="gray", linestyle="--", linewidth=0.5)
        ax.set_aspect("equal")
    draw_grid()
    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.draw()

    p = int(p)
    x, y = 0, 0
    x_values, y_values = [x], [y]
    step = 0
    def update_parabola():
        nonlocal x, y, step
        if x >= 11:
            return

        ax.fill(
            [x, x + 1, x + 1, x],
            [y, y, y + 1, y + 1],
            color="gray",
        )
        canvas_widget.draw()

        deltaH = (y ** 2) - (2 * p) * (x + 1)
        deltaV = (y + 1) * (y + 1) - 2 * p * x
        deltaD = (y + 1) * (y + 1) - (2 * p) * (x + 1)

        info_label.config(
            text=f"Шаг {step + 1}: Точка ({x}, {y})\n"
                 f"Ошибки: ΔH={deltaH}, ΔV={deltaV}, ΔD={deltaD}"
        )

        if ((abs(deltaD) < abs(deltaH) and abs(deltaD) < abs(deltaV)) or
                (abs(deltaD) == abs(deltaH) and abs(deltaD) < abs(deltaV)) or
                (abs(deltaD) == abs(deltaV) and abs(deltaD) < abs(deltaH))):
            x += 1
            y += 1
        elif abs(deltaH) < abs(deltaD) and abs(deltaH) < abs(deltaV):
            x += 1
        elif abs(deltaV) < abs(deltaD) and abs(deltaV) < abs(deltaH):
            y += 1

        x_values.append(x)
        y_values.append(y)

        step += 1
        canvas.after(1000, update_parabola)

    update_parabola()


def open_parabola_debug_window():
    parabola_window = Toplevel()
    parabola_window.title("Алгоритм Брезенхема для генерации параболы")
    parabola_window.geometry("630x600")

    frame_point2 = tk.Frame(parabola_window)
    frame_point2.pack(pady=5)

    # Поле ввода для параметра p
    lbl_x2 = Label(frame_point2, text="Значение фокального параметра p:")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=10)
    entry_x2.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(parabola_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(parabola_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    def on_ok():
        try:
            p = entry_x2.get()
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            parabola_debug(p, canvas_frame, info_label)
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(parabola_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def ermit_graphic(x_values, y_values, canvas, on_point_click):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(x_values, y_values, color="gray", linewidth=2)
    points = ax.scatter(x_values, y_values, color="red", s=30)

    max_y = max(y_values)
    y_limit = max(1.0, (int(max_y * 10) + 1) / 10)
    ax.set_ylim(0, y_limit)
    yticks = [i / 10 for i in range(0, int(y_limit * 10) + 1)]
    ax.set_yticks(yticks)

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)
    def on_click(event):
        if event.inaxes == ax:
            cont, ind = points.contains(event)
            if cont:
                point_index = ind["ind"][0]
                on_point_click(point_index, x_values, y_values)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.mpl_connect("button_press_event", on_click)
    canvas_widget.draw()


def open_edit_point_window(parent, index, x_values, y_values, on_save):
    edit_window = Toplevel(parent)
    edit_window.title("Редактировать точку")

    Label(edit_window, text=f"Точка {index + 1}").pack(pady=5)

    Label(edit_window, text="X:").pack()
    x_entry = Entry(edit_window)
    x_entry.insert(0, str(x_values[index]))
    x_entry.pack(pady=5)

    Label(edit_window, text="Y:").pack()
    y_entry = Entry(edit_window)
    y_entry.insert(0, str(y_values[index]))
    y_entry.pack(pady=5)

    def save_changes():
        try:
            new_x = float(x_entry.get())
            new_y = float(y_entry.get())
            on_save(index, new_x, new_y)
            edit_window.destroy()
        except ValueError:
            print("Введите корректные числовые значения!")

    Button(edit_window, text="Сохранить", command=save_changes).pack(pady=10)


def open_add_point_window(parent, on_save):
    add_window = Toplevel(parent)
    add_window.title("Добавить новую точку")

    Label(add_window, text="Добавить новую точку").pack(pady=5)

    Label(add_window, text="X:").pack()
    x_entry = Entry(add_window)
    x_entry.pack(pady=5)

    Label(add_window, text="Y:").pack()
    y_entry = Entry(add_window)
    y_entry.pack(pady=5)

    def save_new_point():
        try:
            new_x = float(x_entry.get())
            new_y = float(y_entry.get())
            on_save(new_x, new_y)
            add_window.destroy()
        except ValueError:
            print("Введите корректные числовые значения!")

    Button(add_window, text="Сохранить", command=save_new_point).pack(pady=10)


def open_ermit_window():
    ermit_window = Toplevel()
    ermit_window.title("Метод интерполяции Эрмита")
    ermit_window.geometry("630x600")

    frame_point2 = tk.Frame(ermit_window)
    frame_point2.pack(pady=5)

    # Поле ввода для граничного условия P1
    lbl_x2 = Label(frame_point2, text="P1 = [")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=5)
    entry_x2.pack(side=tk.LEFT, padx=5)
    entry_x22 = Entry(frame_point2, width=5)
    entry_x22.pack(side=tk.LEFT, padx=5)
    lbl_x22 = Label(frame_point2, text="]")
    lbl_x22.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия P4
    lbl_x4 = Label(frame_point2, text="P4 = [")
    lbl_x4.pack(side=tk.LEFT, padx=5)
    entry_x4 = Entry(frame_point2, width=5)
    entry_x4.pack(side=tk.LEFT, padx=5)
    entry_x42 = Entry(frame_point2, width=5)
    entry_x42.pack(side=tk.LEFT, padx=5)
    lbl_x42 = Label(frame_point2, text="]")
    lbl_x42.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия R1
    lbl_y2 = Label(frame_point2, text="R1 = [")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=5)
    entry_y2.pack(side=tk.LEFT, padx=5)
    entry_y22 = Entry(frame_point2, width=5)
    entry_y22.pack(side=tk.LEFT, padx=5)
    lbl_y22 = Label(frame_point2, text="]")
    lbl_y22.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия R4
    lbl_x4 = Label(frame_point2, text="R4 = [")
    lbl_x4.pack(side=tk.LEFT, padx=5)
    entry_x44 = Entry(frame_point2, width=5)
    entry_x44.pack(side=tk.LEFT, padx=5)
    entry_x24 = Entry(frame_point2, width=5)
    entry_x24.pack(side=tk.LEFT, padx=5)
    lbl_y42 = Label(frame_point2, text="]")
    lbl_y42.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(ermit_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(ermit_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    x_values, y_values = list(), list()

    # Функция обновления графика
    def refresh_graph():
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        ermit_graphic(x_values, y_values, canvas_frame, on_point_click)

    # Функция обработки клика на точке
    def on_point_click(index, x_vals, y_vals):
        open_edit_point_window(ermit_window, index, x_vals, y_vals, on_save)

    # Функция сохранения новых координат точки
    def on_save(index, new_x, new_y):
        x_values[index] = new_x
        y_values[index] = new_y
        refresh_graph()

    # Функция для добавления новой точки
    def on_add(new_x, new_y):
        x_values.append(new_x)
        y_values.append(new_y)
        refresh_graph()

    def on_ok():
        try:
            P1 = [entry_x2.get(), entry_x22.get()]
            P4 = [entry_x4.get(), entry_x42.get()]
            R1 = [entry_y2.get(), entry_y22.get()]
            R4 = [entry_x44.get(), entry_x24.get()]
            nonlocal x_values, y_values
            x_values, y_values = ermit(P1, P4, R1, R4)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            refresh_graph()
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(ermit_window, text="Построить график", command=on_ok)
    btn_ok.pack(pady=10)

    btn_add = Button(ermit_window, text="Добавить точку", command=lambda: open_add_point_window(ermit_window, on_add))
    btn_add.pack(pady=10)


def bezier_graphic(x_values, y_values, P1, P2, P3, P4, canvas, on_point_click):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(x_values, y_values, color="gray", linewidth=2)
    points2 = ax.scatter(x_values, y_values, color="red", s=30)

    control_points = [P1, P2, P3, P4]
    control_scatter = ax.scatter(*zip(*control_points), color="blue", s=50, picker=True)

    for i in range(len(control_points)):
        x_vals = [control_points[i][0], control_points[(i + 1) % len(control_points)][0]]
        y_vals = [control_points[i][1], control_points[(i + 1) % len(control_points)][1]]
        ax.plot(x_vals, y_vals, color="gray", linestyle="--", linewidth=1)

    def on_click(event):
        if event.inaxes == ax:
            cont, ind = points2.contains(event)
            if cont:
                point_index = ind["ind"][0]
                on_point_click(point_index, x_values, y_values, False)
            cont, ind = control_scatter.contains(event)
            if cont:
                control_index = ind["ind"][0]
                on_point_click(control_index, *zip(*control_points), True)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.mpl_connect("button_press_event", on_click)
    canvas_widget.draw()


def open_edit_point_window2(parent, index, x_vals, y_vals, on_save, is_control_point):
    edit_window = Toplevel(parent)
    edit_window.title("Редактирование точки")

    Label(edit_window, text="X:").pack()
    entry_x = Entry(edit_window)
    entry_x.pack()
    entry_x.insert(0, str(x_vals[index]))

    Label(edit_window, text="Y:").pack()
    entry_y = Entry(edit_window)
    entry_y.pack()
    entry_y.insert(0, str(y_vals[index]))

    def save():
        try:
            new_x = float(entry_x.get())
            new_y = float(entry_y.get())
            on_save(index, new_x, new_y, is_control_point)
            edit_window.destroy()
        except ValueError:
            print("Введите корректные числовые значения!")

    Button(edit_window, text="Сохранить", command=save).pack()


def open_bezier_window():
    bezier_window = Toplevel()
    bezier_window.title("Формы Безье")
    bezier_window.geometry("630x600")

    frame_point2 = tk.Frame(bezier_window)
    frame_point2.pack(pady=5)

    def create_point_input(label_text):
        lbl = Label(frame_point2, text=f"{label_text} = [")
        lbl.pack(side=tk.LEFT, padx=5)
        entry_x = Entry(frame_point2, width=5)
        entry_x.pack(side=tk.LEFT, padx=5)
        entry_y = Entry(frame_point2, width=5)
        entry_y.pack(side=tk.LEFT, padx=5)
        lbl_end = Label(frame_point2, text="]")
        lbl_end.pack(side=tk.LEFT, padx=5)
        return entry_x, entry_y

    entry_x2, entry_y2 = create_point_input("P1")
    entry_x4, entry_y4 = create_point_input("P2")
    entry_x3, entry_y3 = create_point_input("P3")
    entry_x5, entry_y5 = create_point_input("P4")

    canvas_frame = tk.Frame(bezier_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    x_values, y_values = [], []
    control_points = [(0, 0), (1, 1), (2, 1), (3, 0)]

    def refresh_graph():
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        bezier_graphic(
            x_values, y_values,
            control_points[0], control_points[1],
            control_points[2], control_points[3],
            canvas_frame, on_point_click
        )

    def on_point_click(index, x_vals, y_vals, is_control_point):
        open_edit_point_window2(bezier_window, index, x_vals, y_vals, on_save, is_control_point)

    def on_save(index, new_x, new_y, is_control_point):
        if is_control_point:
            control_points[index] = (new_x, new_y)
        else:
            x_values[index] = new_x
            y_values[index] = new_y
        refresh_graph()

    def on_add(new_x, new_y):
        x_values.append(new_x)
        y_values.append(new_y)
        refresh_graph()

    def on_ok():
        try:
            P1 = (float(entry_x2.get()), float(entry_y2.get()))
            P2 = (float(entry_x4.get()), float(entry_y4.get()))
            P3 = (float(entry_x3.get()), float(entry_y3.get()))
            P4 = (float(entry_x5.get()), float(entry_y5.get()))
            nonlocal x_values, y_values, control_points
            control_points = [P1, P2, P3, P4]
            x_values, y_values = bezier(P1, P2, P3, P4)
            refresh_graph()
        except ValueError:
            print("Введите корректные числовые значения!")

    Button(bezier_window, text="Построить график", command=on_ok).pack(pady=10)

    btn_add = Button(bezier_window, text="Добавить точку", command=lambda: open_add_point_window(bezier_window, on_add))
    btn_add.pack(pady=10)


def b_spline_graphic(x_values, y_values, canvas, on_point_click):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(x_values, y_values, color="gray", linewidth=2)
    points = ax.scatter(x_values, y_values, color="red", s=30)

    max_y = max(y_values)
    y_limit = max(1.0, (int(max_y * 10) + 1) / 10)
    ax.set_ylim(0, y_limit)
    yticks = [i / 10 for i in range(0, int(y_limit * 10) + 1)]
    ax.set_yticks(yticks)

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    def on_click(event):
        if event.inaxes == ax:
            cont, ind = points.contains(event)
            if cont:
                point_index = ind["ind"][0]
                on_point_click(point_index, x_values, y_values)

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.mpl_connect("button_press_event", on_click)
    canvas_widget.draw()


def open_b_spline_window():
    spline_window = Toplevel()
    spline_window.title("B-сплайн")
    spline_window.geometry("630x700")

    frame_point_count = tk.Frame(spline_window)
    frame_point_count.pack(pady=5)

    lbl_point_count = Label(frame_point_count, text="Количество точек:")
    lbl_point_count.pack(side=tk.LEFT, padx=5)
    entry_point_count = Entry(frame_point_count, width=5)
    entry_point_count.pack(side=tk.LEFT, padx=5)

    frame_points = tk.Frame(spline_window)
    frame_points.pack(pady=10)

    canvas_frame = tk.Frame(spline_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(spline_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    point_entries, x_values, y_values = list(), list(), list()

    # Функция обновления графика
    def refresh_graph():
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        b_spline_graphic(x_values, y_values, canvas_frame, on_point_click)

    # Функция обработки клика на точку
    def on_point_click(index, x_vals, y_vals):
        open_edit_point_window(spline_window, index, x_vals, y_vals, on_save)

    # Функция сохранения новых координат точки
    def on_save(index, new_x, new_y):
        x_values[index] = new_x
        y_values[index] = new_y

        refresh_graph()

    def on_add(new_x, new_y):
        x_values.append(new_x)
        y_values.append(new_y)
        refresh_graph()

    def create_point_inputs():
        nonlocal point_entries
        for widget in frame_points.winfo_children():
            widget.destroy()
        point_entries.clear()

        try:
            point_count = int(entry_point_count.get())
            if point_count < 2:
                raise ValueError("Должно быть хотя бы 2 точки.")

            for i in range(point_count):
                frame_point = tk.Frame(frame_points)
                frame_point.pack(pady=5)

                lbl_point = Label(frame_point, text=f"P{i + 1} = [")
                lbl_point.pack(side=tk.LEFT, padx=5)
                entry_x = Entry(frame_point, width=5)
                entry_x.pack(side=tk.LEFT, padx=5)
                entry_y = Entry(frame_point, width=5)
                entry_y.pack(side=tk.LEFT, padx=5)
                lbl_point_end = Label(frame_point, text="]")
                lbl_point_end.pack(side=tk.LEFT, padx=5)

                point_entries.append((entry_x, entry_y))
        except ValueError:
            print("Введите корректное количество точек!")

    def on_ok():
        try:
            points = []
            for entry_x, entry_y in point_entries:
                x = float(entry_x.get())
                y = float(entry_y.get())
                points.append((x, y))

            nonlocal x_values, y_values
            x_values, y_values = b_spline(points)
            refresh_graph()
        except ValueError:
            print("Введите корректные числовые значения для точек!")

    btn_set_points = Button(spline_window, text="Задать точки", command=create_point_inputs)
    btn_set_points.pack(pady=10)

    btn_ok = Button(spline_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)

    btn_add = Button(spline_window, text="Добавить точку", command=lambda: open_add_point_window(spline_window, on_add))
    btn_add.pack(pady=10)


# Функции с new - это функции с возможностью состыковки точек на графике
def new_ermit_graphic(x_values, y_values, canvas):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(x_values, y_values, color="gray", linewidth=2)
    points = ax.scatter(x_values, y_values, color="red", s=30)

    max_y = max(y_values)
    y_limit = max(1.0, (int(max_y * 10) + 1) / 10)
    ax.set_ylim(0, y_limit)
    yticks = [i / 10 for i in range(0, int(y_limit * 10) + 1)]
    ax.set_yticks(yticks)

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    selected_points = []

    def on_click(event):
        if event.inaxes == ax:
            cont, ind = points.contains(event)
            if cont:
                point_index = ind["ind"][0]
                selected_points.append(point_index)
                if len(selected_points) == 2:
                    p1_index, p2_index = selected_points
                    x1, y1 = x_values[p1_index], y_values[p1_index]
                    x2, y2 = x_values[p2_index], y_values[p2_index]
                    ax.plot([x1, x2], [y1, y2], color="gray", linewidth=2)
                    selected_points.clear()
                    canvas_widget.draw()

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.mpl_connect("button_press_event", on_click)
    canvas_widget.draw()


def open_new_ermit_window():
    ermit_window = Toplevel()
    ermit_window.title("Метод интерполяции Эрмита")
    ermit_window.geometry("630x600")

    frame_point2 = tk.Frame(ermit_window)
    frame_point2.pack(pady=5)

    # Поле ввода для граничного условия P1
    lbl_x2 = Label(frame_point2, text="P1 = [")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=5)
    entry_x2.pack(side=tk.LEFT, padx=5)
    entry_x22 = Entry(frame_point2, width=5)
    entry_x22.pack(side=tk.LEFT, padx=5)
    lbl_x22 = Label(frame_point2, text="]")
    lbl_x22.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия P4
    lbl_x4 = Label(frame_point2, text="P4 = [")
    lbl_x4.pack(side=tk.LEFT, padx=5)
    entry_x4 = Entry(frame_point2, width=5)
    entry_x4.pack(side=tk.LEFT, padx=5)
    entry_x42 = Entry(frame_point2, width=5)
    entry_x42.pack(side=tk.LEFT, padx=5)
    lbl_x42 = Label(frame_point2, text="]")
    lbl_x42.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия R1
    lbl_y2 = Label(frame_point2, text="R1 = [")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=5)
    entry_y2.pack(side=tk.LEFT, padx=5)
    entry_y22 = Entry(frame_point2, width=5)
    entry_y22.pack(side=tk.LEFT, padx=5)
    lbl_y22 = Label(frame_point2, text="]")
    lbl_y22.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия R4
    lbl_x4 = Label(frame_point2, text="R4 = [")
    lbl_x4.pack(side=tk.LEFT, padx=5)
    entry_x44 = Entry(frame_point2, width=5)
    entry_x44.pack(side=tk.LEFT, padx=5)
    entry_x24 = Entry(frame_point2, width=5)
    entry_x24.pack(side=tk.LEFT, padx=5)
    lbl_y42 = Label(frame_point2, text="]")
    lbl_y42.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(ermit_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(ermit_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    x_values, y_values = list(), list()

    # Функция обновления графика
    def refresh_graph():
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        new_ermit_graphic(x_values, y_values, canvas_frame)

    def on_ok():
        try:
            P1 = [entry_x2.get(), entry_x22.get()]
            P4 = [entry_x4.get(), entry_x42.get()]
            R1 = [entry_y2.get(), entry_y22.get()]
            R4 = [entry_x44.get(), entry_x24.get()]
            nonlocal x_values, y_values
            x_values, y_values = ermit(P1, P4, R1, R4)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            refresh_graph()
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(ermit_window, text="Построить график", command=on_ok)
    btn_ok.pack(pady=10)


def new_bezier_graphic(x_values, y_values, P1, P2, P3, P4, canvas):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(x_values, y_values, color="gray", linewidth=2)
    points2 = ax.scatter(x_values, y_values, color="red", s=30)

    points = [P1, P2, P3, P4]
    points = [(int(x), int(y)) for x, y in points]
    all_y_values = []
    all_y_values.extend(y_values)
    for i in range(len(points)):
        all_y_values.append(points[i][1])

    for i in range(len(points) - 1):
        x_vals = [points[i][0], points[i + 1][0]]
        y_vals = [points[i][1], points[i + 1][1]]
        ax.plot(x_vals, y_vals, color="gray", linestyle="--", linewidth=1)

    x_vals = [points[-1][0], points[0][0]]
    y_vals = [points[-1][1], points[0][1]]
    ax.plot(x_vals, y_vals, color="gray", linestyle="--", linewidth=1)

    max_y = max(all_y_values)
    y_limit = max(1.0, (int(max_y * 10) + 1) / 10)
    ax.set_ylim(0, y_limit)
    yticks = [i / 10 for i in range(0, int(y_limit * 10) + 1)]
    ax.set_yticks(yticks)

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    selected_points = []

    def on_click(event):
        if event.inaxes == ax:
            cont, ind = points2.contains(event)
            if cont:
                point_index = ind["ind"][0]
                selected_points.append(point_index)
                if len(selected_points) == 2:
                    p1_index, p2_index = selected_points
                    x1, y1 = x_values[p1_index], y_values[p1_index]
                    x2, y2 = x_values[p2_index], y_values[p2_index]
                    ax.plot([x1, x2], [y1, y2], color="gray", linewidth=2)
                    selected_points.clear()
                    canvas_widget.draw()

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.mpl_connect("button_press_event", on_click)
    canvas_widget.draw()


def open_new_bezier_window():
    bezier_window = Toplevel()
    bezier_window.title("Формы Безье")
    bezier_window.geometry("630x600")

    frame_point2 = tk.Frame(bezier_window)
    frame_point2.pack(pady=5)

    # Поле ввода для граничного условия P1
    lbl_x2 = Label(frame_point2, text="P1 = [")
    lbl_x2.pack(side=tk.LEFT, padx=5)
    entry_x2 = Entry(frame_point2, width=5)
    entry_x2.pack(side=tk.LEFT, padx=5)
    entry_x22 = Entry(frame_point2, width=5)
    entry_x22.pack(side=tk.LEFT, padx=5)
    lbl_x22 = Label(frame_point2, text="]")
    lbl_x22.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия P2
    lbl_x4 = Label(frame_point2, text="P2 = [")
    lbl_x4.pack(side=tk.LEFT, padx=5)
    entry_x4 = Entry(frame_point2, width=5)
    entry_x4.pack(side=tk.LEFT, padx=5)
    entry_x42 = Entry(frame_point2, width=5)
    entry_x42.pack(side=tk.LEFT, padx=5)
    lbl_x42 = Label(frame_point2, text="]")
    lbl_x42.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия P3
    lbl_y2 = Label(frame_point2, text="P3 = [")
    lbl_y2.pack(side=tk.LEFT, padx=5)
    entry_y2 = Entry(frame_point2, width=5)
    entry_y2.pack(side=tk.LEFT, padx=5)
    entry_y22 = Entry(frame_point2, width=5)
    entry_y22.pack(side=tk.LEFT, padx=5)
    lbl_y22 = Label(frame_point2, text="]")
    lbl_y22.pack(side=tk.LEFT, padx=5)

    # Поле ввода для граничного условия P4
    lbl_x4 = Label(frame_point2, text="P4 = [")
    lbl_x4.pack(side=tk.LEFT, padx=5)
    entry_x44 = Entry(frame_point2, width=5)
    entry_x44.pack(side=tk.LEFT, padx=5)
    entry_x24 = Entry(frame_point2, width=5)
    entry_x24.pack(side=tk.LEFT, padx=5)
    lbl_y42 = Label(frame_point2, text="]")
    lbl_y42.pack(side=tk.LEFT, padx=5)

    canvas_frame = tk.Frame(bezier_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(bezier_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    x_values, y_values, control_points = list(), list(), list()

    # Функция обновления графика
    def refresh_graph():
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        new_bezier_graphic(
            x_values, y_values,
            control_points[0], control_points[1],
            control_points[2], control_points[3],
            canvas_frame
        )

    def on_ok():
        try:
            P1 = [entry_x2.get(), entry_x22.get()]
            P2 = [entry_x4.get(), entry_x42.get()]
            P3 = [entry_y2.get(), entry_y22.get()]
            P4 = [entry_x44.get(), entry_x24.get()]
            nonlocal x_values, y_values, control_points
            control_points = [P1, P2, P3, P4]
            x_values, y_values = bezier(P1, P2, P3, P4)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            refresh_graph()
        except ValueError:
            print("Введите корректные числовые значения!")

    btn_ok = Button(bezier_window, text="Построить график", command=on_ok)
    btn_ok.pack(pady=10)


def new_b_spline_graphic(x_values, y_values, canvas):
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot(x_values, y_values, color="gray", linewidth=2)
    points = ax.scatter(x_values, y_values, color="red", s=30)

    max_y = max(y_values)
    y_limit = max(1.0, (int(max_y * 10) + 1) / 10)
    ax.set_ylim(0, y_limit)
    yticks = [i / 10 for i in range(0, int(y_limit * 10) + 1)]
    ax.set_yticks(yticks)

    ax.set_aspect('equal')
    ax.grid(visible=True, color="lightgray", linestyle="--", linewidth=0.5)

    selected_points = []

    def on_click(event):
        if event.inaxes == ax:
            cont, ind = points.contains(event)
            if cont:
                point_index = ind["ind"][0]
                selected_points.append(point_index)
                if len(selected_points) == 2:
                    p1_index, p2_index = selected_points
                    x1, y1 = x_values[p1_index], y_values[p1_index]
                    x2, y2 = x_values[p2_index], y_values[p2_index]
                    ax.plot([x1, x2], [y1, y2], color="gray", linewidth=2)
                    selected_points.clear()
                    canvas_widget.draw()

    canvas_widget = FigureCanvasTkAgg(figure, master=canvas)
    canvas_widget.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas_widget.mpl_connect("button_press_event", on_click)
    canvas_widget.draw()


def open_new_b_spline_window():
    spline_window = Toplevel()
    spline_window.title("B-сплайн")
    spline_window.geometry("630x600")

    frame_point_count = tk.Frame(spline_window)
    frame_point_count.pack(pady=5)

    # Поле ввода для количества точек
    lbl_point_count = Label(frame_point_count, text="Количество точек:")
    lbl_point_count.pack(side=tk.LEFT, padx=5)
    entry_point_count = Entry(frame_point_count, width=5)
    entry_point_count.pack(side=tk.LEFT, padx=5)

    frame_points = tk.Frame(spline_window)
    frame_points.pack(pady=10)

    canvas_frame = tk.Frame(spline_window, bg="white", width=300, height=200)
    canvas_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    info_label = tk.Label(spline_window, text="", font=("Arial", 12), justify="left")
    info_label.pack()

    point_entries, x_values, y_values = list(), list(), list()

    # Функция обновления графика
    def refresh_graph():
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        new_b_spline_graphic(x_values, y_values, canvas_frame)

    def create_point_inputs():
        nonlocal point_entries
        for widget in frame_points.winfo_children():
            widget.destroy()
        point_entries.clear()

        try:
            point_count = int(entry_point_count.get())
            if point_count < 2:
                raise ValueError("Должно быть хотя бы 2 точки.")

            for i in range(point_count):
                frame_point = tk.Frame(frame_points)
                frame_point.pack(pady=5)

                lbl_point = Label(frame_point, text=f"P{i + 1} = [")
                lbl_point.pack(side=tk.LEFT, padx=5)
                entry_x = Entry(frame_point, width=5)
                entry_x.pack(side=tk.LEFT, padx=5)
                entry_y = Entry(frame_point, width=5)
                entry_y.pack(side=tk.LEFT, padx=5)
                lbl_point_end = Label(frame_point, text="]")
                lbl_point_end.pack(side=tk.LEFT, padx=5)

                point_entries.append((entry_x, entry_y))
        except ValueError:
            print("Введите корректное количество точек!")

    def on_ok():
        try:
            points = []
            for entry_x, entry_y in point_entries:
                x = float(entry_x.get())
                y = float(entry_y.get())
                points.append((x, y))

            nonlocal x_values, y_values
            x_values, y_values = b_spline(points)
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            frame_point_count.pack_forget()
            frame_points.pack_forget()
            btn_set_points.pack_forget()
            btn_ok.pack_forget()
            refresh_graph()
        except ValueError:
            print("Введите корректные числовые значения для точек!")

    btn_set_points = Button(spline_window, text="Задать точки", command=create_point_inputs)
    btn_set_points.pack(pady=10)

    btn_ok = Button(spline_window, text="Ок", command=on_ok)
    btn_ok.pack(pady=10)


def create_window():
    root = tk.Tk()
    root.title("Графический редактор")
    root.geometry("600x300")

    # Панель инструментов
    toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)

    # Кнопка "Отрезки"
    btn_segments = tk.Menubutton(toolbar, text="Отрезки", relief=tk.RAISED)
    btn_segments.menu = Menu(btn_segments, tearoff=0)
    btn_segments["menu"] = btn_segments.menu

    # Опции в "Отрезки"
    btn_segments.menu.add_command(label="Алгоритм ЦДА", command = lambda: open_cda_window())
    btn_segments.menu.add_command(label="Алгоритм Брезенхема", command = lambda: open_brezenhem_window())
    btn_segments.menu.add_command(label="Алгоритм Ву", command = lambda: open_wu_window())
    btn_segments.pack(side=tk.LEFT, padx=2, pady=2)

    # Кнопка "Отладочный режим"
    btn_segmentss = tk.Menubutton(toolbar, text="Отладочный режим", relief=tk.RAISED)
    btn_segmentss.menu = Menu(btn_segmentss, tearoff=0)
    btn_segmentss["menu"] = btn_segmentss.menu

    # Опции в "Отладочный режим"
    btn_segmentss.menu.add_command(label="Алгоритм Брезенхема", command = lambda: open_brezenhem_debug_window())
    btn_segmentss.menu.add_command(label="Алгоритм Ву", command = lambda: open_wu_debug_window())
    btn_segmentss.menu.add_command(label="Окружность", command=lambda: open_circle_debug_window())
    btn_segmentss.menu.add_command(label="Эллипс", command=lambda: open_ellips_debug_window())
    btn_segmentss.menu.add_command(label="Парабола", command=lambda: open_parabola_debug_window())
    btn_segmentss.menu.add_command(label="Гипербола", command=lambda: open_hyperbola_debug_window())
    btn_segmentss.pack(side=tk.LEFT, padx=2, pady=2)

    # Кнопка "Линии второго порядка"
    btn_segments2 = tk.Menubutton(toolbar, text="Линии второго порядка", relief=tk.RAISED)
    btn_segments2.menu = Menu(btn_segments2, tearoff=0)
    btn_segments2["menu"] = btn_segments2.menu

    # Опции в "Линии второго порядка"
    btn_segments2.menu.add_command(label="Окружность", command=lambda: open_circle_window())
    btn_segments2.menu.add_command(label="Эллипс", command=lambda:open_ellips_window())
    btn_segments2.menu.add_command(label="Гипербола", command=lambda:open_hyperbola_window())
    btn_segments2.menu.add_command(label="Парабола", command=lambda:open_parabola_window())
    btn_segments2.pack(side=tk.LEFT, padx=2, pady=2)

    # Кнопка "Кривые"
    btn_segments3 = tk.Menubutton(toolbar, text="Кривые", relief=tk.RAISED)
    btn_segments3.menu = Menu(btn_segments3, tearoff=0)
    btn_segments3["menu"] = btn_segments3.menu

    # Опции в "Кривые"
    btn_segments3.menu.add_command(label="Кривая Эрмита", command=lambda: open_ermit_window())
    btn_segments3.menu.add_command(label="Кривая Безье", command=lambda:open_bezier_window())
    btn_segments3.menu.add_command(label="B-сплайн", command=lambda:open_b_spline_window())
    btn_segments3.pack(side=tk.LEFT, padx=2, pady=2)

    toolbar.pack(side=tk.TOP, fill=tk.X)

    label = Label(root, text="Генерация отрезков", font=("Arial", 14))
    label.pack(pady=10)

    button_frame = Frame(root)
    button_frame.pack()

    btn1 = Button(button_frame, text="Алгоритм ЦДА", command=open_cda_window)
    btn1.pack(side="left", padx=5)

    btn2 = Button(button_frame, text="Алгоритм Брезенхема", command=open_brezenhem_window)
    btn2.pack(side="left", padx=5)

    btn3 = Button(button_frame, text="Алгоритм Ву", command=open_wu_window)
    btn3.pack(side="left", padx=5)

    label2 = Label(root, text="Построение линий второго порядка", font=("Arial", 14))
    label2.pack(pady=10)

    button_frame = Frame(root)
    button_frame.pack()

    btn4 = Button(button_frame, text="Окружность", command=open_circle_window)
    btn4.pack(side="left", padx=5)

    btn5 = Button(button_frame, text="Эллипс", command=open_ellips_window)
    btn5.pack(side="left", padx=5)

    btn6 = Button(button_frame, text="Гипербола", command=open_hyperbola_window)
    btn6.pack(side="left", padx=5)

    btn7 = Button(button_frame, text="Парабола", command=open_parabola_window)
    btn7.pack(side="left", padx=5)

    label3 = Label(root, text="Построение параметрических кривых", font=("Arial",14))
    label3.pack(pady=10)

    button_frame = Frame(root)
    button_frame.pack()

    btn8 = Button(button_frame, text="Метод Эрмита", command=open_ermit_window)
    btn8.pack(side="left", padx=5)

    btn9 = Button(button_frame, text="Метод Безье", command=open_bezier_window)
    btn9.pack(side="left", padx=5)

    btn10 = Button(button_frame, text="B-сплайн", command=open_b_spline_window)
    btn10.pack(side="left", padx=5)

    root.mainloop()


if __name__ == "__main__":
    create_window()
