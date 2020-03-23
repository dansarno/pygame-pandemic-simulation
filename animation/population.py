import numpy as np
import health
import tools
import math
from scipy.spatial.distance import pdist, cdist, squareform


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
        self.status = health.infected

    def check_up(self):
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
        self.pos += self.vector * self.status.speed

    def boundary(self):
        # TODO this could be writen better
        if (self.pos - self.size)[0] <= 0:
            self.vector[0] = np.abs(self.vector[0])
        if (self.pos - self.size)[1] <= 0:
            self.vector[1] = np.abs(self.vector[1])
        if self.pos[0] >= (self.box.dimensions - self.size)[0]:
            self.vector[0] = np.abs(self.vector[0]) * -1
        if self.pos[1] >= (self.box.dimensions - self.size)[1]:
            self.vector[1] = np.abs(self.vector[1]) * -1

    def collide(self, other):
        delta = self.pos - other.pos
        distance = math.hypot(delta[0], delta[1])
        if distance < self.size + other.size \
                and (self.status == health.infected or other.status == health.infected) \
                and (self.status == health.healthy or other.status == health.healthy):
            self.transmission()
            other.transmission()


class People:
    # add class variables here
    def __init__(self, box, n_people, n_infected):
        self.n_people = n_people
        self.box = box
        self.persons = []
        self.n_infected = n_infected
        self.infection_free = False
        self.stats = {'healthy': self.n_people - self.n_infected,
                      'recovered': 0,
                      'dead': 0,
                      'infected': self.n_infected
                      }
        self.positions_matrix = np.zeros([self.n_people, 2])
        self.vector_matrix = np.zeros([self.n_people, 2])

        self.healthy_positions = np.zeros([self.n_people - self.n_infected, 2])
        self.infected_positions = np.zeros([self.n_infected, 2])

    def __len__(self):
        return len(self.persons)

    def populate(self, size):
        for i in range(self.n_people - self.n_infected):
            healthy_person = Person(self.box,
                                    tools.random_between(0, 100),
                                    size=size
                                    )
            self.persons.append(healthy_person)
            self.positions_matrix[i] = healthy_person.pos
            self.vector_matrix[i] = healthy_person.vector
        for i in range(self.n_infected):
            infected_person = Person(self.box,
                                     tools.random_between(0, 100),
                                     size=size,
                                     status=health.infected
                                     )
            self.persons.append(infected_person)
            self.positions_matrix[i + (self.n_people - self.n_infected)] = infected_person.pos
            self.vector_matrix[i + (self.n_people - self.n_infected)] = infected_person.vector

    def update(self):
        collisions = self.check_collisions()
        for i, person in enumerate(self.persons):
            person.check_up()
            person.move()
            self.positions_matrix[i] = person.pos
            person.boundary()
            self.vector_matrix[i] = person.vector
            for j, other_person in enumerate(self.persons):
                if collisions[i][j] \
                        and (person.status == health.infected or other_person.status == health.infected) \
                        and (person.status == health.healthy or other_person.status == health.healthy):
                    person.transmission()
                    other_person.transmission()
            # for other_person in self.persons:
            #     # Only perform collision check for people that are not themselves
            #     if person is not other_person:
            #         person.collide(other_person)

    def check_collisions(self):
        dist_condensed = pdist(self.positions_matrix)
        return squareform(dist_condensed) < 5

    def check_collisions_2(self):
        dist_condensed = cdist(self.healthy_positions, self.infected_positions)
        return squareform(dist_condensed) < 8

    def test_population(self):
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
