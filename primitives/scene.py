from __builtin__ import setattr

from abs_object import *

class Scene(list):

    def draw(self):
        for item in self:
            item.draw()

    def set_for_all_items(self, prop_name, prop_value):
        for item in self:
            if hasattr(item, prop_name):
                setattr(item, prop_name, prop_value)
                if hasattr(item, 'init_vertex_lists'):
                    item.init_vertex_lists()

    def __setattr__(self, key, value):
        if not hasattr(self, key):
            self.set_for_all_items(key, value)
