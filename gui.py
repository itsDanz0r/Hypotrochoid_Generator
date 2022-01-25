"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter
from canvas import MainCanvas


class SidebarFrame(tkinter.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        print(self.parent)
        self.play_button = tkinter.Button(
            text='PLAY',
            command=self.parent.main_canvas.animate
        )

        self.stop_button = tkinter.Button(
            text='STOP',
            command=self.parent.main_canvas.stop_playback
        )

        self.draw_many_button = tkinter.Button(
            text='DRAW MANY',
            command=self.parent.main_canvas.draw_many
        )
        self.tracer_only_checkbox = tkinter.Checkbutton(
            text='Tracer Only',
            variable=self.parent.main_canvas.tracer_only_bool,
            command=self.parent.main_canvas.toggle_tracer_only,
            onvalue=True,
            offvalue=False
        )
        self.frame_skip_label = tkinter.Label(
            text="Skip frames:"
        )

        self.frame_skip_spinbox = tkinter.Spinbox(
            text='Skip Frames:',
            textvariable=self.parent.main_canvas.frame_skip,
            from_=0,
            to=50
        )

        self.controls = [
            self.play_button,
            self.stop_button,
            self.draw_many_button,
            self.tracer_only_checkbox,
            self.frame_skip_label,
            self.frame_skip_spinbox,
        ]

        i = 100
        for control in self.controls:
            control.place(
                x=40, y=i
            )
            i += 30

    def play_button(self) -> None:
        """Define behaviour of play button"""
        if self.parent.main_canvas.playback_stopped:
            self.parent.main_canvas.playback_stopped = False
            self.parent.main_canvas.resume_playback()
        else:
            self.parent.main_canvas.animate()

    def stop_button(self) -> None:
        """Define behaviour of stop button"""
        if self.parent.main_canvas.playback_stopped:
            self.parent.main_canvas.playback_stopped = False
            self.parent.main_canvas.delete('all')
            self.parent.main_canvas.initial_setup()
            self.stop_button.configure(
                text='STOP'
            )
        else:
            self.parent.main_canvas.stop_playback()
            self.parent.main_canvas.playback_frame = 0
            self.stop_button.configure(
                text='RESET'
            )
            self.play_button.configure(
                text='RESUME'
            )


class CanvasFrame(tkinter.Frame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.canvas = MainCanvas(self)
        self.canvas.place(x=200, y=0)


class MainGUI(tkinter.Tk):

    def __init__(self):
        super().__init__()

        # Define app properties
        self.title('Hypotrochoid Generator')
        self.width = 1200
        self.height = 800
        self.geometry(f'{self.width}x{self.height}')
        self.center = (self.width // 2, self.height // 2)
        self.canvas_frame = CanvasFrame(self)
        self.canvas_frame.place(x=0, y=300)
        self.main_canvas = self.canvas_frame.canvas
        self.sidebar_frame = SidebarFrame(self)
        self.sidebar_frame.place(x=0, y=0)
