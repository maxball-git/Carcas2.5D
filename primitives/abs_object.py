from pyglet.gl import *
from enum import Enum

dN = 0
dE = 90
dS = 180
dW = 270

dNE = 45
dSE = 135
dSW = 225
dNW = 315

dNNE = 22.5
dSSE = 157.5
dSSW = 202.5
dNNW = 337.5

dNEE = 67.5
dSEE = 112.5
dSWW = 247.5
dNWW = 192.5

directions = {dN, dNNE, dNE, dNEE,
              dE, dSEE, dSE, dSSE,
              dS, dSSW, dSW, dSWW,
              dW, dNWW, dNW, dNNW}


class WrongNumberOfArguments(ValueError):
    pass


class Point3D(tuple):

    def __new__(cls, *args):
        if len(args) == 3:
            return tuple(args)
        else:
            raise NeedExactlyTree()

    def __add__(self, other):
        return list(map(lambda a, b: a + b, self, other))


class Color3D(tuple):

    def __new__(cls, *args):
        if (len(args) == 3) or (len(args) == 4):
            return tuple(args)
        else:
            raise WrongNumberOfArguments()

    def __add__(self, other):
        return list(map(lambda a, b: a + b, self, other))


class Position:

    def __init__(self, origin, direction, pivot):
        self.position = origin
        self.direction = direction
        self.pivot = pivot


defPositionV = Position(Point3D(0, 0, 0), dN, Point3D(0, 0, 0))
defPositionH = Position(Point3D(0, 0, 0), dE, Point3D(0, 0, 0))

DW_POINTS = "POINTS"
DW_EDGES = "EDGES"
DW_FACES = "FACES"
DW_X_RAY = "X_RAY"

draw_modes = {DW_POINTS, DW_EDGES, DW_FACES, DW_X_RAY}


class Object3d(object):

    def __init__(self, *args, **kwargs):
        super(Object3d, self).__init__()
        self.position = kwargs.get("position", defPositionH)
        self.sizeX = kwargs.get("X", kwargs.get("x", kwargs.get("length", 1)))
        self.sizeY = kwargs.get("Y", kwargs.get("y", kwargs.get("height", 1)))
        self.sizeZ = kwargs.get("Z", kwargs.get("z", kwargs.get("thickness", 1)))
        self.points = []
        self.colors = []
        self.indexes = []

        self.init_points()
        self.init_colors()
        self.init_indexes()

        self.point_color = Color3D(255, 255, 255, 128)
        self.edges_color = Color3D(255, 255, 255, 128)

        self.mode = kwargs.get("mode", kwargs.get("m", {DW_POINTS, DW_EDGES, DW_FACES}))
        self.vertex_lists = {name: None for name in draw_modes}
        self.batch = pyglet.graphics.Batch()
        self.init_vertex_lists()
        self.visible = True

    def get_draw_xyz(self):
        return self.position.position + self.position.pivot

    def init_points(self):
        pass

    def init_colors(self):
        pass

    def init_indexes(self):
        pass

    def draw(self):
        if self.visible:
            glEnable(GL_POINT_SMOOTH)
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_POLYGON_SMOOTH)
            self.batch.draw()

    def init_vertex_lists(self):

        if not self.indexes:
            self.indexes = range(0, self.points.__len__()-1)

        del self.batch
        self.batch = pyglet.graphics.Batch()

        indexes_array = self.vertex_array(int, self.indexes)
        points_len = self.points.__len__()
        vertex_array = self.vertex_array(float, self.points)
        vertex_format = 'v3f/dynamic'
        color_format = 'c'+str(len(self.colors[0]))+'B/dynamic'

        if DW_FACES in self.mode:
            if self.indexes.__len__() > 2:

                if bool(4 & 3):
                    t = GL_TRIANGLES
                if bool(4 & 4):
                    t = GL_QUADS
                else:
                    t = GL_POLYGON

                self.vertex_lists[DW_FACES] = self.batch.add_indexed(
                    points_len,
                    t,
                    None,
                    indexes_array,
                    (vertex_format, vertex_array),
                    (color_format, self.vertex_array(int, self.colors))
                )

        if DW_EDGES in self.mode:
            self.vertex_lists[DW_EDGES] = self.batch.add_indexed(
                points_len,
                GL_LINE_STRIP,
                None,
                self.vertex_array(int, map(lambda x: x+(x[0],), self.indexes)),
                (vertex_format, vertex_array),
                (color_format, self.edges_color * points_len)
            )
        if DW_POINTS in self.mode:
            gl.glPointSize(5)
            self.vertex_lists[DW_POINTS] = self.batch.add_indexed(
                points_len,
                GL_POINTS,
                None,
                indexes_array,
                (vertex_format, vertex_array),
                (color_format, self.point_color * points_len)
            )

    @staticmethod
    def vertex_array(t, lst):
        a = []
        for v in lst:
            a.extend(v)
        return [t(i) for i in a]

