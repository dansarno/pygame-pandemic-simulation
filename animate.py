import pygame
import tools
import numpy as np
import math
from random import random


def update(x, y, x_lim, y_lim, v_x, v_y):
    if (x - 5) <= 0:
        v_x = np.abs(v_x)
    if (y - 5) <= 0:
        v_y = np.abs(v_y)
    if x >= (x_lim - 5):
        v_x = np.abs(v_x) * -1
    if y >= (y_lim - 5):
        v_y = np.abs(v_y) * -1
    x += (0.1 * v_x)
    y += (0.1 * v_y)
    return x, y, v_x, v_y


def collide(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2

    distance = math.hypot(dx, dy)
    if distance < 5 + 5:
        print('Bang!')


if __name__ == '__main__':

    configs = tools.load_yaml('config.yaml')

    pygame.init()
    # Set up the drawing window
    screen = pygame.display.set_mode(configs['environment']['dimensions'])

    number_of_circles = 200
    x_positions = []
    y_positions = []
    x_speeds = []
    y_speeds = []
    for i in range(number_of_circles):
        random_number = random()
        if random_number < 0.5:
            x_speeds.append(0)
            y_speeds.append(0)
        else:
            x_speeds.append(tools.random_between(-2, 2))
            y_speeds.append(tools.random_between(-2, 2))
        x_positions.append(tools.random_between(5, configs['environment']['width'] - 5))
        y_positions.append(tools.random_between(5, configs['environment']['height'] - 5))

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with white
        screen.fill(configs['appearance']['bg_colour'])

        for i in range(number_of_circles):
            pygame.draw.circle(screen,
                               configs['appearance']['clear_colour'],
                               (int(x_positions[i]), int(y_positions[i])),
                               configs['people']['diameter'])

            x_positions[i], y_positions[i], x_speeds[i], y_speeds[i] = update(x_positions[i],
                                                                              y_positions[i],
                                                                              configs['environment']['width'],
                                                                              configs['environment']['height'],
                                                                              x_speeds[i],
                                                                              y_speeds[i]
                                                                              )

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
