import pygame
import tools
import population
import environment
import health
import numpy as np


def render_plot(people, frame, configurations):
    """
    Renders live scrolling plot on screen.

    Parameters
    ----------
    people : People object
        The population whose statistics are to be plotted.
    frame : int
        The moment in time - as a frame number - at which the plot should be displayed.
    configurations : dict
        Configuration dictionary from yaml file.

    Returns
    -------
    None

    """
    delta_y = 0
    counts = list(people.status_numbers.values())
    rounded_counts = tools.round_to_total(counts, total=100)
    for count, colours in zip(rounded_counts, list(configurations['appearance']['people'].items())):
        if count == 0:
            continue
        pygame.draw.rect(screen,
                         colours[1],
                         ((configurations['appearance']['origins']['plot'][0] + frame) // 2,
                          configurations['appearance']['origins']['plot'][1] + delta_y,
                          1, count),
                         0)
        delta_y += count


def render_population(people, configurations):
    """
    Renders live simulation to screen. Note: origin parameter is currently unused.

    Parameters
    ----------
    people : People object
        The population whose simulation is to be displayed.
    configurations : dict
        Configuration dictionary from yaml file.

    Returns
    -------
    None

    """
    for i, person in enumerate(people.persons):
        if person.status == health.healthy:
            pygame.draw.circle(screen,
                               configurations['appearance']['people']['healthy_colour'],
                               tuple(person.pos.astype(int)),
                               configurations['people']['radius'])

        if person.status == health.infected:
            pygame.draw.circle(screen,
                               configurations['appearance']['people']['infected_colour'],
                               tuple(person.pos.astype(int)),
                               configurations['people']['radius'])

        if person.status == health.recovered:
            pygame.draw.circle(screen,
                               configurations['appearance']['people']['recovered_colour'],
                               tuple(person.pos.astype(int)),
                               configurations['people']['radius'])

        if person.days_dead < health.dead.frame_limit and person.status == health.dead:
            pygame.draw.circle(screen,
                               configurations['appearance']['people']['dead_colour'],
                               tuple(person.pos.astype(int)),
                               configurations['people']['radius'])


def render_text(people, configurations):
    """
    Renders live text updates of the population statistics to screen.

    Parameters
    ----------
    people : People object
        The population whose statistics are to be displayed.
    configurations : dict
        Configuration dictionary from yaml file.

    Returns
    -------
    None

    """
    # Cover text area
    pygame.draw.rect(screen,
                     configurations['appearance']['background']['bg_colour'],
                     (650, configurations['environment']['dimensions'][1] + 5,
                      configurations['environment']['dimensions'][0] - 650,
                      150),
                     0)
    i = 0
    j = 0
    for stat, colours in zip(list(people.status_numbers.items()), list(configurations['appearance']['people'].items())):
        text = font.render(f"{stat[0]}: {stat[1]}".capitalize(),
                           True,
                           colours[1])
        screen.blit(text,
                    (configurations['appearance']['origins']['text'][0] + (i * 140),
                     (configurations['appearance']['origins']['text'][1] + (j * 50))))
        if i == 1:
            i = 0
            j += 1
        else:
            i += 1


if __name__ == '__main__':

    pygame.init()
    configs = tools.load_yaml('config.yaml')
    # set the pygame window name
    pygame.display.set_caption('Pandemic Simulation')
    font = pygame.font.SysFont(configs['appearance']['text']['font'], configs['appearance']['text']['size'])

    area_for_plots_and_text = np.zeros(2, dtype=int)
    if configs['appearance']['show']['plot'] or configs['appearance']['show']['text']:
        area_for_plots_and_text = np.array([0, 130])

    # Set up the drawing window
    screen = pygame.display.set_mode(configs['environment']['dimensions'] + area_for_plots_and_text)

    # Create environment object
    our_world = environment.Area(np.array(configs['environment']['dimensions']))
    # Create a population for our environment
    our_population = population.People(our_world,
                                       configs['people']['number'],
                                       configs['people']['initially_infected'],
                                       configs['people']['radius'],
                                       configs['people']['age_range']
                                       )

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
                         (0,
                          0,
                          configs['environment']['dimensions'][0],
                          configs['environment']['dimensions'][1] + 5),  # 5 pixels buffer
                         0)

        if configs['appearance']['show']['plot'] or configs['appearance']['show']['text']:
            # Draw line between simulation and the plot
            pygame.draw.rect(screen,
                             (220, 220, 220),
                             (0,
                              configs['environment']['dimensions'][1],
                              configs['environment']['dimensions'][0], 1),
                             0)

        # Update positions and characteristics of each person in the population
        our_population.update(frame_number,
                              configs['pandemic']['at_risk_age'],
                              configs['pandemic']['collision_detection'],
                              configs['events'])
        our_population.test_population()

        render_population(our_population, configs)
        if not our_population.infection_free:
            if configs['appearance']['show']['plot']:
                render_plot(our_population,
                            frame_number,
                            configs)
        if configs['appearance']['show']['text']:
            render_text(our_population,
                        configs)

        # Flip the display
        pygame.display.flip()
        frame_number += 1

    # Done! Time to quit.
    pygame.quit()
