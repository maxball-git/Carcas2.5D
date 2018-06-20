

class Line(tuple):

    def __new__(cls, p1, p2):
        return p1, p2