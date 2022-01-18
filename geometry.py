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
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


def polar_to_cartesian_with_offset(r=0, theta=0, x_offset=0, y_offset=0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = (r * math.cos(math.radians(theta))) + x_offset
    y = (r * math.sin(math.radians(theta))) + y_offset
    return x, y
