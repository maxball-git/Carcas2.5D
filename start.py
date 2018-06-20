from pyglet.gl import *
from pyglet.window import key
from primitives.box import Box
from primitives.abs_object import *
from random import choice
from math import log, sqrt
from numpy import sign
from primitives.scene import Scene
import tkinter


WINDOW = 800
INCREMENT = 5


class Window(pyglet.window.Window):
    # Cube 3D start rotation
    xRotation = yRotation = 0
    speed_rotation = 0.2
    zoom = 30.0
    zoom_speed = 2.0

    modes = ({DW_FACES},
             {DW_EDGES},
             {DW_POINTS},
             {DW_EDGES, DW_FACES},
             {DW_POINTS, DW_FACES},
             {DW_POINTS, DW_EDGES},
             {DW_POINTS, DW_EDGES, DW_FACES},
             )

    def __init__(self, width, height, title=''):
        #self.push_handlers(pyglet.window.event.WindowEventLogger())
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()
        super(Window, self).__init__(width=width, height=height, caption=title)

        glClearColor(0, 0, 0, 1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LINE_SMOOTH)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        self.current_mode = 0
        self.scene = Scene()
        self.scene.append(Box(length=2.7,
                        thickness=.05,
                        height=.1,
                        mode=self.modes[self.current_mode]))



    def on_draw(self):
        # Clear the current GL Window
        self.clear()
        glLoadIdentity()
        # Push Matrix onto stack

        glPushMatrix()
        glTranslatef(0.0, 0.0, -self.zoom)

        glRotatef(self.xRotation, 1, 0, 0)
        glRotatef(self.yRotation, 0, 1, 0)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)

        glLineWidth(1.5)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)

        self.scene.draw()

        glPopMatrix()

    def on_resize(self, width, height):
        # set the Viewport
        print 'The window was resized to %dx%d' % (width, height)
        glViewport(0, 0, width, height)

        # using Projection mode
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspectRatio = width / height
        gluPerspective(35, aspectRatio, 1, 1000)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -400)
        return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.xRotation -= dy * self.speed_rotation
        self.yRotation += dx * self.speed_rotation

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):

        if scroll_y == 0:
            return
        v = float(scroll_y * self.zoom_speed*(float(1/self.zoom)))
        self.zoom = self.zoom + v
        if self.zoom < 1.0:
            self.zoom = 1.0

    def on_mouse_press(self, x, y, button, modifiers):

        if button == pyglet.window.mouse.RIGHT:
            if (self.current_mode+1) < len(self.modes):
                self.current_mode +=1
            else:
                self.current_mode=0
            self.scene.mode = self.modes[self.current_mode]

    def on_mouse_release(self, x, y, button, modifiers):
        pass


if __name__ == '__main__':

    Window(WINDOW, WINDOW, 'Pyglet')
    pyglet.app.run()