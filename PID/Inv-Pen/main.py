
'''
The model can be played by using keys 'left' and 'right'.
Autonomy mode can be toggled by pressing 'a'.
Once autonomy is triggered manual controls are locked i.e "left/right" wont work.
Press 'm' to deactivate autonomy.

'''
import pygame
import sys
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#import seaborn as sns
import math
import numpy as np

from cart import Cartpole as cp

print (__doc__)

a = cp()
a.run()


while 1:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            sys.exit()

    a.run()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        a.run('1')

    if pressed[pygame.K_RIGHT]:
        a.run('2')

    if pressed[pygame.K_UP]:
        a.run('3')

    if pressed[pygame.K_DOWN]:
        a.run('4')

    if pressed[pygame.K_a]:
        a.run('5')

    if pressed[pygame.K_m]:
        a.run('6')
