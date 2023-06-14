import math
import random
from typing import Tuple, Any
from collections import namedtuple

WIDTH = 40
HEIGHT = 30

random_array = [random.Random(),random.Random()]

Size=namedtuple('Size', ['width', 'height'])
size=Size(WIDTH,HEIGHT)

verbose=False

def get_random_apple_data() -> Tuple[int, int]:
    """
    This method returns randomly drawn data for the apple
    :return: (x,y) - Random location on the board
    """
    x = random_array[0].randint(0, size.width - 1)
    y = random_array[0].randint(0, size.height - 1)

    if verbose:
        print(f'Apple(x={x},y={y})')
    
    return x, y

def get_random_wall_data() -> Tuple[int, int, str]:
    """
    This method returns randomly drawn data for the wall
    :return: (x,y,direction) Random location, and direction
    """
    x = random_array[1].randint(0, size.width - 1)
    y = random_array[1].randint(0, size.height - 1)
    direction = random_array[1].choice(["Up","Down","Left","Right"])

    if verbose:
        print(f'Wall(x={x},y={y},direction={direction})')
    
    return x, y, direction

def set_size(width:int, height:int) -> None:
    global size
    size=Size(width, height)

def set_verbose(flag:bool) -> None:
    global verbose
    verbose=flag

    
def set_random_seed(val: Any) -> None:
    """
    Internal: not for external usage
    :param val:
    :return:
    """
    if val is None:
        random_array[0].seed()
        random_array[1].seed()
    else:
        random_array[0].seed(f'apple{val}')
        random_array[1].seed(f'wall{val}')
