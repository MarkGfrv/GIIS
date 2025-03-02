import numpy as np
import matplotlib.pyplot as plt


def generate_points(n):
    points = np.random.rand(n,2) * 100
    return points


def big_triangle(points):
    minx = np.min(points[:, 0])
    maxx = np.max(points[:, 0])
    miny = np.min(points[:, 1])
    maxy = np.max(points[:, 1])

    dx = maxx - minx
    dy = maxy - miny
    dxy = max(dx, dy)

    midx = dx * 0.5 + minx
    midy = dy * 0.5 + miny

    return np.array([
        [midx - 10 * dxy, midy - 10 * dxy],
        [midx, midy + 10 * dxy],
        [midx + 10 * dxy, midy - 10 * dxy]
    ])


def circumcircle_of_triangle(points, v1, v2, v3):
    x1, y1 = points[v1]
    x2, y2 = points[v2]
    x3, y3 = points[v3]

    dy12 = abs(y1 - y2)
    dy23 = abs(y2 - y3)

    if dy12 < 1e-7:
        m2 = -((x3 - x2) / (y3 - y2))
        mx2, my2 = (x2 + x3) / 2, (y2 + y3) / 2
        xc = (x1 + x2) / 2
        yc = m2 * (xc - mx2) + my2
    elif dy23 < 1e-7:
        m1 = -((x2 - x1) / (y2 - y1))
        mx1, my1 = (x1 + x2) / 2, (y1 + y2) / 2
        xc = (x2 + x3) / 2
        yc = m1 * (xc - mx1) + my1
    else:
        m1 = -((x2 - x1) / (y2 - y1))
        m2 = -((x3 - x2) / (y3 - y2))
        mx1, my1 = (x1 + x2) / 2, (y1 + y2) / 2
        mx2, my2 = (x2 + x3) / 2, (y2 + y3) / 2
        xc = (m1 * mx1 - m2 * mx2 + my2 - my1) / (m1 - m2)
        if dy12 > dy23:
            yc = m1 * (xc - mx1) + my1
        else:
            yc = m2 * (xc - mx2) + my2

    dx = x2 - xc
    dy = y2 - yc
    r = dx * dx + dy * dy
    return {'a': v1, 'b': v2, 'c': v3, 'x': xc, 'y': yc, 'r': r}


def delete_multiples_edges(edges):
    i = 0
    while i < len(edges) - 1:
        a, b = edges[i], edges[i + 1]
        j = i + 2
        while j < len(edges) - 1:
            n, m = edges[j], edges[j + 1]
            if (a == n and b == m) or (a == m and b == n):
                edges = edges[:i] + edges[i + 2:j] + edges[j + 2:]
                break
            j += 2
        i += 2
    return edges


def triangulate(points):
    n = len(points)
    if n < 3:
        return []
    points = points.copy()
    ind = np.argsort(points[:, 0])
    big = big_triangle(points)
    points = np.vstack([points, big])
    cur_points = [circumcircle_of_triangle(points, n, n + 1, n + 2)]
    ans = []
    edges = []

    for i in range(len(ind) - 1, -1, -1):
        for j in range(len(cur_points) - 1, -1, -1):
            dx = points[ind[i], 0] - cur_points[j]['x']
            if dx > 0 and dx * dx > cur_points[j]['r']:
                ans.append(cur_points[j])
                cur_points.pop(j)
                continue
            dy = points[ind[i], 1] - cur_points[j]['y']
            if dx * dx + dy * dy - cur_points[j]['r'] > 1e-7:
                continue
            edges.extend(
                [cur_points[j]['a'], cur_points[j]['b'], cur_points[j]['b'], cur_points[j]['c'], cur_points[j]['c'],
                 cur_points[j]['a']])
            cur_points.pop(j)
        edges = delete_multiples_edges(edges)
        for j in range(0, len(edges), 2):
            a, b = edges[j], edges[j + 1]
            cur_points.append(circumcircle_of_triangle(points, a, b, ind[i]))
        edges = []
    for triangle in cur_points:
        ans.append(triangle)
    tr = []
    for triangle in ans:
        if triangle['a'] < n and triangle['b'] < n and triangle['c'] < n:
            tr.extend([triangle['a'], triangle['b'], triangle['c']])

    return tr


def main():
    size = int(input("Введите количество точек:"))
    pts = generate_points(size)
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    triangles = triangulate(pts)
    ax.scatter(pts[:, 0], pts[:, 1], color='blue')

    for i in range(0, len(triangles), 3):
        x = [pts[triangles[i], 0], pts[triangles[i + 1], 0], pts[triangles[i + 2], 0], pts[triangles[i], 0]]
        y = [pts[triangles[i], 1], pts[triangles[i + 1], 1], pts[triangles[i + 2], 1], pts[triangles[i], 1]]
        ax.plot(x, y, color='black')
    plt.show()


if __name__ == '__main__':
    main()


