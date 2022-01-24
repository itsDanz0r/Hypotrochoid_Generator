from abc import ABC, abstractmethod
import math


class CanvasDrawing(ABC):

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class Circle(CanvasDrawing):
    """Defines linked list of circles on canvas"""

    def __init__(self, r: float = 10, theta: float = 0, canvas=None, parent=None, colour='black'):
        self.center = (0.0, 0.0)
        self.radius = r
        self.canvas = canvas
        self.parent = parent
        self.theta = theta
        self.theta_mod = 1
        self.calculate_position()
        self.canvas_repr = None
        self.colour = colour

    def calculate_position(self) -> None:
        """Calculate current position based on current properties"""
        if self.parent is None:
            self.center = self.canvas.center

        else:
            self.center = polar_to_cartesian_with_offset(
                r=self.parent.radius - self.radius,
                theta=self.theta * self.theta_mod,
                x_offset=self.parent.center[0],
                y_offset=self.parent.center[1]
            )

    def draw(self) -> None:
        """Draw a circle on the main canvas with specified dimensions and location"""
        x, y = self.center
        r = self.radius
        self.canvas_repr = self.canvas.create_oval(x + r, y + r, x - r, y - r, outline=self.colour)

    def delete(self) -> None:
        self.canvas.delete(self.canvas_repr)


class Arm(ABC):

    def __init__(self, parent: Circle, canvas):
        self.canvas = canvas
        self.parent = parent
        self.start_coords = self.parent.center
        self.end_coords = (0, 0)
        self.length_mod = 1
        self.theta = 1
        self.theta_mod = 1
        self.canvas_repr = None

    def calculate_position(self) -> None:
        """Calculate arm start and end position"""
        self.start_coords = self.parent.center
        self.end_coords = polar_to_cartesian_with_offset(
            r=self.parent.radius * self.length_mod,
            theta=self.theta * self.theta_mod,
            x_offset=self.parent.center[0],
            y_offset=self.parent.center[1]
        )

    def draw(self) -> None:
        self.canvas_repr = self.canvas.create_line(
            self.start_coords,
            self.end_coords
        )

    def delete(self) -> None:
        self.canvas.delete(self.canvas_repr)


class Tracer(CanvasDrawing):
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas_repr = None
        self.coords = []
        self.colour = 'red'

    def draw(self):
        self.canvas_repr = self.canvas.create_line(
                    self.coords,
                    width=1,
                    smooth=True,
                    fill=self.colour,
                )

    def delete(self):
        self.canvas.delete(self.canvas_repr)


# def cartesian_to_polar(x=0.0, y=0.0) -> tuple[float, float]:
#     """Takes cartesian coordinates as input and returns polar coordinates"""
#     r = math.sqrt(x ** 2 + y ** 2)
#     theta = math.atan(y / x)
#     return r, theta
#
#
# def polar_to_cartesian(r=0.0, theta=0.0) -> tuple[float, float]:
#     """Takes polar coordinates as input and returns cartesian coordinates"""
#     x = r * math.cos(math.radians(theta))
#     y = r * math.sin(math.radians(theta))
#     return x, y


def polar_to_cartesian_with_offset(r=0.0, theta=0.0, x_offset=0.0, y_offset=0.0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = (r * math.cos(math.radians(theta))) + x_offset
    y = (r * math.sin(math.radians(theta))) + y_offset
    return x, y
