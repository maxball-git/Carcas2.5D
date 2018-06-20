#coding=utf-8

from pyglet.gl import *
from abs_object import *

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''
from OpenGL.arrays import vbo
import numpy as np


class Box(Object3d):

    def __init__(self, orig_direct=defPositionV, length=1, height=1, thickness=1, *args, **kwargs):
        super(Box,self).__init__(position=orig_direct,
                                 length=length,
                                 height=height,
                                 thickness=thickness,
                                 *args, **kwargs)

    def init_points(self):
        l = self.sizeX / 2.0
        h = self.sizeY / 2.0
        t = self.sizeZ / 2.0
        self.points.extend([
            Point3D(l, h, t),
            Point3D(l, -h, t),
            Point3D(l, -h, -t),
            Point3D(l, h, -t),
            Point3D(-l, h, t),
            Point3D(-l, -h, t),
            Point3D(-l, -h, -t),
            Point3D(-l, h, -t),
        ])

    def init_colors(self):
        self.colors.append(Color3D(255, 255, 255, 128))
        self.colors.append(Color3D(0, 255, 255, 128))
        self.colors.append(Color3D(0, 0, 255, 128))
        self.colors.append(Color3D(255, 0, 255, 128))
        self.colors.append(Color3D(255, 0, 0, 128))
        self.colors.append(Color3D(0, 0, 0, 128))
        self.colors.append(Color3D(0, 255, 0, 128))
        self.colors.append(Color3D(255, 255, 0, 128))

    def init_indexes(self):
        self.indexes.extend([
            (0, 1, 2, 3),  # front face
            (0, 4, 7, 3),  # right face
            (0, 1, 5, 4),  # top face
            (1, 5, 6, 2),  # left face
            (2, 3, 7, 6),  # bottom face
            (6, 5, 4, 7),  # back face
        ])
