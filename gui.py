"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter
import time
import math


class MainCanvas(tkinter.Canvas):
    def __init__(self, parent):
        super().__init__()

        self.height = 800
        self.width = 800

        self.configure(
            height=self.height,
            width=self.width,
            background='white'
        )

        self.center_x = self.height // 2
        self.center_y = self.width // 2

        self.parent = parent
        self.fps = 120

        self.trace = None

        self.circles = []

        self.pendulum = None
        self.pendulum_end_x = 0
        self.pendulum_end_y = 0
        self.pendulum_theta_mod = 3
        self.pendulum_length_mod = 0.7

        self.playback_stopped = False

        self.draw_initial_setup()

    def draw_initial_setup(self):
        """Draw all components on canvas at default settings"""
        self.circles = [
            Circle(200, 0, self, None),
        ]
        self.circles.append(
            Circle(100, 0, self, self.circles[0])
        )

        for circle in self.circles:
            circle.draw()

    def stop_playback(self):
        """Sets flag so that drawing stops on next trace calculation"""
        self.playback_stopped = True

    def calculate_pendulum_coords(self, r, theta):
        self.pendulum_end_x, self.pendulum_end_y = geometry.polar_to_cartesian_with_offset(
            r=r * self.pendulum_length_mod,
            theta=theta * self.pendulum_theta_mod,
            x_offset=self.inner_circle_x,
            y_offset=self.inner_circle_y
        )
        return self.inner_circle_x, self.inner_circle_y, self.pendulum_end_x, self.pendulum_end_y

    def animate_test(self):
        """Test animation - pendulum rotating 360° inside the inner circle"""
        pendulum_coords_list = []
        # i represents number of rotations to calculate
        for i in range(1, 3601):
            if self.playback_stopped:
                self.playback_stopped = False
                return

            # Division here determines frame rate if program running full speed
            time.sleep(1 / self.fps)

            # Clear current positions
            self.delete(self.pendulum)
            self.delete(self.inner_circle)
            self.delete(self.trace)

            # Calculate and draw inner circle
            self.calculate_inner_circle_coords(self.inner_circle_radius, i)
            self.inner_circle = self.circle(
                x=self.inner_circle_x,
                y=self.inner_circle_y,
                r=self.inner_circle_radius
            )

            # Calculate and draw pendulum
            self.pendulum = self.create_line(
                self.calculate_pendulum_coords(self.inner_circle_radius, i)
            )

            # Add to coords list every 4 calculations
            # Needs to be adjustable, affects performance and quality
            if i % 4 == 0:
                pendulum_coords_list.append((self.pendulum_end_x, self.pendulum_end_y))

            # Lower Z-index of both circles and pendulum so trace is more visible
            self.tag_lower(self.pendulum)
            self.tag_lower(self.inner_circle)
            self.tag_lower(self.outer_circle)

            # Only begin drawing after 8 frames to allow minimum coordinates in list
            if i > 7:
                self.trace = self.create_line(
                    pendulum_coords_list,
                    width=1,
                    smooth=1,
                    fill='red',
                )

            self.update_idletasks()
            self.update()


class Circle:
    radius: float
    theta: float
    theta_mod: float

    def __init__(self, r: float, theta: float, canvas: MainCanvas, parent=None):
        self.center_x = 0.0
        self.center_y = 0.0
        self.radius = r
        self.canvas = canvas
        self.parent = parent
        self.theta = theta
        self.theta_mod = 1
        self.calculate_position()

    def calculate_position(self):
        if self.parent is None:
            self.center_x = self.canvas.center_x
            self.center_y = self.canvas.center_y
        else:
            self.center_x, self.center_y = polar_to_cartesian_with_offset(
                r=self.radius,
                theta=self.theta * self.theta_mod,
                x_offset=self.parent.center_x,
                y_offset=self.parent.center_y
            )

    def draw(self):
        """Draw a circle on the main canvas with specified attributes"""
        x = self.center_x
        y = self.center_y
        r = self.radius
        return self.canvas.create_oval(x + r, y + r, x - r, y - r)


class MainGUI(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Hypotrochoid Generator')

        self.height = 800
        self.width = 800
        self.geometry(f'{self.height}x{self.width}')

        self.center_x = self.height // 2
        self.center_y = self.width // 2

        self.main_canvas = MainCanvas(self)

        self.main_canvas.place(x=0, y=0)

        self.play_button = tkinter.Button(
            text='PLAY',
            command=self.main_canvas.animate_test
        )
        self.play_button.pack()

        self.stop_button = tkinter.Button(
            text='STOP',
            command=self.main_canvas.stop_playback
        )
        self.stop_button.pack()


def cartesian_to_polar(x=0.0, y=0.0) -> tuple[float, float]:
    """Takes cartesian coordinates as input and returns polar coordinates"""
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan(y / x)
    return r, theta


def polar_to_cartesian(r=0.0, theta=0.0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


def polar_to_cartesian_with_offset(r=0.0, theta=0.0, x_offset=0.0, y_offset=0.0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = (r * math.cos(math.radians(theta))) + x_offset
    y = (r * math.sin(math.radians(theta))) + y_offset
    return x, y
