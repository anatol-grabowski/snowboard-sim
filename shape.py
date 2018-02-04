import numpy as np


class Polygon():
    def __init__(self, points):
        self.original_points = np.array(points, dtype=float)
        print(self.original_points)
        self.rot = 0
        self.loc = np.zeros(2)
        Polygon.update(self)

    def update(self):
        self.points = self.original_points.copy()
        fi = self.rot
        rot_matrix = np.array([[np.cos(fi), -np.sin(fi)],
                               [np.sin(fi), np.cos(fi)]])
        for p in self.points:
            np.dot(rot_matrix, p, p)
        self.points += self.loc

    def contains(self, p):
        sign = np.cross(self.points[-1] - p, self.points[0] - p)
        for i in range(len(self.points) - 1):
            if np.cross(self.points[i] - p, self.points[i+1] - p) * sign < 0:
                return False
        return True



class Body(Polygon):
    def __init__(self, points, m):
        self.m = m
        self.vel = np.zeros(2)
        self.acc = np.zeros(2)
        self.force = np.zeros(2)
        super().__init__(points)

    def update(self, dt):
        self.acc = self.force / self.m
        self.vel += self.acc * dt
        self.loc += self.vel * dt
        super().update()



#s = np.array([[1,2], [-0.1, 0.2], [0, -0.5]])
#sh = Shape(s)
#sh.rot = np.pi/2
#sh.update()
#
#fi = np.pi/2
#rot_matrix = np.array([[np.cos(fi), -np.sin(fi)],
#                       [np.sin(fi), np.cos(fi)]])

