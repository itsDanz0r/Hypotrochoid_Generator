"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter
import time


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

        self.outer_circle = None
        self.outer_circle_radius = 200

        self.inner_circle = None
        self.inner_circle_radius = 100
        self.inner_circle_x = self.center_x
        self.inner_circle_y = self.center_y
        self.inner_circle_theta_mod = 2.0

        self.pendulum = None
        self.pendulum_end_x = 0
        self.pendulum_end_y = 0
        self.pendulum_theta_mod = 3
        self.pendulum_length_mod = 0.7

        self.playback_stopped = False

        self.draw_initial_setup()

    def draw_initial_setup(self):
        """Draw all components on canvas at default settings"""
        self.outer_circle = self.circle(
            x=self.center_x,
            y=self.center_y,
            r=200,
        )

        self.inner_circle = self.circle(
            x=self.center_x,
            y=self.center_y,
            r=100,
        )

        self.pendulum = self.create_line(
            self.inner_circle_x,
            self.inner_circle_y,
            self.inner_circle_x + self.inner_circle_radius,
            self.inner_circle_y
        )

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

    def calculate_inner_circle_coords(self, r=0, theta=0):
        self.inner_circle_x, self.inner_circle_y = geometry.polar_to_cartesian_with_offset(
            r=r,
            theta=theta * self.inner_circle_theta_mod,
            x_offset=self.center_x,
            y_offset=self.center_y
        )
        return

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
