import matplotlib.pyplot as plt
from matplotlib.path import Path
import math


def vector_multiplic(vector1: list, vector2: list) -> list:
    vector3 = [vector1[1] * vector2[2] - vector1[2] * vector2[1], vector1[0] * vector2[2] - vector1[2] * vector2[0], vector1[0] * vector2[1] - vector1[1] * vector2[0]]
    return vector3


def find_bisector(point1: list, point2: list) -> list:
    x0, y0 = (float(point1[0]) + float(point2[0])) / 2, (float(point1[1]) + float(point2[1])) / 2
    a, b = point2[0] - point1[0], point2[1] - point1[1]
    c = a * x0 * (-1) - b * y0
    return [a, b, c]


def find_intersections(points: list, line_coeffs: list) -> list:
    intersections = []
    u, v = line_coeffs, [points[0][1] - points[1][1], points[1][0] - points[0][0], points[0][0] * points[1][1] - points[1][0] * points[0][1]]
    z = vector_multiplic(u, v)
    if z[2] != 0:
        intersections.append(z[0] / z[2])
        intersections.append(z[1] / z[2])
    return intersections


def find_intersection_with_polygon(polygon: list, line_coeffs: list) -> list:
    a, b, c = line_coeffs
    intersections = []
    n = len(polygon)
    eps = 1e-9
    def already_exists(p, points_list):
        for pt in points_list:
            if math.isclose(pt[0], p[0], abs_tol=eps) and math.isclose(pt[1], p[1], abs_tol=eps):
                return True
        return False
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        denom = a * dx + b * dy
        if abs(denom) < eps:
            if math.isclose(a * x1 + b * y1 + c, 0, abs_tol=eps):
                if not already_exists([x1, y1], intersections):
                    intersections.append([x1, y1])
                if not already_exists([x2, y2], intersections):
                    intersections.append([x2, y2])
            continue
        t = - (a * x1 + b * y1 + c) / denom
        if 0 <= t <= 1:
            x_inter = x1 + t * dx
            y_inter = y1 + t * dy
            pt = [x_inter, y_inter]
            if not already_exists(pt, intersections):
                intersections.append(pt)
    return intersections


def point_on_segment(p, a, b, eps=1e-9):
    ax, ay = a
    bx, by = b
    px, py = p
    cross = (px - ax) * (by - ay) - (py - ay) * (bx - ax)
    if abs(cross) > eps:
        return False
    dot = (px - ax) * (bx - ax) + (py - ay) * (by - ay)
    if dot < -eps:
        return False
    sq_len = (bx - ax) ** 2 + (by - ay) ** 2
    if dot - sq_len > eps:
        return False
    return True


def find_point_position(point, polygon):
    n = len(polygon)
    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]
        if point_on_segment(point, a, b):
            if abs(point[0] - a[0]) < 1e-9 and abs(point[1] - a[1]) < 1e-9:
                return i, 0.0
            dx = b[0] - a[0]
            dy = b[1] - a[1]
            if abs(dx) >= abs(dy):
                t = (point[0] - a[0]) / dx if dx != 0 else 0.0
            else:
                t = (point[1] - a[1]) / dy if dy != 0 else 0.0
            return i, t
    raise ValueError("Точка {} не принадлежит границе многоугольника".format(point))


def cut_polygon(poly, pt1, pt2):
    i1, t1 = find_point_position(pt1, poly)
    i2, t2 = find_point_position(pt2, poly)
    n = len(poly)
    result = [pt1]
    if i1 == i2:
        if t2 > t1:
            result.append(pt2)
        else:
            current_index = (i1 + 1) % n
            while current_index != i1:
                result.append(poly[current_index])
                current_index = (current_index + 1) % n
                if current_index == i2:
                    break
            result.append(pt2)
        return result
    current_index = (i1 + 1) % n
    while current_index != i2:
        result.append(poly[current_index])
        current_index = (current_index + 1) % n
    if not math.isclose(t2, 0.0, abs_tol=1e-9):
        result.append(poly[i2])
    result.append(pt2)
    return result


def diagram(points: list):
    points_edges = points
    points_edges.append(points_edges[0])
    cells = list()
    xs, ys = [int(el[0]) for el in points], [int(el[1]) for el in points]
    padding = 0.5
    x_min, x_max, y_min, y_max = min(xs), max(xs), min(ys), max(ys)
    box = [[x_min - padding, y_max + padding], [x_max + padding, y_max + padding], [x_max + padding, y_min - padding], [x_min - padding, y_min - padding]]
    for point in points:
        cell = box
        for point2 in points:
            if point2 != point:
                b = find_bisector(point, point2)
                print(b)
                intersections = find_intersection_with_polygon(cell, b)
                print(intersections)
                if len(intersections) == 2:
                    newCell = cut_polygon(cell, intersections[0], intersections[1])
                    print(newCell)
                    if not Path(newCell).contains_point(point):
                        newCell = cut_polygon(cell, intersections[1], intersections[0])
                    cell = newCell
            else:
                continue
        cells.append(cell)
    return cells, box


def main():
    points = [[1,3], [2,2], [3,4], [2,1]]
    voronoi, box = diagram(points)
    print(voronoi)
    fig, ax = plt.subplots()
    for cell in voronoi:
        polygon = cell + [cell[0]]
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        ax.plot(xs, ys, marker='o')
    box_polygon = box + [box[0]]
    xs_box = [p[0] for p in box_polygon]
    ys_box = [p[1] for p in box_polygon]
    ax.plot(xs_box, ys_box, marker='o', color='green', linestyle='--')
    ax.scatter(*zip(*points), color='red')
    plt.show()
    print(cut_polygon([[0.5,0.5],[0.5,4.5],[3.5,4.5],[3.5,0.5]], [1.5, 4.5], [3, 0.5]))


if __name__ == '__main__':
    main()

