"""
Hypotrochoid Generator - geometry.py
Geometry and other math needed to place objects
"""

import math

import gui


class Circle:
    radius: float
    center_x: float
    center_y: float

    def __init__(self, x, y, r, theta, canvas: gui.MainCanvas, parent=None):
        self.center_x = x
        self.center_y = y
        self.radius = r
        self.canvas = canvas
        self.parent = parent
        self.theta = theta

    def calculate_position(self, theta):
        if self.parent is None:
            self.center_x = self.canvas.center_x
            self.center_y = self.canvas.center_y
        else:
            self.center_x, self.center_y =
    -+-*8
    def draw(self):
        """Draw a circle on the main canvas with specified attributes"""
        x = self.center_x
        y = self.center_y
        r = self.radius
        return self.canvas.create_oval(x + r, y + r, x - r, y - r)


def cartesian_to_polar(x=0, y=0) -> tuple[float, float]:
    """Takes cartesian coordinates as input and returns polar coordinates"""
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan(y / x)
    return r, theta


def polar_to_cartesian(r=0, theta=0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


def polar_to_cartesian_with_offset(r=0, theta=0, x_offset=0, y_offset=0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = (r * math.cos(math.radians(theta))) + x_offset
    y = (r * math.sin(math.radians(theta))) + y_offset
    return x, y
