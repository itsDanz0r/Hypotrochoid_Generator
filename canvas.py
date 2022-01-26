import tkinter
import geometry
import time
import math
from PIL import Image, ImageDraw

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
YELLOW = [255, 255, 0]
CYAN = [0, 255, 255]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
PURPLE = [255, 0, 255]


class MainCanvas(tkinter.Canvas):
    """Defines custom canvas and animation class"""

    def __init__(self, parent):
        super().__init__()

        self.height = 2160
        self.width = 3840

        self.configure(
            height=self.height,
            width=self.width,
            background='white'
        )

        self.center = (self.width // 2, self.height // 2)

        self.parent = parent
        self.fps = 60
        self.frame_skip = tkinter.StringVar()
        self.frame_skip.set(0)

        self.tracer = None
        self.tracer_only_bool = tkinter.BooleanVar()
        self.tracer_only_bool.set(False)

        self.add_text_overlay = True

        self.draw_glow = True
        self.pixel_resolution = 20

        self.background_colour = (0, 0, 0)
        self.rounded_coords = []

        self.circles = []
        self.inner_circle = None
        self.arm = None

        self.playback_stopped = True
        self.playback_frame = 0

        self.rotation_mod = 30
        self.total_rotations = tkinter.IntVar()
        self.total_rotations.set(0)
        self.img_output_res_mod = 5

        self.draw_pixels = True
        self.inner_colour = [0, 0, 0]
        self.outer_colour = [240, 240, 240]

        self.glow_colour = [255, 255, 255]

        self.initial_setup()
        self.calc_start = time.time()

    def initial_setup(self) -> None:
        """Draw all components on canvas at default settings"""
        self.circles = [
            geometry.Circle(820, 0, self, None, 'gray'),
        ]

        self.circles.append(
            geometry.Circle(600, 0, self, self.circles[0], 'gray')
        )

        self.circles.append(
            geometry.Circle(240, 0, self, self.circles[1], 'gray')
        )

        self.inner_circle = self.circles[-1]
        for i in range(len(self.circles)):
            if i % 2 != 0:
                self.circles[i].theta_mod = self.circles[i].theta_mod * -1

        self.circles[1].theta_mod = self.circles[1].theta_mod * 2.3
        self.circles[2].theta_mod = self.circles[2].theta_mod * 1.6
        self.arm = geometry.Arm(self.circles[-1], self)
        # self.apply_mods()
        self.arm.theta_mod = -1
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
        # self.arm.theta_mod = 1
        self.arm.length_mod = 0.6

    def toggle_tracer_only(self):
        if self.tracer_only_bool.get():
            self.delete(self.arm.canvas_repr)
            for circle in self.circles:
                self.delete(circle.canvas_repr)
            self.update()
        else:
            for circle in self.circles:
                circle.calculate_position()
                circle.draw()
            self.arm.calculate_position()
            self.arm.draw()
            self.update()

    def calculate_positions(self, i) -> None:
        """Calculates all canvas drawing object positions"""
        for circle in self.circles:
            if circle.parent is not None:
                circle.theta = circle.parent.radius / circle.radius * i
            circle.calculate_position()
        self.arm.theta = -self.arm.parent.theta * (self.arm.parent.parent.radius / self.arm.parent.radius)
        self.arm.calculate_position()
        self.tracer.coords.append((round(self.arm.end_coords[0], 4), round(self.arm.end_coords[1], 4)))

    def input_sanity_check(self):
        try:
            int(self.frame_skip.get())
        except ValueError:
            self.frame_skip.set(0)

    def animate(self) -> None:
        """Test animation - pendulum rotating 360° inside the inner circle"""

        self.tracer.coords = []
        self.playback_stopped = False
        # self.apply_mods()

        # i represents number of rotations to calculate
        while not self.playback_stopped:
            self.input_sanity_check()
            self.playback_frame += 1

            # Division here determines frame rate if program running full speed

            # Clear current positions
            self.delete("all")

            # Draw circles
            self.calculate_positions(self.playback_frame)
            if (self.playback_frame + 1) % 360 == 0:
                self.total_rotations.set((self.playback_frame - 1) // 360)
                self.parent.parent.sidebar_frame.update_rotations()

            # Lower Z-index of all circles and pendulum so trace is more visible
            self.tag_lower(self.arm)
            for circle in self.circles:
                self.tag_lower(circle)

            # Only begin drawing after 2 frames to allow minimum coordinates in list
            # Check frame skip setting and only draw and update on non skipped frames
            if self.playback_frame > 2 and self.playback_frame % (int(self.frame_skip.get()) + 1) == 0:
                self.tracer.draw()
                if not self.tracer_only_bool.get():
                    for circle in self.circles:
                        circle.draw()
                    self.arm.draw()
                time.sleep(1 / self.fps)
                self.update()

            if len(self.tracer.coords) > 2 and self.tracer.coords[0] == self.tracer.coords[-1]:
                self.playback_stopped = True
                self.tracer.draw()
                self.tracer_only_bool.get()
                if not self.tracer_only_bool.get():
                    for circle in self.circles:
                        circle.draw()
                    self.arm.draw()
                self.update()

    def draw_many(self) -> None:
        """Calculates and draws a specified number of frames in one step"""
        self.playback_stopped = True
        self.tracer.coords = []
        self.delete('all')
        # self.apply_mods()
        self.calc_start = time.time()
        self.create_many_images()

    def create_many_images(self):
        # CREATE MANY IMAGES

        img_path = r"C:\users\DK\desktop\test"
        for i in range(0, 28800):
            print(i)
            self.circles[1].radius += (1 / 12000)
            if self.arm.theta_mod >= 1.5:
                self.arm.theta_mod -= (1 / 12000)
            elif self.arm.theta_mod <= 1.5:
                self.arm.theta_mod += (1 / 12000)
            if self.circles[1].theta_mod >= 1.5:
                self.circles[1].theta_mod -= (1 / 12000)
            elif self.circles[1].theta_mod <= 1.5:
                self.circles[1].theta_mod += (1 / 12000)
            self.create_img(f'{img_path}/{str(i).zfill(3)}.png')

    def calculate_img_canvas_size(self) -> tuple[float, float]:
        size = round(((self.circles[0].radius * 2) + (
                self.arm.length_mod * self.circles[-1].radius)) * self.img_output_res_mod)
        return size + 10, size + 10

    def modify_coords_for_output(self) -> list:
        rounded_coords = []
        img_size = self.calculate_img_canvas_size()[0] // 2
        for i in self.tracer.coords:
            # rounded_coords.append(
            #     (
            #         round(((i[0] - self.center[0]) * self.img_output_res_mod) + self.width // 2),
            #         round(((i[1] - self.center[1]) * self.img_output_res_mod) + self.height // 2)
            #     )
            # )


            # adjusted for 4k
            rounded_coords.append(
                (
                    round((i[0] - self.center[0]) + self.width // 2),
                    round((i[1] - self.center[1]) + self.height // 2)
                )
            )
        return rounded_coords

    # @staticmethod
    # def compute_glow(rounded_coords, mod: tuple) -> tuple[tuple, ...]:
    #     new_coords = list(map(list, rounded_coords))
    #     for i in new_coords:
    #         i[0] += mod[0]
    #         i[1] += mod[1]
    #     return tuple(map(tuple, new_coords))

    def create_img(self, file_name):
        self.calc_start = time.time()
        print('Generating image...')
        iterations = 360 * self.rotation_mod * self.pixel_resolution
        for j in range(0, iterations):
            self.calculate_positions(j / self.pixel_resolution)
        self.rounded_coords = self.modify_coords_for_output()

        # CHANGE BACKGROUND COLOUR
        # img = Image.new(mode='RGB', size=self.calculate_img_canvas_size(), color=self.background_colour)

        # Auto calc img size
        # img = Image.new(mode='RGB', size=self.calculate_img_canvas_size(), color='black')

        # 4K output
        img = Image.new(mode='RGB', size=(3840, 2160), color='black')

        draw = ImageDraw.Draw(img)
        self.draw_pixels = True
        if self.draw_pixels:
            for i in self.rounded_coords:
                img.putpixel((i[0], i[1]), self.calculate_pixel_gradient(i))
        else:
            draw.line(self.rounded_coords, fill=(255, 255, 255), width=1)

        print(f'Completed in {time.time() - self.calc_start} seconds')
        print('Saving image...')

        if self.add_text_overlay:
            draw.text((30, self.height - 110),
                      f"Rotations per frame: {round(self.rotation_mod)}",
                      (255, 255, 255))
            draw.text((30, self.height - 120),
                      f"Arm Length Mod: {round(self.arm.length_mod, 4)}",
                      (255, 255, 255))
            draw.text((30, self.height - 130),
                      f"Arm Theta Mod: {round(self.arm.theta_mod, 4)}",
                      (255, 255, 255))
            for i in range(len(self.circles)):
                draw.text(
                    (30, self.height - 70 - (i * 10)),
                    f"Circle {i} - Radius: {round(self.circles[i].radius, 4)}, "
                    f"Theta Mod: {round(self.circles[i].theta_mod, 4)}",
                    (255, 255, 255)
                )
            draw.text((30, self.height - 30),
                      f"itsDanz0r Jan 2022",
                      (255, 255, 255))

        img.save(file_name)
        print('Done!')
        self.tracer.coords = []

        if self.playback_frame >= 600:
            self.playback_frame = 0
        # self.cycle_background_colour()
        self.cycle_gradient_colours()
        self.playback_frame += 1

    def calculate_pixel_gradient(self, pixel_coords):
        if self.outer_colour == self.inner_colour:
            return self.outer_colour[0], self.outer_colour[1], self.outer_colour[2]
        img_size = self.calculate_img_canvas_size()

        # Find the distance to the center
        distance_to_centre_in_pixels = math.sqrt(
            (pixel_coords[1] - self.height / 2) ** 2 + (pixel_coords[0] - self.width / 2) ** 2)

        # Make it on a scale from 0 to 1
        distance_to_centre = float(distance_to_centre_in_pixels / (math.sqrt(2) * 2300 / 2))

        # Calculate r, g, and b values
        r = round(self.outer_colour[0] * distance_to_centre + self.inner_colour[0] * (1 - distance_to_centre))
        g = round(self.outer_colour[1] * distance_to_centre + self.inner_colour[1] * (1 - distance_to_centre))
        b = round(self.outer_colour[2] * distance_to_centre + self.inner_colour[2] * (1 - distance_to_centre))
        return r, g, b

    def cycle_gradient_colours(self):
        i = self.playback_frame
        colour_increment = 120
        colour_change_freq = 2

        while True:
            if (colour_increment * 4) <= i <= (colour_increment * 5):
                self.inner_colour[1] -= colour_change_freq
                self.inner_colour[2] -= colour_change_freq
                break
            if (colour_increment * 3) <= i <= (colour_increment * 4):
                self.inner_colour[1] += colour_change_freq
                break
            if (colour_increment * 2) <= i <= (colour_increment * 3):
                self.inner_colour[1] -= colour_change_freq
                self.inner_colour[2] += colour_change_freq
                break
            if colour_increment <= i <= (colour_increment * 2):
                self.inner_colour[0] -= colour_change_freq
                self.inner_colour[1] += colour_change_freq
                break
            if 0 <= i <= colour_increment + 1:
                self.inner_colour[0] += colour_change_freq
                break

        # Cycle outer colour
        while True:
            if (colour_increment * 4) <= i <= (colour_increment * 5):
                self.outer_colour[0] += colour_change_freq
                self.outer_colour[1] += colour_change_freq
                break
            if (colour_increment * 3) <= i <= (colour_increment * 4):
                self.outer_colour[1] -= colour_change_freq
                self.outer_colour[2] += colour_change_freq
                break
            if (colour_increment * 2) <= i <= (colour_increment * 3):
                self.outer_colour[0] -= colour_change_freq
                self.outer_colour[1] += colour_change_freq
                break
            if colour_increment <= i <= (colour_increment * 2):
                self.outer_colour[0] += colour_change_freq
                break
            if 0 <= i <= colour_increment:
                self.outer_colour[0] -= colour_change_freq
                self.outer_colour[1] -= colour_change_freq
                self.outer_colour[2] -= colour_change_freq
                break













        print(self.inner_colour, self.outer_colour)
