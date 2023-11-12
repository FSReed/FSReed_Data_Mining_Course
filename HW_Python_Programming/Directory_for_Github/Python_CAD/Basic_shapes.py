from pyautocad import aDouble, APoint
import numpy as np
from numpy.linalg import *


def rectangle_seq(width, height, x=0, y=0):
    return aDouble(
        x, y, 0, x + width, y, 0, x + width, y + height, 0, x, y + height, 0, x, y, 0
    )


def make_rectangle(model, width, height, x=0, y=0, fixlineweight=False):
    """Pass in a block and return a rectangle in the block."""
    rectangle = model.AddPolyLine(rectangle_seq(width, height, x, y))
    if fixlineweight:
        rectangle.Lineweight = fixlineweight
    return rectangle


def beam_bottom_curve(model, x0, y0, x_mid, y_mid, x1, y1, accuracy=100):
    """Pass in a block and return a parabola in the block."""
    A = np.array([[x0**2, x0, 1], [x_mid**2, x_mid, 1], [x1**2, x1, 1]])
    y = np.array([y0, y_mid, y1])
    result = solve(A, y)
    a, b, c = result[0], result[1], result[2]
    f = lambda x: a * (x**2) + b * x + c
    point_set = []
    for i in range(accuracy + 1):
        point_set.extend(
            [x0 + i * (x1 - x0) / accuracy, f(x0 + i * (x1 - x0) / accuracy), 0]
        )
    curve = aDouble(point_set)
    start_node = APoint(x0, y0, 0)
    end_node = APoint(x1, y1, 0)
    spline = model.AddSpLine(curve, start_node, end_node)
    # spline.StartTangent = 2 * result[0] * x0 + result[0]
    # spline.EndTangent = 2 * result[0] * x1 + result[1]
    return spline
