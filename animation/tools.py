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


def round_to_total(number_set, total=100, digit_after_decimal=0):
    """
        Largest Remainder Method
        This function takes a list of numbers and returns a new list of numbers which represent the portion of each that
        sum exactly to the desired 'total' value
    """
    unround_numbers = [x / float(sum(number_set)) * total * 10 ** digit_after_decimal for x in number_set]
    decimal_part_with_index = sorted([(index, unround_numbers[index] % 1) for index in range(len(unround_numbers))],
                                     key=lambda y: y[1], reverse=True)
    remainder = total * 10 ** digit_after_decimal - sum([int(x) for x in unround_numbers])
    index = 0
    while remainder > 0:
        unround_numbers[decimal_part_with_index[index][0]] += 1
        remainder -= 1
        index = (index + 1) % len(number_set)
    return [int(int(x) / float(10 ** digit_after_decimal)) for x in unround_numbers]


if __name__ == '__main__':
    counts = [43, 56, 75, 86, 97]
    rounded_counts = round_to_100_percent(counts)
    print(rounded_counts)
