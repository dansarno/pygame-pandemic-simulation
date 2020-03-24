import numpy as np
import health
import tools
import math


class Person:
    # add class variables here
    def __init__(self, box, age, size, status=health.healthy, days_infected=0, days_dead=0):
        self.box = box
        self.pos = np.random.rand(2) * self.box.dimensions
        self.age = age
        self.size = size
        self.status = status
        self.days_infected = days_infected
        self.days_dead = days_dead

        self.vector = np.array([tools.random_between(-1, 1), tools.random_between(-1, 1)]) * self.status.speed

    def transmission(self):
        """
        Transmits the virus to the person.

        Changes the status attribute of the person object to health.infected.

        Returns
        -------
        None

        """
        self.status = health.infected

    def check_up(self):
        """
        Checks the health of the person and performs an action.

        If the person's status is infected and...
            a. if they are over a certain age and been infected for a certain number of days they die
            b. if they are under a certain age and been infected for a certain number of days they recover
            c. else the number of days infected attribute increases by one.

        Returns
        -------
        None

        """
        if self.status == health.infected:
            if self.age > 80 and (self.days_infected > health.infected.frame_limit):
                self.status = health.dead
            elif self.age <= 80 and (self.days_infected > health.infected.frame_limit):
                self.status = health.recovered
            else:
                self.days_infected += 1
        if self.status == health.dead:
            self.days_dead += 1

    def move(self):
        """
        Moves the person to the new position.

        Adds the product of the direction vector attribute and speed of travel (health status dependant) attribute to
        the currently held position and updates the position attribute to the new value.

        Returns
        -------
        None

        """
        self.pos += self.vector * self.status.speed

    def boundary(self):
        """
        Updates the person's direction of travel if they have hit the environment's boundary.

        Checks if the position - accounting for the size of the person - has exceeded the dimensions of the simulation
        environment. The left and top edges being zero and the right and bottom edges being the x and y environment
        dimensions attribute respectively. If the condition is met, the person's vector attribute flips direction.

        Returns
        -------
        None

        """
        # TODO this could be writen better
        if self.pos[0] - self.size <= 0:
            self.vector[0] = np.abs(self.vector[0])
        if self.pos[1] - self.size <= 0:
            self.vector[1] = np.abs(self.vector[1])
        if self.pos[0] + self.size >= self.box.dimensions[0]:
            self.vector[0] = np.abs(self.vector[0]) * -1
        if self.pos[1] + self.size >= self.box.dimensions[1]:
            self.vector[1] = np.abs(self.vector[1]) * -1

    def collide(self, population, mode='basic'):
        if mode == 'basic':
            for other in population:
                # Only perform collision check for people that are not themselves
                if self is not other:
                    delta = self.pos - other.pos
                    distance = math.hypot(delta[0], delta[1])
                    if distance < self.size + other.size \
                            and (self.status == health.infected or other.status == health.infected) \
                            and (self.status == health.healthy or other.status == health.healthy):
                        self.transmission()
                        other.transmission()

        elif mode == 'selective':
            if self.status == health.healthy:
                for other in population:
                    if other.status == health.infected:
                        delta = self.pos - other.pos
                        distance = math.hypot(delta[0], delta[1])
                        if distance < self.size + other.size:
                            self.transmission()

        else:
            pass
            # TODO raise error here is mode is not recognised


class People:
    """
    This is a class for the collection of people as part of a single population.

    Attributes
    ----------
    n_people : int
        Total number of people in the population.
    n_infected : int
        Number of people initially infected in the population.
    box : object of type Area
        The environment which bounds the population.
    persons : list of objects of type Person
        Container for very person in the population.
    infection_free : bool
        Indicator of where the population is free from infection or not.
    stats : dict
        Container for the counts of the health status of very person in the population.

    """
    # add class variables here
    def __init__(self, box, n_people, n_infected):
        self.n_people = n_people
        self.n_infected = n_infected
        self.box = box
        self.persons = []
        self.infection_free = False
        self.stats = {'healthy': self.n_people - self.n_infected,
                      'recovered': 0,
                      'dead': 0,
                      'infected': self.n_infected
                      }

    def __len__(self):
        """Special method returning the length of the 'persons' attribute i.e. population size"""
        return len(self.persons)

    def __str__(self):
        """Special method returning a nicely formatted output for print"""
        human_readable_string = "Population \n" \
                                "-------------"
        for status_type, count in self.stats.items():
            human_readable_string += "\n" + f"{status_type.capitalize()}: {count}"
        return human_readable_string

    def __repr__(self):
        """Special method returning an unambiguous description of the object"""
        stats_string = f""
        i = 1
        for status_type, count in self.stats.items():
            stats_string += f"{' ' if i != 1 else ''}{count}{',' if i != len(self.stats) else ''}"
            i += 1
        return f"{self.__class__.__name__} ({stats_string})"

    def __getitem__(self, index):
        """Special method returning the person in the population given an index int"""
        return self.persons[index]

    def populate(self, size):
        """
        Creates many people and stores the objects in the 'persons' list attribute of this class.

        Two loops initialise people: bounded by the environment, with random age attributes ranging from 0 to 100
        (float) and of radius determined by the method input. The number of people created and their health status
        is determined the attributes n_people and n_infected.

        Parameters
        ----------
        size : int
            Radius, in number of pixels, of the people in the population to be generated.

        Returns
        -------
        None

        """
        for _ in range(self.n_people - self.n_infected):
            self.persons.append(Person(self.box,
                                       tools.random_between(0, 100),
                                       size=size
                                       ))
        for _ in range(self.n_infected):
            self.persons.append(Person(self.box,
                                       tools.random_between(0, 100),
                                       size=size,
                                       status=health.infected
                                       ))
        self.test_population()

    def update(self, mode_string):
        """
        All actions to be performed on each person stored in the 'persons' attribute of this class for each frame of
        animation.

        Parameters
        ----------
        mode_string : string
            Specify the method for determining the proximity of people.
            'basic' = every person is checked against all other people to see if they are close enough for transmission
            'selective' = only healthy people are checked against infected people to see if they are close enough for
                          transmission.

        Returns
        -------
        None

        """
        for person in self.persons:
            person.check_up()
            person.move()
            person.boundary()
            person.collide(self.persons, mode=mode_string)

    def test_population(self):
        """
        Update the 'stats' attribute of this class which keeps track of the health status of each person sorted in
        the 'persons' attribute. Also detects when the population has had no new infections and updates the
        'infection_free' boolean attribute.

        Returns
        -------
        None

        """
        healthy_count = 0
        infected_count = 0
        dead_count = 0
        recovered_count = 0
        for person in self.persons:
            if person.status == health.healthy:
                healthy_count += 1
            if person.status == health.infected:
                infected_count += 1
            if person.status == health.dead:
                dead_count += 1
            if person.status == health.recovered:
                recovered_count += 1

        if self.stats['infected'] == 0 and self.stats['recovered'] == recovered_count:
            self.infection_free = True

        self.stats = {'healthy': healthy_count,
                      'recovered': recovered_count,
                      'dead': dead_count,
                      'infected': infected_count
                      }
