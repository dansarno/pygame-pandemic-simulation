import tools
import numpy as np
from random import randint

configs = tools.load_yaml('config.yaml')


class Status:
    def __init__(self, status, speed, frame_limit):
        # self.infectious = infectious
        # self.mobile = mobile
        # self.alive = alive
        # self.size = size
        self.status = status
        self.speed = speed
        self.frame_limit = frame_limit


clear = Status('clear', tools.random_between(1, 2), np.nan)
infected = Status('infected', tools.random_between(0.5, 1.5), 300)
recovered = Status('recovered', tools.random_between(1, 2), np.nan)
dead = Status('dead', 0.0, 200)
