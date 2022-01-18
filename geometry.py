"""
Hypotrochoid Generator - geometry.py
Geometry and other math needed to place objects
"""

import math


def cartesian_to_polar(x=0, y=0) -> tuple[float, float]:
    """Takes cartesian coordinates as input and returns polar coordinates"""
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan(y / x)
    return r, theta


def polar_to_cartesian(r=0, theta=0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y
