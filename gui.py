"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter
import time
import geometry


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

        self.center = (self.height // 2, self.width // 2)

        self.parent = parent
        self.fps = 60

        self.tracer = None

        self.circles = []
        self.inner_circle = None
        self.arm = None

        self.playback_stopped = True
        self.playback_frame = 1

        self.hide_drawing = tkinter.BooleanVar()
        self.hide_drawing.set(False)

        self.draw_initial_setup()

    def draw_initial_setup(self) -> None:
        """Draw all components on canvas at default settings"""
        self.circles = [
            geometry.Circle(300, 0, self, None),
        ]

        self.circles.append(
            geometry.Circle(180, 0, self, self.circles[0])
        )

        self.circles.append(
            geometry.Circle(120, 0, self, self.circles[1])
        )

        for circle in self.circles:
            circle.draw()

        self.inner_circle = self.circles[-1]

        self.arm = geometry.Arm(self.circles[-1], self)
        self.arm.draw()

        self.tracer = geometry.Tracer(self)

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

    def apply_mods(self):
        self.arm.length_mod = 1.1
        self.circles[1].radius = 194.7
        self.circles[1].theta_mod = -1
        self.circles[2].radius = 30

    def calculate_positions(self, i) -> None:
        """Calculates all canvas drawing object positions"""
        for circle in self.circles:
            if circle.parent is not None:
                circle.theta = circle.parent.radius / circle.radius * i
            circle.calculate_position()
        self.arm.theta = -self.arm.parent.theta * (self.arm.parent.parent.radius / self.arm.parent.radius)
        self.arm.calculate_position()
        self.tracer.coords.append(self.arm.end_coords)

    def animate_test(self) -> None:
        """Test animation - pendulum rotating 360° inside the inner circle"""
        self.tracer.coords = []
        self.playback_stopped = False
        self.apply_mods()

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
            self.calculate_positions(i)
            for circle in self.circles:
                circle.draw()
            self.arm.draw()

            # Add to coords list every 4 calculations
            # Needs to be adjustable, affects performance and quality
            self.tracer.coords.append(self.arm.end_coords)

            # Lower Z-index of all circles and pendulum so trace is more visible
            self.tag_lower(self.arm)
            for circle in self.circles:
                self.tag_lower(circle)

            # Only begin drawing after 2 frames to allow minimum coordinates in list
            if i > 1:
                self.tracer.draw()

            self.update_idletasks()
            self.update()

    def draw_many(self) -> None:
        """Calculates and draws a specified number of frames in one step"""
        self.playback_stopped = True
        self.tracer.coords = []
        self.delete('all')
        self.apply_mods()

        for i in range(0, 40000):
            self.calculate_positions(i / 10)

        self.tracer.draw()
        self.update_idletasks()
        self.update()


class MainGUI(tkinter.Tk):

    def __init__(self):
        super().__init__()

        # Define app properties
        self.title('Hypotrochoid Generator')
        self.height = 1200
        self.width = 1200
        self.geometry(f'{self.height}x{self.width}')
        self.center = (self.height // 2, self.width // 2)

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
        # self.hide_circles = tkinter.Checkbutton(
        #     text='Hide Circles',
        #     variable=self.main_canvas.hide_drawing,
        #     onvalue=True,
        #     offvalue=False,
        # )
        # self.hide_circles.pack()

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
