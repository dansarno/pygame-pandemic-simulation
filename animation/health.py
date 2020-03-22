import tools
import numpy as np

configs = tools.load_yaml('config.yaml')


class Status:
    def __init__(self, status, speed, frame_limit):
        self.status = status
        self.speed = speed
        self.frame_limit = frame_limit


healthy = Status('healthy', tools.random_between(1, 2), np.nan)
infected = Status('infected', tools.random_between(0.5, 1.5), tools.random_between(250, 350))
recovered = Status('recovered', tools.random_between(1, 2), np.nan)
dead = Status('dead', 0.0, tools.random_between(200, 250))
