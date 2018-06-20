from functions.line import Line


class Rectangle():

    def __init__(self, w = 1, vertex_array_2d=([0, 0], [5, 5])):

        x1 = vertex_array_2d[0][0]
        y1 = vertex_array_2d[0][1]
        x2 = vertex_array_2d[1][0]
        y2 = vertex_array_2d[1][1]

        self.points = ((x1,y1),(x1,y2),(x2,y2),(x2,y1))
        self.lines = (
            Line(self.points[0], self.points[1]),
            Line(self.points[1], self.points[2]),
            Line(self.points[2], self.points[3]),
            Line(self.points[3], self.points[0])
        )

