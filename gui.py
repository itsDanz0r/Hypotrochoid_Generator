"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter
import time
import geometry


class MainGUI(tkinter.Tk):
    main_canvas: tkinter.Canvas

    def __init__(self):
        super().__init__()
        self.title('Hypotrochoid Generator')

        self.height = 800
        self.width = 800
        self.geometry(f'{self.height}x{self.width}')

        self.center_x = self.height // 2
        self.center_y = self.width // 2

        self.fps = 60

        self.trace = None

        self.outer_circle = None
        self.outer_circle_radius = 200

        self.inner_circle = None
        self.inner_circle_radius = 100
        self.inner_circle_x = self.center_x
        self.inner_circle_y = self.center_y
        self.inner_circle_theta_mod = 1.0

        self.pendulum = None
        self.pendulum_end_x = 0
        self.pendulum_end_y = 0
        self.pendulum_theta_mod = 43

        self.playback_stopped = False

        self.main_canvas = tkinter.Canvas(
            height=800,
            width=800,
            background='white'
        )
        self.main_canvas.place(x=0, y=0)

        self.play_button = tkinter.Button(
            text='PLAY',
            command=self.animate_test
        )
        self.play_button.pack()

        self.stop_button = tkinter.Button(
            text='STOP',
            command=self.stop_playback
        )
        self.stop_button.pack()

        self.draw_initial_setup()

    def circle(self, x=0.0, y=0.0, r=0.0):
        """Draw a circle on the main canvas with specified attributes"""
        return self.main_canvas.create_oval(x + r, y + r, x - r, y - r)

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

        self.pendulum = self.main_canvas.create_line(
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
            r=r,
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

            self.main_canvas.delete(self.pendulum)
            self.main_canvas.delete(self.inner_circle)
            self.main_canvas.delete(self.trace)

            self.calculate_inner_circle_coords(self.inner_circle_radius, i)
            self.inner_circle = self.circle(
                x=self.inner_circle_x,
                y=self.inner_circle_y,
                r=self.inner_circle_radius
            )

            # Every 4 calculations add new coordinates to list
            # This will need a setting so it can be turned up or down, affects performance

            # Draw pendulum
            self.pendulum = self.main_canvas.create_line(
                self.calculate_pendulum_coords(self.inner_circle_radius, i)
            )

            # Add to coords list every 4 frames
            # Needs to be adjustable, affects performance and quality
            if i % 4 == 0:
                pendulum_coords_list.append((self.pendulum_end_x, self.pendulum_end_y))

            # Lower Z-index of both circles and pendulum so trace is more visible
            self.main_canvas.tag_lower(self.pendulum)
            self.main_canvas.tag_lower(self.inner_circle)
            self.main_canvas.tag_lower(self.outer_circle)

            # Only begin drawing after 8 frames to allow minimum coordinates in list
            if i > 7:
                self.trace = self.main_canvas.create_line(
                    pendulum_coords_list,
                    width=1,
                    smooth=1,
                    fill='red',
                )

            self.update_idletasks()
            self.update()

