import os
import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame_graphics import setup_display, load_image
from colors_utilities import *
from math_utilities import *


class Rocket(pygame.sprite.Sprite):

    THRUSTERS_ON = "thrusters"
    THRUSTERS_OFF = "normal"
    ROTATION_LIMIT = 5.0  # rotation angle limit
    THRUSTER_LIMIT = 5.0  # thruster max speed

    def __init__(self, normal_img_path, thruster_img_path, position, bearing, group_list = None):
        super(Rocket, self).__init__(group_list)
        self._position = None
        self._bearing = bearing
        self.velocity = Vector2((0, 0))
        self.image_store = dict()

        self.add_graphic(Rocket.THRUSTERS_OFF, normal_img_path)
        self.add_graphic(Rocket.THRUSTERS_ON, thruster_img_path)
        self.image = self.image_store[Rocket.THRUSTERS_OFF]
        self.graphic = None
        self.rect = self.image.get_rect()  # self.graphic_rect.copy()
        self.move_to(position)
        self.thrust_on = Rocket.THRUSTERS_OFF
        self.rotate_to(self._bearing)

    def add_graphic(self, name, image_path):
        image, rect = load_image(image_path, colorkey = BLACK)
        image = pygame.transform.scale(image, (rect.w // 2, rect.h // 2))
        self.image_store[name] = image

    def move_to(self, location):
        self._position = Vector2(location)
        self.rect.center = self._position.xy
        # self.rect.move(self._position)

    def thrusters(self, thrust):
        if thrust:
            self.thrust_on = Rocket.THRUSTERS_ON
        else:
            self.thrust_on = Rocket.THRUSTERS_OFF

        self.image = self.image_store[self.thrust_on]
        self.rect = self.image.get_rect()
        self.rect.move((self._position.x, self._position.y))

    def is_thrusters(self):
        return self.thrust_on == Rocket.THRUSTERS_ON

    def rotate(self, angle):
        # new_angle = clamp(angle, -Rocket.ROTATION_LIMIT, Rocket.ROTATION_LIMIT)
        # self._bearing = (self._bearing + new_angle) % 360
        # self.rotate_to(self._bearing)
        pass

    def rotate_to(self, new_bearing):
        #
        # self.image = pygame.transform.rotate(self.image_store[self.thrust_on], new_bearing)
        # print(self._position)
        # self.rect = self.image.get_rect()
        # self.move_to((400, 400))
        pass

    def update(self, *args, **kwargs) -> None:
        if self.is_thrusters():
            # print(Rocket.THRUSTERS_ON)
            pass
        else:
            # print(Rocket.THRUSTERS_OFF)
            pass


if __name__ == '__main__':
    FPS = 60
    DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 800
    win_display, win_rect = setup_display(DISPLAY_WIDTH, DISPLAY_HEIGHT, "Asteroids Shooter!")
    IMG_FOLDER = os.path.join(os.path.dirname(__file__), "img")
    all_sprites = pygame.sprite.RenderUpdates()
    hero_group = pygame.sprite.RenderUpdates()
    rocket_ship = Rocket(os.path.join(IMG_FOLDER, "rocket_off.png"),
                         os.path.join(IMG_FOLDER, "rocket_thrusters.png"),
                         (win_rect.w // 2, win_rect.h // 2),
                         0,
                         [all_sprites, hero_group])

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)

        # check events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            print("Fire!")
        if keys[K_LEFT]:
            rocket_ship.rotate(Rocket.ROTATION_LIMIT)
        if keys[K_RIGHT]:
            rocket_ship.rotate(-Rocket.ROTATION_LIMIT)
        if keys[K_UP]:
            rocket_ship.thrusters(True)
        if not keys[K_UP]:
            rocket_ship.thrusters(False)

        # update objects
        all_sprites.update()

        # display screen
        win_display.fill(BLACK)
        all_sprites.draw(win_display)
        pygame.display.update(win_rect)

    pygame.quit()
