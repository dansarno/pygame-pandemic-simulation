import numpy as np
import math
import health
import tools


class Person:
    """
    This is a class for each person in the population.

    Attributes
    ----------
    box : object of type Area
        The environment which bounds the person.
    age : float
        Person's age.
    size : int
        Radius, in number of pixels, of the person displayed in the simulation.
    status : attribute of the Status objects
        Health status of the person.
    days_infected : int
        Number of frames since the person was infected.
    days_dead : int
        Number of frames since the person died.
    pos : 2 element numpy array of floats
        x and y values defining the centre of the person's position in 2-D.
    vector : 2 element numpy array of floats
        Vx and Vy values defining the vector of motion for the person, scaled by the health status dependant speed

    """
    def __init__(self, box, age, size, status=health.healthy, days_infected=0, days_dead=0):
        self.box = box
        self.age = age
        self.size = size
        self.status = status
        self.days_infected = days_infected
        self.days_dead = days_dead
        self.pos = np.random.rand(2) * self.box.dimensions
        self.vector = np.array([tools.random_between([-1, 1]), tools.random_between([-1, 1])]) * self.status.speed

    def transmission(self):
        """Transmits the virus to the person. Changes the status attribute of the person object to health.infected."""
        self.status = health.infected

    def recovery(self):
        """The person recovers from infection. Changes the status attribute of the person object to health.recovered."""
        self.status = health.recovered

    def death(self):
        """The person dies from infection. Changes the status attribute of the person object to health.dead."""
        self.status = health.dead

    def check_up(self, age_lim):
        """
        Checks the health of the person and performs an action.

        If the person's status is infected and...
            a. if they are over a certain age and been infected for a certain number of days they die
            b. if they are under a certain age and been infected for a certain number of days they recover
            c. else the number of days infected attribute increases by one.

        Parameters
        ----------
        age_lim : float
            Age above which an infected person dies.

        Returns
        -------
        None

        """
        if self.status == health.infected:
            if self.age > age_lim and (self.days_infected > health.infected.frame_limit):
                self.death()
            elif self.age <= age_lim and (self.days_infected > health.infected.frame_limit):
                self.recovery()
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
        """
        Changes the health status of a person to infected if they come into contact with someone who is infected.

        Parameters
        ----------
        population : People object
            The population with which to check for collisions.
        mode : string
            Specify the method for determining the proximity of people.
            'basic' = every person is checked against all other people to see if they are close enough for transmission
            'selective' = only healthy people are checked against infected people to see if they are close enough for
                          transmission.

        Returns
        -------
        None

        """
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

    def __init__(self, box, n_people, n_infected, size, ages):
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

        # Populate with people...
        self.populate(size, ages)

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
            stats_string += f"{' ' if i != 1 else ''}{status_type.capitalize()[0]}: {count}{',' if i != len(self.stats) else ''}"
            i += 1
        return f"{self.__class__.__name__} ({stats_string})"

    def __getitem__(self, index):
        """Special method returning the person in the population given an index int"""
        return self.persons[index]

    def populate(self, size, ages):
        """
        Creates many people and stores the objects in the 'persons' list attribute of this class.

        Two loops initialise people: bounded by the environment, with random age attributes ranging from 0 to 100
        (float) and of radius determined by the method input. The number of people created and their health status
        is determined the attributes n_people and n_infected.

        Parameters
        ----------
        size : int
            Radius, in number of pixels, of the people in the population to be generated.
        ages : float
            Ages of the people to be added to the population.
        Returns
        -------
        None

        """
        for _ in range(self.n_people - self.n_infected):
            self.persons.append(Person(self.box,
                                       tools.random_between(ages),
                                       size=size
                                       ))
        for _ in range(self.n_infected):
            self.persons.append(Person(self.box,
                                       tools.random_between(ages),
                                       size=size,
                                       status=health.infected
                                       ))
        self.test_population()

    def update(self, age_lim, mode_string):
        """
        All actions to be performed on each person stored in the 'persons' attribute of this class for each frame of
        animation.

        Parameters
        ----------
        age_lim : float
            Age above which an infected person dies.
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
            person.check_up(age_lim)
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
