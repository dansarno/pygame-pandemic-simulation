import pygame
import tools
import population
import environment
import health
import numpy as np


def render_plot(plot_origin, stats, frame):
    delta_y = 0
    for stat, colours in zip(stats, list(configs['appearance'].items())):
        if stat == 0:
            continue
        pygame.draw.rect(screen,
                         colours[1],
                         ((plot_origin[0] + frame) // 2, plot_origin[1] + delta_y, 1, stat),
                         0)
        delta_y += stat


if __name__ == '__main__':

    configs = tools.load_yaml('config.yaml')

    pygame.init()
    # Set up the drawing window
    screen = pygame.display.set_mode(configs['environment']['dimensions'])
    # set the pygame window name
    pygame.display.set_caption('Pandemic Simulation')

    font = pygame.font.SysFont("arialrounded", 42)

    # Create environment object
    our_world = environment.Area(np.array(configs['environment']['dimensions']) - np.array([0, 150]))
    # Create a population for our environment
    our_population = population.People(our_world, configs['people']['number'], configs['people']['infected'])
    our_population.populate(configs['people']['radius'])

    screen.fill(configs['appearance']['bg_colour'])

    frame_number = 1
    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with the background colour
        pygame.draw.rect(screen,
                         configs['appearance']['bg_colour'],
                         (0, 0, configs['environment']['dimensions'][0], configs['environment']['dimensions'][1] - 125),
                         0)

        pygame.draw.rect(screen,
                         (200, 200, 200),
                         (0, configs['environment']['dimensions'][1] - 150, configs['environment']['dimensions'][0], 1),
                         0)

        for i, person in enumerate(our_population.persons):
            if person.status == health.clear:
                pygame.draw.circle(screen,
                                   configs['appearance']['clear_colour'],
                                   tuple(person.pos.astype(int)),
                                   configs['people']['radius'])

            if person.status == health.infected:
                pygame.draw.circle(screen,
                                   configs['appearance']['infected_colour'],
                                   tuple(person.pos.astype(int)),
                                   configs['people']['radius'])

            if person.status == health.recovered:
                pygame.draw.circle(screen,
                                   configs['appearance']['recovered_colour'],
                                   tuple(person.pos.astype(int)),
                                   configs['people']['radius'])

            if person.days_dead < health.dead.frame_limit and person.status == health.dead:
                pygame.draw.circle(screen,
                                   configs['appearance']['dead_colour'],
                                   tuple(person.pos.astype(int)),
                                   configs['people']['radius'])

        # Update positions and characteristics of each person in the population
        our_population.update()
        counts = our_population.test_population()

        render_plot([20, 475], counts, frame_number)

        # text = font.render(f"Clear: {counts[0]}", True, (0, 0, 0))
        # screen.blit(text, (50, 500 - text.get_height() // 2))
        #
        # text = font.render(f"Infected: {counts[1]}", True, (0, 0, 0))
        # screen.blit(text, (50, 560 - text.get_height() // 2))
        #
        # text = font.render(f"Dead: {counts[2]}", True, (0, 0, 0))
        # screen.blit(text, (320, 500 - text.get_height() // 2))
        #
        # text = font.render(f"Recovered: {counts[3]}", True, (0, 0, 0))
        # screen.blit(text, (320, 560 - text.get_height() // 2))

        # Flip the display
        pygame.display.flip()
        frame_number += 1

    # Done! Time to quit.
    pygame.quit()
