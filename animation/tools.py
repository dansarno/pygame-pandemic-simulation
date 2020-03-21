from random import random
import yaml
import pathlib


def random_between(start, stop):
    return ((stop - start) * random()) + start


def load_yaml(file):
    # Read YAML file containing configuration information
    yaml_path = pathlib.Path.cwd() / 'pandemic_simulation' / 'animation' / file
    with yaml_path.open(mode='r') as f:
        yaml_doc = f.read()
    return yaml.load(yaml_doc, Loader=yaml.FullLoader)


if __name__ == '__main__':
    print(random_between(-3, 3))
