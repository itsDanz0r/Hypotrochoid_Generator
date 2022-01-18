import tkinter


class MainGUI(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Hypotrochoid Generator')
        self.geometry('800x600')
        self.build_app()

    def build_app(self):
        self.main_canvas = tkinter.Canvas(
            height=800,
            width=600
        )
        self.main_canvas.pack()



