from line import Line
from functions.rectangle import Rectangle
from math import acos, sqrt, degrees, radians, pi

X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2

delta = 0.00000001

def find_overlapping_segments_by_axis(axis_index_set, lines_array):
    result_set = {}
    lines_set = set(lines_array)
    for line in lines_set:
        for another in lines_set-{line, }:
            flag = True
            for axis_index in axis_index_set:
                if len(line[0])<axis_index:
                    flag = flag and line[0][axis_index] == line[1][axis_index] == another[0][axis_index] == another[1][axis_index]
                else:
                    flag = False
            if flag:
                result_set.update({line, another})
    return result_set


def get_all_axis_values_by_axis(axis_index, lines_array):
    if len(lines_array[0][0]) < axis_index:
        return set(points[axis_index] for points in set(lines[0] for lines in lines_array) | set((lines[1] for lines in lines_array)))
    else:
        return {}


def is_in(v, any_range):
    l = min(any_range)
    h = max(any_range)
    return l <= v <= h


def collapsing_lines():
    pass


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def concatenate2d(func_array):

    lines_array = list()
    [lines_array.extend(figure.lines) for figure in func_array]
    lines_array = list(set(lines_array))

    matches_x = find_overlapping_segments_by_axis((X_AXIS, ), lines_array)
    matches_y = find_overlapping_segments_by_axis((Y_AXIS, ), lines_array)
    matches_z = find_overlapping_segments_by_axis((Z_AXIS, ), lines_array)

    # for matches
    x_list = get_all_axis_values_by_axis(X_AXIS, lines_array)
    y_list = get_all_axis_values_by_axis(Y_AXIS, lines_array)
    z_list = get_all_axis_values_by_axis(Z_AXIS, lines_array)

    lines_array = set(lines_array)

    mach_lines = list()
    for x in x_list:
        # collect all lines with equal x value - values from all overlapping lines
        lines_by_x = tuple((lines for lines in matches_x if lines[0][0] == lines[1][0] == x))

        # collect all unique y-axis values
        y_set = set(tuple((lines[0][1] for lines in lines_by_x)) + tuple((lines[1][1] for lines in lines_by_x)))
        y_set = list(y_set)
        y_set.sort()

        c = 1

        while c < y_set.__len__():
            for line in lines_by_x:
                v = mean((y_set[c], y_set[c-1]))
                if is_in(v, (line[0][1], line[1][1])):
                    lines_array = lines_array.difference({line, })
                    mach_lines.append(Line((x, y_set[c]), (x, y_set[c-1])))
                    break
            c += 1

    lines_array = set(lines_array).union(set(mach_lines))

    return lines_array


def dot_product(a,b):
    return sum([a[i]*b[i] for i in range(len(a))])


def vector_len(a):
    return sqrt(sum([a[i]*a[i] for i in range(len(a))]))


def angle_vector(a, b, deg_precision=5):
    d = vector_len(a)*vector_len(b)
    if d != 0:
        r = dot_product(a, b) / d
    else:
        return 0
    if (-1.0-delta) <= r <= (-1.0 + delta):
        return pi
    else:
        return radians(round(degrees(acos(r)), deg_precision))


def line2vec(a):
    return tuple((a[0][i]-a[1][i] for i in range(len(a[0]))))


def angle_lines(a, b, deg_precision=5):
    v1 = line2vec(a)
    v2 = line2vec(b)
    return radians(round(degrees(acos(dot_product(v1, v2) / (vector_len(v1)*vector_len(v2)))), deg_precision))


def point_on_straight(p,line):
    vA = line2vec((p, line[0]))
    vB = line2vec((p, line[1]))
    a = angle_vector(vA, vB)
    return a == 0 or a == pi


def point_in_segment(p, segment):
    vA = line2vec((p, segment[0]))
    vB = line2vec((p, segment[1]))
    return point_on_straight(p, segment) and (dot_product(vA, vB) <= 0 + delta)


if __name__ == '__main__':

    assert( concatenate2d({Rectangle(1, ((0, 0), (5, 5))), Rectangle(1, ((5, 3), (10, 8)))}) == {((5, 0), (0, 0)), ((5, 8), (10, 8)), ((0, 0), (0, 5)), ((10, 3), (5, 3)), ((0, 5), (5, 5)), ((10, 8), (10, 3)), ((5, 5), (5, 0)), ((5, 3), (5, 8))})
    assert (degrees(angle_vector( (1.0, 2.0), (2.0, 1.0))) == 36.8699)
    assert (degrees(angle_lines ( ((0.0, 0.0), (1.0, 2.0)), ((0.0, 0.0), (2.0, 1.0)) )) == 36.8699)
    assert(point_on_straight((2.0, 3.0, 3.0), ((0.0,0.0,0.0), (2.0,2.0,2.0))) is False)
    assert (point_on_straight((3.0, 3.0, 3.0), ((0.0, 0.0, 0.0), (2.0, 2.0, 2.0))) is True)
    assert(point_in_segment((3.0, 3.0, 3.0), ((0.0, 0.0, 0.0), (2.0, 2.0, 2.0))) is False)
    assert(point_in_segment((1.0, 1.0, 2.0), ((0.0, 0.0, 0.0), (2.0, 2.0, 4.0))) is True)