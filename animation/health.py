import tools
import numpy as np

configs = tools.load_yaml('config.yaml')


class Status:
    def __init__(self, status, speed, frame_limit):
        self.status = status
        self.speed = speed
        self.frame_limit = frame_limit


healthy = Status('healthy',
                 tools.random_between(configs['people']['healthy']['speed']),
                 tools.random_between(configs['people']['healthy']['frame_limit']))
infected = Status('infected',
                  tools.random_between(configs['people']['infected']['speed']),
                  tools.random_between(configs['people']['infected']['frame_limit']))
recovered = Status('recovered',
                   tools.random_between(configs['people']['recovered']['speed']),
                   tools.random_between(configs['people']['recovered']['frame_limit']))
dead = Status('dead',
              tools.random_between(configs['people']['dead']['speed']),
              tools.random_between(configs['people']['dead']['frame_limit']))
