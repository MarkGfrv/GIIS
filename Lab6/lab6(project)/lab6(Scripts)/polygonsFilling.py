import matplotlib.pyplot as plt
from lab5Scripts.polygonsConstruct import find_max_point, point_in_polygon


def find_intersect(x_coords: list, y_coords: list) -> list:
    x1, y1, x2, y2, result = x_coords[0], y_coords[0], x_coords[1], y_coords[1], list()
    if y1 == y2:
        return []
    for i in range(0, max(y1, y2) + 1):
        if min(y1,y2) <= i <= max(y1,y2):
            t = (i - y1) / (y2 - y1)
            if t < 0 or t > 1:
                continue
            x_intersect = x1 + (x2 - x1) * t
            result.append([x_intersect, i])
    return result


def find_intersect_with_concrete_line(x_coords: list, y_coords: list, line_y: int) -> list:
    x1, y1, x2, y2 = x_coords[0], y_coords[0], x_coords[1], y_coords[1]
    if y1 == y2:
        return []
    t = (line_y - y1) / (y2 - y1)
    if t < 0 or t > 1:
        return []
    x_intersect = x1 + (x2 - x1) * t
    result = [line_y, x_intersect]
    return result


def split_into_pairs(lst):
    pairs = [lst[i:i+2] for i in range(0, len(lst), 2)]
    if pairs and len(pairs[-1]) == 1:
        pairs[-1].append(pairs[-1][0])
    return pairs


def is_point_in_polygon(x, y, polygon):
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]
    for i in range(1, n):
        p2x, p2y = polygon[i]
        if (p1y > y) != (p2y > y):
            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if x < xinters:
                inside = not inside
        p1x, p1y = p2x, p2y
    return inside


class PolygonsFilling:
    def __init__(self, polygon: list):
        self.pol = polygon

    def with_ordered_list_of_edges(self) -> list:
        intersections, intervals = [], []
        self.pol.append(self.pol[0])
        for i in range(len(self.pol) - 1):
            is_list = False
            temp_results = find_intersect([self.pol[i][0], self.pol[i + 1][0]], [self.pol[i][1], self.pol[i + 1][1]])
            for i in range(len(temp_results)):
                if isinstance(temp_results[i], list):
                    is_list = True
            if is_list:
                intersections.extend(temp_results)
            else:
                intersections.append(temp_results)
        intersections = [el for el in intersections if el]
        sorted_intersections = sorted(intersections, key=lambda x: (x[1], x[0]))
        intervals = split_into_pairs(sorted_intersections)
        return intervals

    def ordered_list_using_active_edges(self) -> list:
        self.pol.append(self.pol[0])
        sap, upgraded_sap = dict(), dict()
        intervals = []
        x_values, y_values = [el[0] for el in self.pol], [el[1] for el in self.pol]
        max_x, max_y, max_index = find_max_point(x_values, y_values)
        for i in range(1, max_y + 1):
            temp_list = []
            for j in range(len(self.pol) - 1):
                if self.pol[j][1] == self.pol[j+1][1]:
                    continue
                intersection_points = find_intersect_with_concrete_line([self.pol[j][0], self.pol[j+1][0]], [self.pol[j][1], self.pol[j+1][1]], i)
                temp_list.append(intersection_points[::-1])
            sap[i] = temp_list
        upgraded_sap = {key: [item for item in value if item] for key, value in sap.items()}
        sorted_sap = dict(sorted(upgraded_sap.items(), reverse=True))
        for key in sorted_sap:
            sorted_sap[key].sort(key=lambda x: (x[0], x[1]))
        values = list(sorted_sap.values())
        for i in range(len(values)):
            if len(values[i]) <= 2:
                intervals.append(values[i])
            else:
                pairs = split_into_pairs(values[i])
                for j in range(len(pairs)):
                    intervals.append(pairs[j])
        return intervals

    def simple_seeded_filling(self, pixel: list):
        filled_pixels, stack, visited = [], [(pixel[0], pixel[1])], set()
        self.pol.append(self.pol[0])
        xs, ys = [el[0] for el in self.pol], [el[1] for el in self.pol]
        max_x, min_x, max_y, min_y = int(max(xs)), int(min(xs)), int(max(ys)), int(min(ys))
        if not is_point_in_polygon(pixel[0], pixel[1], self.pol):
            print("Затравочная точка вне полигона!")
            return []
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if x < min_x or x > max_x or y < min_y or y > max_y:
                continue
            if is_point_in_polygon(x, y, self.pol):
                filled_pixels.append((x, y))
                stack.append((x, y + 1))
                stack.append((x - 1, y))
                stack.append((x, y - 1))
                stack.append((x + 1, y))
        return filled_pixels

    def seeded_filling_line_by_line(self, pixel: list):
        filled_pixels, stack = set(), [(pixel[0], pixel[1])]
        self.pol.append(self.pol[0])
        xs, ys = [el[0] for el in self.pol], [el[1] for el in self.pol]
        max_x, min_x, max_y, min_y = int(max(xs)), int(min(xs)), int(max(ys)), int(min(ys))
        while stack:
            x, y = stack.pop()
            if (x, y) in filled_pixels:
                continue
            x_left = x
            while x_left > min_x and is_point_in_polygon(x_left - 1, y, self.pol) and ((x_left - 1, y) not in filled_pixels):
                x_left -= 1
            x_right = x
            while x_right < max_x and is_point_in_polygon(x_right + 1, y, self.pol) and ((x_right + 1, y) not in filled_pixels):
                x_right += 1
            for xi in range(x_left, x_right + 1):
                filled_pixels.add((xi, y))
            for ny in [y - 1, y + 1]:
                if ny < min_y or ny > max_y:
                    continue
                xi = x_left
                while xi <= x_right:
                    if is_point_in_polygon(xi, ny, self.pol) and ((xi, ny) not in filled_pixels):
                        stack.append((xi, ny))
                        xi_temp = xi + 1
                        while xi_temp <= x_right and is_point_in_polygon(xi_temp, ny, self.pol) and (
                                (xi_temp, ny) not in filled_pixels):
                            xi_temp += 1
                        xi = xi_temp
                    else:
                        xi += 1
        return list(filled_pixels)

    def draw_by_intervals(self, intervals: list):
        fig, ax = plt.subplots()
        x_all = []
        y_all = []
        for interval in intervals:
            x_start, y = interval[0]
            x_end, _ = interval[1]
            x_all.extend([x_start, x_end])
            y_all.append(y)
            for x in range(int(x_start), int(x_end) + 1):
                rect = plt.Rectangle((x, y), 1, 1, color='blue', ec='black')
                ax.add_patch(rect)
        if x_all:
            ax.set_xlim(min(x_all) - 1, max(x_all) + 2)
        if y_all:
            ax.set_ylim(min(y_all) - 1, max(y_all) + 2)
        ax.set_aspect('equal', adjustable='box')
        plt.title("Закрашенные интервалы")
        plt.show()

    def draw_by_pixels(self, pixels: list):
        fig, ax = plt.subplots()
        x_all = []
        y_all = []
        for (x, y) in pixels:
            x_all.append(x)
            y_all.append(y)
            rect = plt.Rectangle((x, y), 1, 1, color='blue', ec='black')
            ax.add_patch(rect)
        if x_all:
            ax.set_xlim(min(x_all) - 1, max(x_all) + 2)
        if y_all:
            ax.set_ylim(min(y_all) - 1, max(y_all) + 2)
        ax.set_aspect('equal', adjustable='box')
        plt.title("Закрашенные пиксели")
        plt.show()

    def debug_ordered_list_of_edges(self):
        if self.pol[0] != self.pol[-1]:
            self.pol.append(self.pol[0])
        xs = [p[0] for p in self.pol]
        ys = [p[1] for p in self.pol]
        min_y = int(min(ys))
        max_y = int(max(ys))
        debug_intervals = []
        for i in range(min_y, max_y + 1):
            line_intersections = []
            for j in range(len(self.pol) - 1):
                p1, p2 = self.pol[j], self.pol[j+1]
                if p1[1] == p2[1]:
                    continue
                ip = find_intersect_with_concrete_line([p1[0], p2[0]], [p1[1], p2[1]], i)
                if ip:
                    reversed_ip = ip[::-1]
                    line_intersections.append(reversed_ip)
            if line_intersections:
                line_intersections.sort(key=lambda x: (x[0], x[1]))
                if len(line_intersections) % 2 != 0:
                    if len(line_intersections) == 1:
                        intervals = [[line_intersections[0], line_intersections[0]]]
                    else:
                        line_intersections = line_intersections[:-1]
                        intervals = split_into_pairs(line_intersections)
                else:
                    intervals = split_into_pairs(line_intersections)
                debug_intervals.extend(intervals)
                yield debug_intervals.copy()
            else:
                yield debug_intervals.copy()
        yield debug_intervals.copy()

    def debug_ordered_list_using_active_edges(self):
        if self.pol[0] != self.pol[-1]:
            self.pol.append(self.pol[0])
        xs = [p[0] for p in self.pol]
        ys = [p[1] for p in self.pol]
        max_y = int(max(ys))
        min_y = int(min(ys))
        debug_intervals = []
        sap = {}
        for i in range(max_y, min_y - 1, -1):
            temp_list = []
            for j in range(len(self.pol) - 1):
                p1, p2 = self.pol[j], self.pol[j + 1]
                if p1[1] == p2[1]:
                    continue
                ip = find_intersect_with_concrete_line([p1[0], p2[0]], [p1[1], p2[1]], i)
                if ip:
                    reversed_ip = ip[::-1]
                    temp_list.append(reversed_ip)
            sap[i] = temp_list
            print(f"[debug_active_edges] Scanline y={i}, raw intersections: {temp_list}")
            upgraded = [item for item in temp_list if item]
            upgraded.sort(key=lambda x: (x[0], x[1]))
            print(f"[debug_active_edges] Scanline y={i}, sorted intersections: {upgraded}")
            if upgraded:
                if len(upgraded) % 2 != 0:
                    if len(upgraded) == 1:
                        intervals = [[upgraded[0], upgraded[0]]]
                    else:
                        upgraded = upgraded[:-1]
                        intervals = split_into_pairs(upgraded)
                else:
                    intervals = split_into_pairs(upgraded)
                print(f"[debug_active_edges] Scanline y={i}, intervals: {intervals}")
                debug_intervals.extend(intervals)
                yield debug_intervals.copy()
            else:
                yield debug_intervals.copy()
        yield debug_intervals.copy()

    def debug_simple_seeded_filling(self, seed: list):
        filled_pixels = []
        stack = [tuple(seed)]
        visited = set()
        self.pol.append(self.pol[0])
        xs, ys = [p[0] for p in self.pol], [p[1] for p in self.pol]
        max_x, min_x = int(max(xs)), int(min(xs))
        max_y, min_y = int(max(ys)), int(min(ys))
        if not is_point_in_polygon(seed[0], seed[1], self.pol):
            print("Затравочная точка вне полигона!")
            yield filled_pixels
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if x < min_x or x > max_x or y < min_y or y > max_y:
                continue
            if is_point_in_polygon(x, y, self.pol):
                filled_pixels.append((x, y))
                yield filled_pixels.copy()
                stack.extend([(x, y + 1), (x - 1, y), (x, y - 1), (x + 1, y)])
        yield filled_pixels.copy()

    def debug_seeded_filling_line_by_line(self, seed: list):
        filled_pixels = set()
        stack = [tuple(seed)]
        if self.pol[0] != self.pol[-1]:
            self.pol.append(self.pol[0])
        xs, ys = zip(*self.pol)
        max_x, min_x = int(max(xs)), int(min(xs))
        max_y, min_y = int(max(ys)), int(min(ys))
        while stack:
            x, y = stack.pop()
            if (x, y) in filled_pixels:
                continue
            x_left = x
            while x_left > min_x and is_point_in_polygon(x_left - 1, y, self.pol) and (
                    (x_left - 1, y) not in filled_pixels):
                x_left -= 1
            x_right = x
            while x_right < max_x and is_point_in_polygon(x_right + 1, y, self.pol) and (
                    (x_right + 1, y) not in filled_pixels):
                x_right += 1
            for xi in range(x_left, x_right + 1):
                filled_pixels.add((xi, y))
            yield list(filled_pixels)
            for ny in [y - 1, y + 1]:
                if ny < min_y or ny > max_y:
                    continue
                xi = x_left
                while xi <= x_right:
                    if is_point_in_polygon(xi, ny, self.pol) and ((xi, ny) not in filled_pixels):
                        stack.append((xi, ny))
                        xi_temp = xi + 1
                        while xi_temp <= x_right and is_point_in_polygon(xi_temp, ny, self.pol) and (
                                (xi_temp, ny) not in filled_pixels):
                            xi_temp += 1
                        xi = xi_temp
                    else:
                        xi += 1
        yield list(filled_pixels)


def main():
    pf = PolygonsFilling([[1, 1], [8, 1], [8, 5], [4, 3], [1, 6]])
    pf2 = PolygonsFilling([[0, 0], [9, 0], [9, 5], [5, 1], [3, 3]])
    pf3 = PolygonsFilling([[2, 1], [5, 1], [7, 4], [4, 7], [1, 5]])
    print(pf.ordered_list_using_active_edges())
    print(pf2.with_ordered_list_of_edges())
    print(pf3.simple_seeded_filling([3, 3]))
    print(split_into_pairs([1,2,3,4,5]))
    pf.draw_by_intervals(pf.ordered_list_using_active_edges())
    pf.draw_by_intervals(pf.with_ordered_list_of_edges())
    pf.draw_by_pixels(pf.seeded_filling_line_by_line([5, 2]))
    pf.draw_by_intervals(pf2.with_ordered_list_of_edges())
    pf.draw_by_pixels(pf3.simple_seeded_filling([3, 3]))
    pf.draw_by_pixels(pf3.seeded_filling_line_by_line([5, 2]))


if __name__ == '__main__':
    main()


