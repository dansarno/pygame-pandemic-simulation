import numpy as np
import health
import tools
import math


class Person:
    # add class variables here
    def __init__(self, box, age, size, status=health.clear, days_infected=0, days_dead=0):
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
            if self.age > 60 and (self.days_infected > health.infected.frame_limit):
                self.status = health.dead
            elif self.age <= 60 and (self.days_infected > health.infected.frame_limit):
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
                and (self.status == health.clear or other.status == health.clear):
            self.transmission()
            other.transmission()


class People:
    # add class variables here
    def __init__(self, box, n_people, n_infected):
        self.n_people = n_people
        self.box = box
        self.persons = []
        self.n_clear = n_people - n_infected
        self.n_infected = n_infected
        self.n_recovered = 0
        self.n_dead = 0

    def __len__(self):
        return len(self.persons)

    def populate(self, size):
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

    def update(self):
        for person in self.persons:
            person.check_up()
            person.move()
            person.boundary()
            for other_person in self.persons:
                # Only perform collision check for people that are not themselves
                if person is not other_person:
                    person.collide(other_person)

            # if person.status == health.dead and person.days_dead > health.dead.frame_limit:
            #     self.persons.remove(person)
            #     del person

    def test_population(self):
        clear_count = 0
        infected_count = 0
        dead_count = 0
        recovered_count = 0
        for person in self.persons:
            if person.status == health.clear:
                clear_count += 1
            if person.status == health.infected:
                infected_count += 1
            if person.status == health.dead:
                dead_count += 1
            if person.status == health.recovered:
                recovered_count += 1
        self.n_clear = clear_count
        self.n_infected = infected_count
        self.n_dead = dead_count
        self.n_recovered = recovered_count
        return [clear_count, infected_count, dead_count, recovered_count]