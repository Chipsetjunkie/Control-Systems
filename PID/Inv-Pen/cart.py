import pygame as pg
import sys
import math,time

pg.init()
clock = pg.time.Clock()
start = 0

class Cartpole():
    def __init__(self):
        self.screen = pg.display.set_mode((1300,700))
        self.center = [650,350]
        self.position = [350,150]
        self.radius = 200
        self.angle = math.radians(180)
        self.ang_vel = 3
        self.ang_acc = 0
        self.offset = math.radians(90)
        self.cart = self.center[:]
        self.c_acc = 0
        self.c_vel = 0
        self.font = pg.font.SysFont('bitstreamverasansmono', 15)
        self.acc_label = self.font.render('angular_acceleration:', True, (255, 255, 255))
        self.vel_label = self.font.render('angular_velocity:', True, (255, 255, 255))
        self.pos_label = self.font.render('Position:', True, (255, 255, 255))
        self.ang_label = self.font.render('Angle:', True, (255, 255, 255))
        self.auto_label = self.font.render('Auto:', True, (255, 255, 255))
        self.auto = 0
        self.motion = 0
        self.mag = 0
        self.pid = 0
        self.error = [[0,0,0,0,0,0,0],0]


    def rotate(self):
        x,y = self.position

        m = 0.9
        M = 1
        g = 9.81
        l = 1
        delta_t = 0.01
        theta = self.angle


        ang_vel =self.ang_vel
        ang_acc = (m*self.c_acc*math.cos(theta)+ -0.19*ang_vel-m*g*math.sin(theta))/m*l
        self.ang_acc = ang_acc
        c_acc = self.c_vel
        force = (M+m)*self.c_acc - m*l*ang_acc*math.cos(theta) + m*l*ang_vel**2*math.sin(theta)


        self.ang_vel += self.ang_acc * delta_t
        self.angle += ang_vel * delta_t
        self.c_vel += c_acc*delta_t
        self.c_acc += (force/M)*delta_t


        y = self.center[1] + math.sin(self.angle+self.offset)*self.radius
        x = self.center[0] + math.cos(self.angle+self.offset)*self.radius
        #self.center[0] += self.c_vel
        #self.center[0] = self.center[0]%1300

        self.position = [int(x),int(y)]
        self.c_acc= 0

    def draw(self):
        self.screen.fill([0,0,0])
        pg.draw.line(self.screen, [255,255,255], self.center, self.position, 2)
        pg.draw.rect(self.screen, [255,255,255], [self.center[0]-40,self.center[1]-20,80,40],2)
        pg.draw.circle(self.screen, [255,255,255],self.position,10)

        self.acc_text = self.font.render(str(round(self.ang_acc,2)), True, (255, 255, 0))
        self.vel_text = self.font.render(str(round(self.ang_vel,2)), True, (255, 255, 0))
        self.pos_text = self.font.render(str(self.position), True, (255, 255, 0))
        self.ang_text = self.font.render(str(math.degrees(self.angle)%360), True, (255, 255, 0))
        if self.auto == 0:
            self.auto_text = self.font.render(str(self.auto), True, (255, 0, 0))
        else:
            self.auto_text = self.font.render(str(self.auto), True, (0, 255, 0))


        self.screen.blit(self.acc_label,(0,10))
        self.screen.blit(self.vel_label,(0,30))
        self.screen.blit(self.pos_label,(0,50))
        self.screen.blit(self.ang_label,(0,70))
        self.screen.blit(self.auto_label,(1000,30))

        self.screen.blit(self.acc_text,(200,10))
        self.screen.blit(self.vel_text,(200,30))
        self.screen.blit(self.pos_text,(200,50))
        self.screen.blit(self.ang_text,(200,70))
        self.screen.blit(self.auto_text,(1100,30))


        pg.display.flip()


    def play(self):
        if self.motion == 0:
            self.motion =1
        self.rotate()

    def reset(self):
        self.angle = math.radians(360)
        self.ang_acc = 0
        self.ang_vel = 0
        self.motion  = 0
        self.pid = 0
        self.mag = 0

    def get_angle(self):
        return self.angle


############### PID ###################################

    def PID(self):
        error = math.radians(180) -(self.angle)%math.radians(360)
        e_i = self.error[0][1:0]
        e_i.append(error)
        edt = sum(e_i)
        e_d = self.error[1]
        De = error - e_d
        self.error = [e_i,De]
        kp = -10
        ki = -6.5 #2
        kd = -4
        #print(kp*error)
        opt = kp*error + ki*edt + kd*De
        self.c_acc = opt
        m = opt/abs(opt)
        self.center[0] += m*2
        self.center[0] = self.center[0]%1300


#################### Swing up Maneuver ###############
    def swingup(self):
        if self.motion ==1:
            if self.mag == 0:
                #print (self.ang_acc,self.ang_vel)
                self.mag =self.ang_acc/abs(self.ang_acc)

            else:
                if self.pid == 0:
                    if 160 < math.degrees(self.angle)%360 <200:
                        #print(math.degrees(self.angle)%360)
                        #input()
                        self.pid =1
                    if (self.ang_acc/abs(self.ang_acc) != self.mag):
                        self.mag *= -1

                    self.c_acc = self.mag*15
                    self.center[0] += self.mag
                    self.center[0] = self.center[0]%1300
                else:
                    if -1 <self.ang_vel < 3:
                        self.PID()

        else:
            pass



###########################  Main ####################
    def run(self,action = None):
        global start
        if action == '5':
            if self.auto == 0:
                start = time.time()
                print ("Initiated")
                self.auto = 1
                self.reset()
                self.c_acc = -15
                self.center[0] -= 3
                self.center[0] = self.center[0]%1300

        if self.auto == 0:
            if action == '1':
                self.center[0] -= 3
                self.center[0] = self.center[0]%1300
                self.c_acc = -15
                #self.F = -7.5

            if action == '2':
                self.center[0] += 3
                self.center[0] = self.center[0]%1300
                self.c_acc = 15
                #self.F = 7.5

            if action == '3':
                self.reset()

        else:
            if action == '4':
                print("time")
                print(time.time()-start)

            if action == '6':
                print ("disengaged")
                self.auto = 0


            self.swingup()



        self.play()


        clock.tick(120)
        self.draw()
