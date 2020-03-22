import pygame
import tools
import population
import environment
import health
import numpy as np


def render_plot(people, origin, frame):
    delta_y = 0
    for stat, colours in zip(list(people.stats.items()), list(configs['appearance']['people'].items())):
        if stat[1] == 0:
            continue
        pygame.draw.rect(screen,
                         colours[1],
                         ((origin[0] + frame) // 2, origin[1] + delta_y, 1, stat[1]),
                         0)
        delta_y += stat[1]


def render_population(people, origin):
    for i, person in enumerate(people.persons):
        if person.status == health.healthy:
            pygame.draw.circle(screen,
                               configs['appearance']['people']['healthy_colour'],
                               tuple(person.pos.astype(int)),
                               configs['people']['radius'])

        if person.status == health.infected:
            pygame.draw.circle(screen,
                               configs['appearance']['people']['infected_colour'],
                               tuple(person.pos.astype(int)),
                               configs['people']['radius'])

        if person.status == health.recovered:
            pygame.draw.circle(screen,
                               configs['appearance']['people']['recovered_colour'],
                               tuple(person.pos.astype(int)),
                               configs['people']['radius'])

        if person.days_dead < health.dead.frame_limit and person.status == health.dead:
            pygame.draw.circle(screen,
                               configs['appearance']['people']['dead_colour'],
                               tuple(person.pos.astype(int)),
                               configs['people']['radius'])


def render_text(people, origin):
    # Cover text area
    pygame.draw.rect(screen,
                     configs['appearance']['background']['bg_colour'],
                     (650, 460, configs['environment']['dimensions'][0] - 460,
                      configs['environment']['dimensions'][1] - 400),
                     0)
    i = 0
    j = 0
    for stat, colours in zip(list(people.stats.items()), list(configs['appearance']['people'].items())):
        text = font.render(f"{stat[0]}: {stat[1]}".capitalize(),
                           True,
                           colours[1])
        screen.blit(text, (origin[0] + (i * 140), (origin[1] + (j * 50))))
        if i == 1:
            i = 0
            j += 1
        else:
            i += 1

    # text = font.render(f"Infected: {counts[1]}", True, (0, 0, 0))
    # screen.blit(text, (50, 560 - text.get_height() // 2))
    #
    # text = font.render(f"Dead: {counts[2]}", True, (0, 0, 0))
    # screen.blit(text, (320, 500 - text.get_height() // 2))
    #
    # text = font.render(f"Recovered: {counts[3]}", True, (0, 0, 0))
    # screen.blit(text, (320, 560 - text.get_height() // 2))


if __name__ == '__main__':

    configs = tools.load_yaml('config.yaml')

    pygame.init()
    # Set up the drawing window
    screen = pygame.display.set_mode(configs['environment']['dimensions'])
    # set the pygame window name
    pygame.display.set_caption('Pandemic Simulation')

    font = pygame.font.SysFont("arialrounded", 22)

    # Create environment object
    our_world = environment.Area(np.array(configs['environment']['dimensions']) - np.array([0, 150]))
    # Create a population for our environment
    our_population = population.People(our_world, configs['people']['number'], configs['people']['infected'])
    our_population.populate(configs['people']['radius'])

    screen.fill(configs['appearance']['background']['bg_colour'])

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
                         configs['appearance']['background']['bg_colour'],
                         (0, 0, configs['environment']['dimensions'][0], configs['environment']['dimensions'][1] - 125),
                         0)

        # Draw line between simulation and the plot
        pygame.draw.rect(screen,
                         (220, 220, 220),
                         (0, configs['environment']['dimensions'][1] - 150, configs['environment']['dimensions'][0], 1),
                         0)

        # Update positions and characteristics of each person in the population
        our_population.update()
        our_population.test_population()

        render_population(our_population, [0, 0])
        if not our_population.infection_free:
            render_plot(our_population, [20, 475], frame_number)
            render_text(our_population, [680, 480])

        # Flip the display
        pygame.display.flip()
        frame_number += 1

    # Done! Time to quit.
    pygame.quit()
