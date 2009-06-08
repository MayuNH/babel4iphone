import pygame
from pygame.locals import *

def get():
    return pygame.event.get()

def get_key_pressed():
    return pygame.key.get_pressed()
