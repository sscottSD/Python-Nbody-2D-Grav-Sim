import pygame
from pygame.locals import *
from math import *
import sys
import time
from decimal import *
import random
pygame.init()

class body:
        def __init__(self,boddx,boddy,velxA,velyA,massa): #(x,y,speedX,speedY,mass)
                self.x = boddx
                self.y = boddy
                self.mass = massa
                self.velx = float(velxA/10**0)
                self.vely = float(velyA/10**0)
                self.vector = (self.mass/pi*5)**(1/2.0)
                self.bod = (int(255-random.random()*200),int(255-random.random()*200),int(255-random.random()*200))

class SolarSystem:
        def __init__(self,size):
                self.size = size
                self.surface = pygame.display.set_mode((self.size[0],self.size[1]))
                self.bodys = []
                self.zoom = 1.0
                self.times = 0
                self.trace = False
                self.paused = False
                self.values = {}

        def calGrav(self,body_a,body_b):
                if not (body_a,body_b) in self.values and not (body_b,body_a) in self.values:
                        const_gravitacional = 6.67428E-11
                        xdif,ydif = (body_a.x-body_b.x) , (body_a.y-body_b.y)
                        dist = sqrt((xdif)**2+(ydif)**2) #Simplified to the next formula
                        if dist < (body_a.vector+body_b.vector): dist = body_a.vector+body_b.vector
                        force = (const_gravitacional*(body_a.mass*10**10)*(body_b.mass*10**10))/(dist*10**6)**2
#F = (Constant*massA*massB)/dist**2
                else:
                        if (body_b,body_a) in self.values:
                                val = self.values[(body_b,body_a)]
                                force = val[0]
                                xdif,ydif = -val[1][0],-val[1][1]
                                dist = val[2]
                if dist <= body_a.vector+body_b.vector+10:
                        aceleration = 0
                else:
                        aceleration = (force/body_a.mass)*10**3
                Xcomp = xdif/dist
                Ycomp = ydif/dist
                body_a.velx -= aceleration * Xcomp
                body_a.vely -= aceleration * Ycomp
                self.values[(body_a,body_b)] = (force,(xdif,ydif),dist)
                return force
        def move(self):
                self.values = {}
                for bA in self.bodys:
                        for bB in self.bodys:
                                if bA != bB:
                                        self.calGrav(bA,bB)

                for obj in self.bodys:
                        obj.x += obj.velx
                        obj.y += obj.vely

        def create(self,n,massa):
                for i in range(n):
                        self.bodys.append(body(random.random()*self.size[0],random.random()*self.size[1],0,0,massa))

        def demo (self):
                self.zoom = 0.1
                self.bodys = []
                self.surface.fill((10,0,30))
                self.bodys.append(body(400,-500,0.7,0.0,500.0))
                self.bodys.append(body(400,1500,-0.7,0.0,500.0))
                self.bodys.append(body(400,0,2.0,0.0,50.0))


        def draw(self):
                if not self.trace:
                        self.surface.fill((10,0,30))
                for B in self.bodys:
                        distx = abs(B.x - self.size[0]/2.0)
                        disty = abs(B.y - self.size[1]/2.0)
                        if B.x < self.size[0]/2.0:
                                x = B.x + distx*(1-self.zoom)
                        else:
                                x = B.x - distx*(1-self.zoom)

                        if B.y < self.size[1]/2.0:
                                y = B.y + disty*(1-self.zoom)
                        else:
                                y = B.y - disty*(1-self.zoom)

                        pygame.draw.circle(self.surface,B.bod,(int(x),int(y)),int(round(B.vector*self.zoom)))
                pygame.display.flip()

        def GetInput(self):
                key_pressed = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pressed()
                for event in pygame.event.get():
                        if event.type == QUIT or key_pressed[K_ESCAPE]:
                                pygame.quit()
                                sys.exit()

                        if mouse[0] and not key_pressed[K_n]:
                                mouse_x,mouse_y = pygame.mouse.get_pos()
                                distx,disty = abs(mouse_x-self.size[0]/2.0),abs(mouse_y-self.size[1]/2.0)
                                if mouse_x < self.size[0]/2.0:
                                        x = mouse_x + distx*(1-self.zoom**-1)
                                else:
                                        x = mouse_x - distx*(1-self.zoom**-1)

                                if mouse_y < self.size[1]/2.0:
                                        y = mouse_y + disty*(1-self.zoom**-1)
                                else:
                                        y = mouse_y - disty*(1-self.zoom**-1)
                                print x,y
                                self.bodys.append(body(x,y,0.0,0.0,100.0))

                        if mouse[1]:
                                mouse_x,mouse_y = pygame.mouse.get_pos
                                distx,disty = abs(mouse_x-self.size[0]/2.0),abs(mouse_y-self.size[1]/2.0)
                                if mouse_x < self.size[0]/2.0:
                                        x = mouse_x + distx*(1-self.zoom**-1)
                                else:
                                        x = mouse_x - distx*(1-self.zoom**-1)

                                if mouse_y < self.size[1]/2.0:
                                        y = mouse_y + disty*(1-self.zoom**-1)
                                else:
                                        y = mouse_y - disty*(1-self.zoom**-1)
                                print x,y
                                self.bodys.append(body(x,y,0.0,0.0,1000.0))

                        if mouse[2]:
                                mouse_x,mouse_y = pygame.mouse.get_pos()
                                distx,disty = abs(mouse_x-self.size[0]/2.0),abs(mouse_y-self.size[1]/2.0)
                                if mouse_x < self.size[0]/2.0:
                                        x = mouse_x + distx*(1-self.zoom**-1)
                                else:
                                        x = mouse_x - distx*(1-self.zoom**-1)

                                if mouse_y < self.size[1]/2.0:
                                        y = mouse_y + disty*(1-self.zoom**-1)
                                else:
                                        y = mouse_y - disty*(1-self.zoom**-1)
                                print x,y
                                self.bodys.append(body(x,y,2.0,0.0,100.0))

                        if key_pressed[K_DOWN]:
                                for i in self.bodys:
                                        i.y -= 50/self.zoom

                        elif key_pressed[K_UP]:
                                for i in self.bodys:

                                        i.y += 50/self.zoom

                        elif key_pressed[K_LEFT]:
                                for i in self.bodys:
                                        i.x += 50/self.zoom

                        elif key_pressed[K_RIGHT]:
                                for i in self.bodys:
                                        i.x -= 50/self.zoom

                        if key_pressed[K_r]:
                                self.trace = not self.trace

                        elif key_pressed[K_c]: #Clears the Screan
                                self.bodys = []
                                self.surface.fill((10,0,30))
                                self.zoom = 1.0

                        elif key_pressed[K_p]:
                                self.paused = not self.paused

                        elif key_pressed[K_z]:
                                self.zoom *= 2.0

                        elif key_pressed[K_x]:
                                self.zoom /= 2.0

                        elif key_pressed[K_d]:
                                self.demo()

        def collisionDetect(self):
                for B in self.bodys:
                        for B2 in self.bodys:
                                if B != B2:
                                        Distance2 = sqrt(  ((B.x-B2.x)**2)  +  ((B.y-B2.y)**2)  )

                                        if Distance2 < (B.vector+B2.vector) and Distance2 >
(B.vector+B2.vector)/3.0*2: #Objects collision
                                                Distance = B.vector+B2.vector
                                                dif = (B.x-B2.x,B.y-B2.y)
                                                angle = atan2(dif[0],dif[1])
                                                ra = B.vector/B2.vector
                                                inter = (B.x+B.vector*-sin(angle),B.y+B.vector*-cos(angle))
                                                B.x = inter[0] + B.vector*sin(angle)
                                                B.y = inter[1] + B.vector*cos(angle)
                                                B2.x = inter[0] + B2.vector*-sin(angle)
                                                B2.y = inter[1] + B2.vector*-cos(angle)
                                                B.velx = (B.velx*B.mass+B2.velx*B2.mass)/(B2.mass+B.mass)
                                                B.vely = (B.vely*B.mass+B2.vely*B2.mass)/(B2.mass+B.mass)
                                                B2.velx,B2.vely = B.velx,B.vely

                                        elif Distance2 <= (B.vector+B2.vector)/3.0*2: #Objects Fusion
                                                B.velx = ((B.mass*B.velx)+(B2.mass*B2.velx))/(B.mass+B2.mass)
                                                B.vely = ((B.mass*B.vely)+(B2.mass*B2.vely))/(B.mass+B2.mass)
                                                B.x = ((B.mass*B.x)+(B2.mass*B2.x))/(B.mass+B2.mass)
                                                B.y = ((B.mass*B.y)+(B2.mass*B2.y))/(B.mass+B2.mass)
                                                B.mass += B2.mass
                                                B.vector = sqrt(B.mass/pi*5)
                                                B.bod = ((B.bod[0]+B2.bod[0])/2.0,(B.bod[1]+B2.bod[1])/2.0,(B.bod[2]+B2.bod[2])/2.0)
                                                self.bodys.remove(B2)


        def main_loop(self):
                clock = pygame.time.Clock()
                while True:
                        clock.tick(200)
                        self.times += 1
                        self.GetInput()
                        if not self.paused:
                                self.move()
                                self.collisionDetect()
                        self.draw()

if __name__ == "__main__":
        if not len(sys.argv[1:]):
                print "The correct syntax is \'python pygravity X_size Y_size\'"
                print "But the Solar System will run in the default mode (800x600)."
                game = SolarSystem((800,600))
        elif len(sys.argv[1:]) == 2:
                game = SolarSystem((int(sys.argv[1]),int(sys.argv[2])))
        else:
                print "The correct syntax is \'python pygravity X_size Y_size\'"
                sys.exit()
        game.main_loop()
