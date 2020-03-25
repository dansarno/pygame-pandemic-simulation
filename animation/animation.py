import pygame
import tools
import population
import environment
import health
import numpy as np


def render_plot(people, origin, frame):
    """
    Renders live scrolling plot on screen.

    Parameters
    ----------
    people : People object
        The population whose statistics are to be plotted.
    origin : list
        Pixel coordinates, i.e. [x, y], of the top left corner of the plot area.
    frame : int
        The moment in time - as a frame number - at which the plot should be displayed.

    Returns
    -------
    None

    """
    delta_y = 0
    counts = list(people.stats.values())
    rounded_counts = tools.round_to_total(counts, total=100)
    for count, colours in zip(rounded_counts, list(configs['appearance']['people'].items())):
        if count == 0:
            continue
        pygame.draw.rect(screen,
                         colours[1],
                         ((origin[0] + frame) // 2, origin[1] + delta_y,
                          1, count),
                         0)
        delta_y += count


def render_population(people, origin):
    """
    Renders live simulation to screen. Note: origin parameter is currently unused.

    Parameters
    ----------
    people : People object
        The population whose simulation is to be displayed.
    origin : list
        Pixel coordinates, i.e. [x, y], of the top left corner of the simulation area.

    Returns
    -------
    None

    """
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
    """
    Renders live text updates of the population statistics to screen.

    Parameters
    ----------
    people : People object
        The population whose statistics are to be displayed.
    origin : list
        Pixel coordinates, i.e. [x, y], of the top left corner of the text area.

    Returns
    -------
    None

    """
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


if __name__ == '__main__':

    configs = tools.load_yaml('config.yaml')

    pygame.init()
    # Set up the drawing window
    screen = pygame.display.set_mode(configs['environment']['dimensions'])
    # set the pygame window name
    pygame.display.set_caption('Pandemic Simulation')

    font = pygame.font.SysFont(configs['appearance']['text']['font'], configs['appearance']['text']['size'])

    # Create environment object
    our_world = environment.Area(np.array(configs['environment']['dimensions']) - np.array([0, 150]))
    # Create a population for our environment
    our_population = population.People(our_world,
                                       configs['people']['number'],
                                       configs['people']['initially_infected'])
    our_population.populate(configs['people']['radius'],
                            configs['people']['age_range'])

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
        our_population.update(configs['pandemic']['at_risk_age'], configs['pandemic']['collision_detection'])
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
