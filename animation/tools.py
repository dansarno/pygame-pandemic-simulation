from random import random
import yaml
import pathlib


def random_between(lower_upper_list):
    """Random number (float) between given lower and upper bounds stored in list as [lower, upper]"""
    return ((lower_upper_list[1] - lower_upper_list[0]) * random()) + lower_upper_list[0]


def load_yaml(file):
    """
    Loads the yaml file and returns a dictionary of the file contents.

    Parameters
    ----------
    file : string
        Name of the yaml file with extension i.e. 'filename.yaml'.

    Returns
    -------
    dict
        Structured contents of the yaml file.
    """
    yaml_path = pathlib.Path.cwd() / 'pandemic_simulation' / 'animation' / file
    with yaml_path.open(mode='r') as f:
        yaml_doc = f.read()
    return yaml.load(yaml_doc, Loader=yaml.FullLoader)


def round_to_total(number_set, total=100, digit_after_decimal=0):
    """
    Largest Remainder Method

    Function takes a list of numbers and returns a new list of numbers with the same proportions where the list sums
    exactly to the desired 'total' value and each element has the stipulated number of digits after the decimal point.

    Parameters
    ----------
    number_set : list of floats or ints
        List of numbers on which the function acts.
    total : float or int
        The total which the returned list must sum to.
    digit_after_decimal : int
        The number of digits after the decimal point each element fo the returned list must have.

    Returns
    -------
    list

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


# To be run for testing only
if __name__ == '__main__':
    print(random_between([0, 0]))
