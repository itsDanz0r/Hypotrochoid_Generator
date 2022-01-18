"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter


class MainGUI(tkinter.Tk):
    main_canvas: tkinter.Canvas

    def __init__(self):
        super().__init__()
        self.title('Hypotrochoid Generator')
        self.height = 800
        self.width = 800
        self.geometry(f'{self.height}x{self.width}')

        self.outer_circle = None
        self.inner_circle = None
        self.pendulum = None

        self.main_canvas = tkinter.Canvas(
            height=800,
            width=800,
            background='white'
        )
        self.main_canvas.pack()
        self.draw_initial_setup()

    def circle(self, x=0, y=0, r=0):
        """Draw a circle on the main canvas with specified attributes"""
        return self.main_canvas.create_oval(x + r, y + r, x - r, y - r)

    def draw_initial_setup(self):
        """Draw all components on canvas at default settings"""
        self.outer_circle = self.circle(
            x=self.height // 2,
            y=self.width // 2,
            r=200,
        )

        self.inner_circle = self.circle(
            x=self.height // 2,
            y=self.width // 2,
            r=100,
        )

        # inner_circle_specs = self.main_canvas.coords(self.inner_circle)
        # self.pendulum = self.main_canvas.create_line(self.main_canvas.coords(self.inner_circle))
