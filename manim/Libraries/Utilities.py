from manim import *
import random

def random_color(seed):
    random.seed(seed)
    return utils.color.random_bright_color()

def most_signficant_bit(value):
    b = -1
    while value > 0:
        value = value >> 1
        b += 1
    return b