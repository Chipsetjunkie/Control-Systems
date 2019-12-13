import pygame,sys
from car import Car
from km import Kalman_Filter
import time



mode = 1

if len(sys.argv) == 2:

    if sys.argv[1] in ('0','1'):
        print(sys.argv[1])
        mode = sys.argv[1]




gt = Car(mode)
gt.run()
k = Kalman_Filter(4,1)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    k.predict()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
            gt.drive(1)

    if pressed[pygame.K_DOWN]:
            gt.drive(2)

    if pressed[pygame.K_LEFT]:
            gt.drive(3)

    if pressed[pygame.K_RIGHT]:
            gt.drive(4)

    if pressed[pygame.K_SPACE]:
            gt.drive(5)

    if sum(pressed) == 0:
            gt.drive(0)



    pos_x,pos_y,vel_x,vel_y,acc_x,acc_y = gt.get_data()
    k.set_measure([pos_x,pos_y,vel_x,vel_y],acc_x,acc_y)
    corr_pos = k.Update()
    x_k,y_k = corr_pos[0],corr_pos[1]
    gt.k_cord = (x_k,y_k)
    '''
    k.predict()
    corr_pos = k.Update()
    x_k,y_k = corr_pos[0],corr_pos[1]
    gt.draw(x_k,y_k)
    k.set_measure([x_pos,y_pos,0,0])
    '''
