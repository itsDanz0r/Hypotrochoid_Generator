"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter
import time
import math
import typing


class MainCanvas(tkinter.Canvas):
    """Defines custom canvas and animation class"""
    def __init__(self, parent):
        super().__init__()

        self.height = 1200
        self.width = 1200

        self.configure(
            height=self.height,
            width=self.width,
            background='white'
        )

        self.center_x = self.height // 2
        self.center_y = self.width // 2

        self.parent = parent
        self.fps = 240

        self.trace = None
        self.trace_coords = []

        self.circles = []
        self.inner_circle = None

        self.pendulum = None
        self.pendulum_end_x = 0
        self.pendulum_end_y = 0
        self.pendulum_theta_mod = 5 / 3
        self.pendulum_length_mod = 5 / 3

        self.playback_stopped = True
        self.playback_frame = 1

        self.draw_initial_setup()

    def draw_initial_setup(self) -> None:
        """Draw all components on canvas at default settings"""
        self.circles = [
            Circle(300, 0, self, None),
        ]

        self.circles.append(
            Circle(180, 0, self, self.circles[0])
        )

        self.circles.append(
            Circle(30, 0, self, self.circles[1])
        )

        for circle in self.circles:
            circle.draw()

        self.inner_circle = self.circles[-1]
        self.pendulum = self.create_line(
            self.calculate_pendulum_coords(self.inner_circle.radius, 0)
        )

    def calculate_pendulum_coords(self, r, theta) -> tuple[float, float, float, float]:
        """Calculate pendulum start and end position"""
        self.pendulum_end_x, self.pendulum_end_y = polar_to_cartesian_with_offset(
            r=r * self.pendulum_length_mod,
            theta=theta * self.pendulum_theta_mod,
            x_offset=self.inner_circle.center_x,
            y_offset=self.inner_circle.center_y
        )
        return self.inner_circle.center_x, self.inner_circle.center_y, self.pendulum_end_x, self.pendulum_end_y

    def reset_playback(self) -> None:
        """Reset paused playback and redraw initial setup"""
        self.delete('all')
        self.draw_initial_setup()
        self.playback_frame = 1

    def resume_playback(self) -> None:
        """Resume paused playback"""
        self.animate_test()

    def stop_playback(self) -> None:
        """Sets flag so that drawing stops on next trace calculation"""
        self.playback_stopped = True

    def animate_test(self) -> None:
        """Test animation - pendulum rotating 360° inside the inner circle"""
        # TEMPORARY - Mess with theta mods for chaos testing
        self.trace_coords = []
        self.playback_stopped = False

        # i represents number of rotations to calculate
        for i in range(self.playback_frame, 36001):
            if self.playback_stopped:
                self.playback_frame = i
                self.parent.stop_button.configure(
                    text='RESET'
                )
                self.parent.play_button.configure(
                    text='RESUME'
                )
                return

            # Division here determines frame rate if program running full speed
            time.sleep(1 / self.fps)

            # Clear current positions
            self.delete("all")

            # Draw circles
            for circle in self.circles:
                circle.theta = i
                circle.calculate_position()
                circle.draw()

            # Draw pendulum
            self.pendulum = self.create_line(
                self.calculate_pendulum_coords(self.inner_circle.radius, -i)
            )

            # Add to coords list every 4 calculations
            # Needs to be adjustable, affects performance and quality
            self.trace_coords.append((self.pendulum_end_x, self.pendulum_end_y))

            # Lower Z-index of all circles and pendulum so trace is more visible
            self.tag_lower(self.pendulum)
            for circle in self.circles:
                self.tag_lower(circle)

            # Only begin drawing after 8 frames to allow minimum coordinates in list
            if i > 7:
                self.trace = self.create_line(
                    self.trace_coords,
                    width=1,
                    smooth=1,
                    fill='red',
                )

            self.update_idletasks()
            self.update()

    def draw_many(self) -> None:
        """Calculates and draws a specified number of frames in one step"""
        self.trace_coords = []
        self.circles[1].theta_mod = 2.11
        self.circles[2].theta_mod = 2.71
        self.pendulum_theta_mod = -0.9
        self.pendulum_length_mod = 2
        self.delete('all')

        for i in range(0, 36000):
            for circle in self.circles:
                circle.theta = i
                circle.calculate_position()
            self.calculate_pendulum_coords(self.inner_circle.radius, i)
            self.trace_coords.append((self.pendulum_end_x, self.pendulum_end_y))

        self.trace = self.create_line(
            self.trace_coords,
            width=1,
            smooth=1,
            fill='red',
        )
        self.update_idletasks()
        self.update()


class Circle:
    """Defines linked list of circles on canvas"""

    def __init__(self, r: float = 10, theta: float = 0, canvas: MainCanvas = None, parent=None):
        self.center_x = 0.0
        self.center_y = 0.0
        self.radius = r
        self.canvas = canvas
        self.parent = parent
        self.theta = theta
        self.theta_mod = 1
        self.calculate_position()

    def calculate_position(self) -> None:
        """Calculate current position based on current properties"""
        if self.parent is None:
            self.center_x = self.canvas.center_x
            self.center_y = self.canvas.center_y

        else:
            self.center_x, self.center_y = polar_to_cartesian_with_offset(
                r=self.parent.radius - self.radius,
                theta=self.theta * self.theta_mod,
                x_offset=self.parent.center_x,
                y_offset=self.parent.center_y
            )

    def draw(self) -> classmethod:
        """Draw a circle on the main canvas with specified dimensions and location"""
        x = self.center_x
        y = self.center_y
        r = self.radius
        return self.canvas.create_oval(x + r, y + r, x - r, y - r)


class MainGUI(tkinter.Tk):

    def __init__(self):
        super().__init__()

        # Define app properties
        self.title('Hypotrochoid Generator')
        self.height = 1200
        self.width = 1200
        self.geometry(f'{self.height}x{self.width}')
        self.center_x = self.height // 2
        self.center_y = self.width // 2

        # Define and pack widgets
        self.main_canvas = MainCanvas(self)
        self.main_canvas.place(x=0, y=0)

        self.play_button = tkinter.Button(
            text='PLAY',
            command=self.play_button
        )
        self.play_button.pack()

        self.stop_button = tkinter.Button(
            text='STOP',
            command=self.main_canvas.stop_playback
        )
        self.stop_button.pack()

        self.draw_many_button = tkinter.Button(
            text='DRAW MANY',
            command=self.main_canvas.draw_many
        )
        self.draw_many_button.pack()

    def play_button(self) -> None:
        """Define behaviour of play button"""
        if self.main_canvas.playback_stopped:
            self.main_canvas.playback_stopped = False
            self.main_canvas.resume_playback()

        else:
            self.main_canvas.animate_test()

    def stop_button(self) -> None:
        """Define behaviour of stop button"""
        if self.main_canvas.playback_stopped:
            self.main_canvas.playback_stopped = False
            self.main_canvas.delete('all')
            self.main_canvas.draw_initial_setup()
            self.stop_button.configure(
                text='STOP'
            )

        else:
            self.main_canvas.stop_playback()
            self.stop_button.configure(
                text='RESET'
            )
            self.play_button.configure(
                text='RESUME'
            )


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
