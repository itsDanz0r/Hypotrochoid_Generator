"""
Hypotrochoid Generator - main.py
Core app module
"""
import math
import time
from PIL import Image, ImageDraw, ImageFont

############
# SETTINGS #
############

RESOLUTION = (3840, 2160)
FRAMES_TO_GENERATE = 1440

FILE_PATH = r'D:\test'

PIXEL_DENSITY = 15
ROTATIONS_PER_FRAME = 50

CIRCLE_RADII = [1050, 630, 300, 50]
CIRCLE_THETA_MODS = [1, -2.3, 1.4, -1]
ARM_LENGTH_MOD = 1.1
ARM_THETA_MOD = -1.4

FONT = ImageFont.truetype("cour.ttf", 28)


class ImageFrame:
    def __init__(self, roulette, file_name):
        self.roulette = roulette
        self.resolution = RESOLUTION
        self.file_name = file_name
        self.img = None

    def output_png(self):
        calc_start = time.time()
        print(f'Generating image {self.roulette.frame} / {FRAMES_TO_GENERATE}...')
        self.img = Image.new(mode='RGB', size=self.resolution, color='black')

        for i in range(len(self.roulette.tracer.coords)):
            self.img.putpixel(
                self.roulette.tracer.mod_coords[i],
                self.roulette.calculate_pixel_gradient(self.roulette.tracer.coords[i])
            )
        self.draw_text_overlay()
        print('Saving image...')

        self.img.save(f'{FILE_PATH}/{str(self.file_name).zfill(3)}.png')
        print('Done!')
        print(f'Completed in {time.time() - calc_start} seconds')

    def draw_text_overlay(self):
        draw = ImageDraw.Draw(self.img)
        draw.text((60, self.resolution[1] - 190),
                  f"Rotations per frame: {round(ROTATIONS_PER_FRAME)}",
                  (255, 255, 255), font=FONT)
        draw.text((60, self.resolution[1] - 220),
                  f"Arm Length Mod: {round(self.roulette.arm.length_mod, 4)}",
                  (255, 255, 255), font=FONT)
        draw.text((60, self.resolution[1] - 250),
                  f"Arm Theta Mod: {round(self.roulette.arm.theta_mod, 4)}",
                  (255, 255, 255), font=FONT)
        for i in range(len(self.roulette.circles)):
            draw.text(
                (60, self.resolution[1] - 100 - (i * 30)),
                f"Circle {i} - Radius: {round(self.roulette.circles[i].radius, 4)}, "
                f"Theta Mod: {round(self.roulette.circles[i].theta_mod, 4)}",
                (255, 255, 255), font=FONT
            )
        draw.text((60, self.resolution[1] - 60),
                  f"Danny Kerr 2022",
                  (255, 255, 255), font=FONT)


class Roulette:
    """Core class that defines a hypotrochoid to be drawn"""

    def __init__(self, parent=None):
        self.parent = parent
        self.circles = []
        self.arm = None
        self.tracer = None
        self.rotations = 10
        self.frame = 0
        self.inner_colour = [0, 255, 255]
        self.outer_colour = [255, 0, 0]
        self.dimensions = (0, 0)
        self.resolution = (0, 0)
        self.center = (self.dimensions[0] // 2, self.dimensions[1] // 2)

    def calculate_size(self):
        size = round(((self.circles[0].radius * 2) + (self.arm.length_mod * self.circles[-1].radius)))
        self.dimensions = (size, size)
        self.center = (self.dimensions[0] // 2, self.dimensions[1] // 2)

    def calculate_positions(self, i) -> None:
        """Calculates all canvas drawing object positions"""
        for circle in self.circles:
            if type(circle.parent) != Roulette:
                circle.theta = circle.parent.radius / circle.radius * i
            circle.calculate_position()
        self.arm.theta = -self.arm.parent.theta * (self.arm.parent.parent.radius / self.arm.parent.radius)
        self.arm.calculate_position()
        self.tracer.coords.append((round(self.arm.end_coords[0], 4), round(self.arm.end_coords[1], 4)))

    def calculate_pixel_gradient(self, pixel_coords):
        if self.outer_colour == self.inner_colour:
            return self.outer_colour[0], self.outer_colour[1], self.outer_colour[2]

        # Find the distance to the center
        distance_to_centre_in_pixels = math.sqrt(
            (pixel_coords[1] - self.dimensions[1] / 2) ** 2 + (pixel_coords[0] - self.dimensions[0] / 2) ** 2)

        # Make it on a scale from 0 to 1
        distance_to_centre = float(distance_to_centre_in_pixels / (math.sqrt(2) * self.dimensions[0] / 2)) - 0.1

        # Calculate r, g, and b values
        r = round(self.outer_colour[0] * distance_to_centre + self.inner_colour[0] * (1 - distance_to_centre))
        g = round(self.outer_colour[1] * distance_to_centre + self.inner_colour[1] * (1 - distance_to_centre))
        b = round(self.outer_colour[2] * distance_to_centre + self.inner_colour[2] * (1 - distance_to_centre))
        return r, g, b

    def cycle_gradient_colours(self):
        i = self.frame
        colour_increment = 255
        colour_change_freq = 1

        while True:
            if (colour_increment * 4) <= i <= (colour_increment * 5):
                self.inner_colour[0] -= colour_change_freq
                self.inner_colour[1] += colour_change_freq
                self.inner_colour[2] += colour_change_freq
                break
            if (colour_increment * 3) <= i <= (colour_increment * 4):
                self.inner_colour[1] -= colour_change_freq
                self.inner_colour[0] += colour_change_freq
                break
            if (colour_increment * 2) <= i <= (colour_increment * 3):
                self.inner_colour[0] -= colour_change_freq
                self.inner_colour[1] += colour_change_freq
                self.inner_colour[2] -= colour_change_freq
                break
            if colour_increment <= i <= (colour_increment * 2):
                self.inner_colour[0] += colour_change_freq
                break
            if 0 <= i <= colour_increment + 1:
                self.inner_colour[1] -= colour_change_freq
                break

        while True:
            if (colour_increment * 4) <= i <= (colour_increment * 5):
                self.outer_colour[1] -= colour_change_freq
                self.outer_colour[0] += colour_change_freq
                break
            if (colour_increment * 3) <= i <= (colour_increment * 4):
                self.outer_colour[0] -= colour_change_freq
                self.outer_colour[1] += colour_change_freq
                self.outer_colour[2] -= colour_change_freq
                break
            if (colour_increment * 2) <= i <= (colour_increment * 3):
                self.outer_colour[0] += colour_change_freq
                break
            if colour_increment <= i <= (colour_increment * 2):
                self.outer_colour[1] -= colour_change_freq
                break
            if 0 <= i <= colour_increment + 1:
                self.outer_colour[0] -= colour_change_freq
                self.outer_colour[1] += colour_change_freq
                self.outer_colour[2] += colour_change_freq
                break

    def clear_coords_lists(self):
        self.tracer.coords = []
        self.tracer.mod_coords = []


class Circle:

    def __init__(self, radius: float = 10, theta: float = 0, theta_mod=0, parent=None):
        self.center = (0.0, 0.0)
        self.radius = radius
        self.parent = parent
        self.theta = theta
        self.theta_mod = theta_mod

    def calculate_position(self) -> None:
        """Calculate current position based on current properties"""
        if type(self.parent) == Roulette:
            self.center = self.parent.center

        else:
            self.center = polar_to_cartesian_with_offset(
                r=self.parent.radius - self.radius,
                theta=(self.radius / self.parent.radius) * self.theta * self.theta_mod,
                x_offset=self.parent.center[0],
                y_offset=self.parent.center[1]
            )


class Arm:
    def __init__(self, parent=None, theta_mod=1.0):
        self.parent = parent
        self.start_coords = self.parent.center
        self.end_coords = (0, 0)
        self.length_mod = 1
        self.theta = theta_mod
        self.theta_mod = theta_mod

    def calculate_position(self) -> None:
        """Calculate arm start and end position"""
        self.start_coords = self.parent.center
        self.end_coords = polar_to_cartesian_with_offset(
            r=self.parent.radius * self.length_mod,
            theta=self.theta * self.theta_mod,
            x_offset=self.parent.center[0],
            y_offset=self.parent.center[1]
        )


class Tracer:
    def __init__(self, parent=None):
        self.parent = parent
        self.coords = []
        self.mod_coords = []

    def modify_coords_for_output(self):
        rounded_coords = []
        for i in self.coords:
            rounded_coords.append(
                (
                    round((i[0] - self.parent.center[0]) + self.parent.resolution[0] // 2),
                    round((i[1] - self.parent.center[1]) + self.parent.resolution[1] // 2)
                )
            )
        self.mod_coords = rounded_coords


def polar_to_cartesian_with_offset(r=0.0, theta=0.0, x_offset=0.0, y_offset=0.0) -> tuple[float, float]:
    """Takes polar coordinates as input and returns cartesian coordinates"""
    x = (r * math.cos(math.radians(theta))) + x_offset
    y = (r * math.sin(math.radians(theta))) + y_offset
    return x, y


def define_roulette() -> Roulette:
    roulette = Roulette()
    roulette.circles.append(
        Circle(
            radius=CIRCLE_RADII[0],
            theta_mod=CIRCLE_THETA_MODS[0],
            parent=roulette
        )
    )
    for i in range(1, len(CIRCLE_RADII) - 1):
        roulette.circles.append(
            Circle(
                radius=CIRCLE_RADII[i],
                theta_mod=CIRCLE_THETA_MODS[i],
                parent=roulette.circles[i - 1]
            )
        )

    roulette.arm = Arm(
        parent=roulette.circles[-1],
        theta_mod=ARM_THETA_MOD
    )
    roulette.tracer = Tracer(
        parent=roulette
    )
    roulette.calculate_size()
    roulette.calculate_positions(1)
    roulette.resolution = RESOLUTION
    roulette.rotations = ROTATIONS_PER_FRAME
    return roulette


def calculate_geometry(roulette, degrees):
    for i in range(degrees * 360 * PIXEL_DENSITY):
        roulette.calculate_positions(i / PIXEL_DENSITY)


def oscillate_attribute(roulette, section, attribute, upper_bound, lower_bound, increment):

    if getattr(getattr(roulette, section), attribute) <= upper_bound:
        setattr(getattr(roulette, section), attribute, getattr(getattr(roulette, section), attribute) + increment)
    elif getattr(getattr(roulette, section), attribute) >= lower_bound:
        setattr(getattr(roulette, section), attribute, getattr(getattr(roulette, section), attribute) - increment)


def main():

    roulette = define_roulette()

    for i in range(FRAMES_TO_GENERATE):

        oscillate_attribute(roulette, 'arm', 'theta_mod', 1.5, -1.5, 1/32000)

        calculate_geometry(roulette, roulette.rotations)
        roulette.frame += 1

        roulette.cycle_gradient_colours()
        roulette.tracer.modify_coords_for_output()

        output_image = ImageFrame(roulette, i)
        output_image.output_png()

        del output_image
        roulette.clear_coords_lists()


if __name__ == '__main__':
    main()
