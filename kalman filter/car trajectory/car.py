import pygame
import math
import numpy as np
import warnings

print ("disable num lock and other default keys")
warnings.simplefilter("ignore")
pygame.init()
clock = pygame.time.Clock()


bd = np.load('boundary_bg.npy')
bd = list(zip(bd[1],bd[0]))


class Car:

    def __init__(self,m):
        self.k_cord = (None,None)
        self.size = (700,700)
        self.screen = pygame.display.set_mode(self.size)
        self.position = [0,0]
        self.velocity = [0,0]
        self.acceleration = [0,0]
        self.deccelerate = 0
        self.points = [(self.position[0]-15,self.position[1]-25),
                        (self.position[0]+15,self.position[1]-25),
                        (self.position[0]+15,self.position[1]+25),
                        (self.position[0]-15,self.position[1]+25)]
        self.headlight = [(self.position[0]-10,self.position[1]-20),
                        (self.position[0]+10,self.position[1]-20)]

        self.offset_angl = [240,300,60,120,243,297]
        self.angle = 0
        self.boundary = bd
        self.prev = []
        self.toggle = int(m)

    def heading(self,angle):
        center = self.position
        data = []
        radius = [25,25,25,25,20,20]
        for i in range(len(self.offset_angl)):
            theta = (angle+self.offset_angl[i])%360
            x_pos = center[0] + int(math.cos(theta*math.pi/180) *radius[i])
            y_pos = center[1] + int(math.sin(theta*math.pi/180)*radius[i])
            data.append((x_pos,y_pos))


        return data[:4],data[4:]


    def get_data(self):
        return self.position[0],self.position[1],round(self.velocity[0],1),round(self.velocity[1],1),\
                self.acceleration[0],self.acceleration[1]


    def draw(self):
        self.screen.fill((0,0,0))
        self.position[0] = max(min(self.position[0],675),25)
        self.position[1] = max(min(self.position[1],675),55)

        if self.toggle:
            if  75 < self.position[0] < 225 and 105 < self.position[1] < 255:
                self.position = self.prev

            if 75 < self.position[0] < 225 and 375 < self.position[1] < 625:
                self.position = self.prev

            if 275 < self.position[0] < 625 and 105 < self.position[1] < 625:
                self.position = self.prev

            for pt in self.boundary:
                pygame.draw.circle(self.screen,[255,255,255],pt,1)


        self.points,self.headlight = self.heading(self.angle)
        pygame.draw.polygon(self.screen,(255,0,0),self.points,1)
        pygame.draw.circle(self.screen, [0,255,0], self.headlight[0],1)
        pygame.draw.circle(self.screen, [0,255,0], self.headlight[1],1)


        if self.k_cord[0] != None:
            pygame.draw.circle(self.screen, [255,255,89], self.k_cord,3,1)
        pygame.draw.circle(self.screen, [255,20,89], self.position,1)

        pygame.display.flip()


    def physics(self):
        self.prev = self.position[:]
        self.position[0] += int(self.velocity[0])
        self.position[1] += int(self.velocity[1])

        if self.deccelerate:
                self.velocity[1] = self.velocity[1]*0.96
                self.velocity[0] = self.velocity[0]*0.96
        else:
            self.velocity[0] = self.velocity[0]*0.7
            self.velocity[1] = self.velocity[1]*0.7

    def run(self):
        self.physics()
        self.draw()


#drive should change acceleration which inturn changes velocity which goes onto changing the position.
# After each drive acceleration becomes zero, and velocity decreases with friction
# acceleration can be automated with pid .. a golden oppertunity I must say
# Use kalman filter to predict colision

    def drive(self,action=None):
        if action == 0:
            self.acceleration = [0,0]
            self.deccelerate = 1


        if action ==1:
            self.angle = 0
            self.deccelerate = 0
            self.acceleration[1] = max(self.acceleration[1]-0.05,-4)
            self.velocity[1] += self.acceleration[1]

        if action ==2:
            self.angle = 180
            self.deccelerate=  0
            self.acceleration[1] = min(self.acceleration[1]+0.05,4)
            self.velocity[1] += self.acceleration[1]

        if action ==3:
                self.angle = -90
                self.deccelerate=  0
                self.acceleration[0] = max(self.acceleration[0]-0.05,-4)
                self.velocity[0] += self.acceleration[0]

        if action ==4:
            self.angle = 90
            self.deccelerate=  0
            self.acceleration[0] = min(self.acceleration[0]+0.05,4)
            self.velocity[0] += self.acceleration[0]

        if action == 5:
            self.velocity = [0,0]


        clock.tick(60)
        self.run()
