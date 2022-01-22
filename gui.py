"""
Hypotrochoid Generator - gui.py
GUI setup and drawing functions
"""

import tkinter
import time
import geometry
from PIL import Image, ImageDraw
import math
import fractions


class SidebarFrame(tkinter.Frame):
    def __init__(self):
        super().__init__()


class CanvasFrame(tkinter.Frame):
    def __init__(self):
        super().__init__()


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

        self.rotation_mod = 250

        self.hide_drawing = tkinter.BooleanVar()
        self.hide_drawing.set(False)

        self.img_output_res_mod = 10

        self.draw_pixels = False
        self.inner_colour = [255, 255, 255]
        self.outer_colour = [0, 0, 255]

        self.initial_setup()
        self.calc_start = time.time()

    def initial_setup(self) -> None:
        """Draw all components on canvas at default settings"""
        self.circles = [
            geometry.Circle(300, 0, self, None),
        ]

        self.circles.append(
            geometry.Circle(175, 0, self, self.circles[0])
        )

        self.circles.append(
            geometry.Circle(150, 0, self, self.circles[1])
        )

        self.inner_circle = self.circles[-1]
        for i in range(len(self.circles)):
            if i % 2 != 0:
                self.circles[i].theta_mod = -1

        self.arm = geometry.Arm(self.circles[-1], self)
        self.apply_mods()
        self.arm.calculate_position()

        for circle in self.circles:
            circle.draw()

        self.arm.draw()

        self.tracer = geometry.Tracer(self)

    def reset_playback(self) -> None:
        """Reset paused playback and redraw initial setup"""
        self.delete('all')
        self.initial_setup()
        self.playback_frame = 1

    def resume_playback(self) -> None:
        """Resume paused playback"""
        self.animate()

    def stop_playback(self) -> None:
        """Sets flag so that drawing stops on next trace calculation"""
        self.playback_stopped = True

    def apply_mods(self):
        self.arm.theta_mod = -1
        self.arm.length_mod = 1
        self.circles[1].theta_mod = -1

    def calculate_positions(self, i) -> None:
        """Calculates all canvas drawing object positions"""
        for circle in self.circles:
            if circle.parent is not None:
                circle.theta = circle.parent.radius / circle.radius * i
            circle.calculate_position()
        self.arm.theta = -self.arm.parent.theta * (self.arm.parent.parent.radius / self.arm.parent.radius)
        self.arm.calculate_position()
        self.tracer.coords.append((round(self.arm.end_coords[0], 4), round(self.arm.end_coords[1], 4)))

    def animate(self) -> None:
        """Test animation - pendulum rotating 360° inside the inner circle"""
        self.tracer.coords = []
        self.playback_stopped = False
        self.apply_mods()

        # i represents number of rotations to calculate
        while not self.playback_stopped:
            self.playback_frame += 1

            # Division here determines frame rate if program running full speed
            time.sleep(1 / self.fps)

            # Clear current positions
            self.delete("all")

            # Draw circles
            self.calculate_positions(self.playback_frame)
            for circle in self.circles:
                circle.draw()
            self.arm.draw()

            # Lower Z-index of all circles and pendulum so trace is more visible
            self.tag_lower(self.arm)
            for circle in self.circles:
                self.tag_lower(circle)

            # Only begin drawing after 2 frames to allow minimum coordinates in list
            if self.playback_frame > 2:
                self.tracer.draw()

            self.update()

    def draw_many(self) -> None:
        """Calculates and draws a specified number of frames in one step"""
        self.playback_stopped = True
        self.tracer.coords = []
        self.delete('all')
        self.apply_mods()
        self.calc_start = time.time()
        print(f'Calculating {self.rotation_mod} rotations...')
        iterations = 36000 * self.rotation_mod
        for j in range(0, iterations):
            self.calculate_positions(j / 100)
        print(f'Completed in {time.time() - self.calc_start} seconds')
        self.create_img('test' + str(time.time()) + '.png')
        print('')
        self.tracer.coords = self.tracer.coords[0:100000]
        self.tracer.draw()


        # CREATE MANY IMAGES
        # for i in range(1, 999):
        #     self.rotation_mod = 10
        #     self.circles[1].radius = 150 + (i / 10)
        #     self.arm.theta_mod = 1 + (i / 100)
        #     iterations = 36000 * self.rotation_mod
        #     for j in range(0, iterations):
        #         self.calculate_positions(j / 100)
        #     print(f'Completed in {time.time() - self.calc_start} seconds')
        #     self.create_img(f'{str(i).zfill(3)}.png')
        #     self.tracer.coords = []


    def calculate_img_canvas_size(self) -> tuple[float, float]:
        size = round(((self.circles[0].radius * 2) + (
                    self.arm.length_mod * self.circles[-1].radius)) * self.img_output_res_mod)
        return size + 10, size + 10

    def modify_coords_for_output(self) -> list:
        rounded_coords = []
        img_size = self.calculate_img_canvas_size()[0] // 2
        for i in self.tracer.coords:
            rounded_coords.append(
                (
                    round(((i[0] - self.center[0]) * self.img_output_res_mod) + img_size),
                    round(((i[1] - self.center[1]) * self.img_output_res_mod) + img_size)
                )
            )
        return rounded_coords

    def compute_glow(self, rounded_coords, mod: tuple) -> tuple[tuple, ...]:
        new_coords = list(map(list, rounded_coords))
        for i in new_coords:
            i[0] += mod[0]
            i[1] += mod[1]
        return tuple(map(tuple, new_coords))

    def create_img(self, file_name):

        self.calc_start = time.time()
        print('Generating image...')
        rounded_coords = self.modify_coords_for_output()
        img = Image.new('RGB', self.calculate_img_canvas_size(), 'blue')
        print(self.calculate_img_canvas_size())
        draw = ImageDraw.Draw(img)

        # DRAW OUTLINE

        mod_list = (
            (0, 1),
            (1, 0),
            (1, 1),
            (-1, 0),
            (0, -1),
            (-1, -1),
            (1, -1),
            (-1, 1)
        )
        glow_coords_list = []
        for i in mod_list:
            glow_coords_list.append(self.compute_glow(rounded_coords, i))
        for i in glow_coords_list:
            draw.line(i, fill=(255, 255, 255), width=2)
        self.draw_pixels = True
        if self.draw_pixels:
            for i in rounded_coords:
                img.putpixel((i[0], i[1]), self.calculate_pixel_gradient(i))
        else:
            draw.line(rounded_coords, fill=(255, 255, 255), width=1)

        print(f'Completed in {time.time() - self.calc_start} seconds')
        print('Saving image...')
        img_path = r"C:\users\DK\desktop\test"
        img.save(img_path + '/' + file_name)
        print('Done!')

    def calculate_pixel_gradient(self, pixel_coords):
        img_size = self.calculate_img_canvas_size()

        # Find the distance to the center
        distance_to_centre = math.sqrt((pixel_coords[0] - img_size[0] / 2) ** 2 + (pixel_coords[1] - img_size[1] / 2) ** 2)

        # Make it on a scale from 0 to 1
        distance_to_centre = float(distance_to_centre) / (math.sqrt(2) * pixel_coords[0] / 2)

        # Calculate r, g, and b values
        r = round(self.outer_colour[0] * distance_to_centre + self.inner_colour[0] * (1 - distance_to_centre))
        g = round(self.outer_colour[1] * distance_to_centre + self.inner_colour[1] * (1 - distance_to_centre))
        b = round(self.outer_colour[2] * distance_to_centre + self.inner_colour[2] * (1 - distance_to_centre))
        return r, g, b


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
            self.main_canvas.animate()

    def stop_button(self) -> None:
        """Define behaviour of stop button"""
        if self.main_canvas.playback_stopped:
            self.main_canvas.playback_stopped = False
            self.main_canvas.delete('all')
            self.main_canvas.initial_setup()
            self.stop_button.configure(
                text='STOP'
            )
        else:
            self.main_canvas.stop_playback()
            self.main_canvas.playback_frame = 0
            self.stop_button.configure(
                text='RESET'
            )
            self.play_button.configure(
                text='RESUME'
            )
