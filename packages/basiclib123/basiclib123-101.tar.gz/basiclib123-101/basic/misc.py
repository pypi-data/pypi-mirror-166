import random
import time as tile_lib

_start_time = tile_lib.time()

def rand(rand_max):
    """Generates random integer between 0 and rand_max.

    Args:
        rand_max (int): Maximum random number that rand can generate.

    Returns:
        int: Generated random number.
    """
    return random.randint(0, rand_max)


def time():
    """Returns number of seconds from the start of the program.

    Returns:
        float: Number of seconds that have passed from the start of the program.
    """
    return tile_lib.time() - _start_time
