import math

import pygame
import random
from pygame.locals import *

fps = 30
pygame.init()
width, height = 900, 700
screen = pygame.display.set_mode((width, height))
speed = 0.5
fpsClock = pygame.time.Clock()
zoom = 0.5


gold = 10000
clicked = False
clicks = 0
selected = ""

bodies = []
buttons = []
G = 20 * speed**2
scale = 0.0001 #km

square = []
start_x = 0
start_y = 0

class orbital_body:
    def __init__(self, x, y, size, mass, colour, x_vel, y_vel, name):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.colour = colour
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.name = name

    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size)

class button:
    def __init__(self, x, y, button_size_x, button_size_y, text, visible, clickable, colour, name, price):
        self.x = x
        self.y = y
        self.button_size_x = button_size_x
        self.button_size_y = button_size_y
        self.text = text
        self.visible = visible
        self.clickable = clickable
        self.colour = colour
        self.name = name
        self.price = price
    def display(self):
        if self.visible and self.clickable:
            pygame.draw.rect(screen, self.colour, pygame.Rect(self.x, self.y, self.button_size_x, self.button_size_y))
        if self.visible and not self.clickable:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(self.x, self.y, self.button_size_x, self.button_size_y))
    def check_input(self, x, y):

        if x > self.x and x < self.x + self.button_size_x:
            if y > self.y and y < self.y + self.button_size_y:
                print("click")
                return True
        return False


for x in range(0):
    mass = random.randint(1, 20)

    bodies.append(orbital_body(random.randint(1, width)*zoom + (width*zoom)*0.5, random.randint(1, height)*zoom + (height*zoom)*0.5, mass*2*zoom, mass*zoom, (random.randint(1,255), random.randint(1,255), random.randint(1,255)), 0, 0, "planet"))

buttons.append(button(20, 20, 120, 50, "suns", True, True, (255, 255, 0), "small sun", 300))
buttons.append(button(20, 80, 100, 40, "planets", True, True, (50, 50, 200), "small planet", 30))
buttons.append(button(20, 130, 100, 40, "planets", True, True, (255, 50, 10), "Gas Giant", 60))

buttons.append(button(20, 180, 100, 40, "suns", True, True, (100, 100, 100), "comet", 10))
buttons.append(button(20, 230, 100, 40, "planets", True, True, (10, 0, 0), "black hole", 200))
buttons.append(button(20, 280, 100, 40, "planets", True, True, (200, 200, 200), "moon", 5))

buttons.append(button(20, 330, 100, 40, "planets", True, True, (230, 230, 230), "dark matter", 250))
def apply_gravity(body):
    x_vel = 0
    y_vel = 0
    other_bodies = bodies.copy()
    other_bodies.remove(body)
    if body.name != "small sun,":
        for O_body in other_bodies:
            distance = math.sqrt((abs(O_body.x - body.x))**2 + (abs(O_body.y - body.y))**2)
            if distance <= body.size + O_body.size and O_body.mass >= body.mass:

                ratio = O_body.mass / body.mass
                print(ratio)
                bodies.append(orbital_body(O_body.x,O_body.y, body.size/math.pi+O_body.size, body.mass+O_body.mass,
                                           (O_body.colour), (O_body.x_vel*ratio+body.x_vel)/ratio,
                                           (O_body.y_vel*ratio+body.y_vel)/ratio, O_body.name))

                bodies.remove(body)
                bodies.remove(O_body)
                return

            force = ((G*body.mass * O_body.mass)/distance**2)
            direction = math.atan2(O_body.y - body.y, O_body.x - body.x)
            direction *= (180/math.pi)
            direction += 90

            if direction < 0:
                direction = 360 + direction
            body.x_vel += round(math.cos(math.radians((direction-90))), 10) * force/body.mass
            body.y_vel += round(math.sin(math.radians((direction-90))), 10) * force/body.mass

        body.x += body.x_vel
        body.y += body.y_vel




def update(body):
    body.x *= zoom
    body.y *= zoom
    #body.x += (width*zoom)/2
    #body.y += (height*zoom)/2

    body.size *= zoom


def buy_planet(button, planet):
    global gold, selected

    if button.name == planet:
        if gold >= button.price:
            gold -= button.price
            print("brought", button.name, " balance: ", gold)
            selected = button.name
def key_inputs():
    global speed
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT]:
        for body in bodies:
            body.x += 10
    if keys_pressed[pygame.K_RIGHT]:
        for body in bodies:
            body.x -= 10
    if keys_pressed[pygame.K_UP]:
        for body in bodies:
            body.y += 10
    if keys_pressed[pygame.K_DOWN]:
        for body in bodies:
            body.y -= 10
    if keys_pressed[pygame.K_SPACE]:
        sun_x = 0
        sun_y = 0
        for body in bodies:
            if body.name == "small sun":
                sun_x = body.x - width/2
                sun_y = body.y - height/2

        for body in bodies:
            body.x -= sun_x
            body.y -= sun_y

    if keys_pressed[K_EQUALS]:
        speed += 0.1
        print(speed)
    if keys_pressed[K_MINUS]:
        speed -= 0.1
        print(speed)





while True:



    key_inputs()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        x, y = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONUP and selected != "" and clicked:
            if clicks == 2:
                clicks = 0
                print(selected, "released")

                if selected == "small planet":
                    bodies.append(orbital_body(start_x, start_y, 10*speed, 10, (0, 0, 255), ((x-start_x)/40)*speed, ((y-start_y)/40)*speed, "small planet"))
                if selected == "small sun":
                    bodies.append(orbital_body(start_x, start_y, 50*speed, 1000, (255, 255, 0), 0, 0, "small sun"))
                if selected == "Gas Giant":
                    bodies.append(orbital_body(start_x, start_y, 30*speed, 15, (255, 50, 0), ((x-start_x)/50)*speed, ((y-start_y)/50)*speed, "Gas Giant"))

                if selected == "comet":
                    bodies.append(orbital_body(start_x, start_y, 5*speed, 1, (100, 100, 100), ((x-start_x)/20)*speed, ((y-start_y)/20)*speed, "comet"))
                if selected == "black hole":
                    bodies.append(orbital_body(start_x, start_y, 20*speed, 300, (0, 0, 0), ((x-start_x)/150)*speed, ((y-start_y)/150)*speed, "black hole"))
                if selected == "moon":
                    bodies.append(orbital_body(start_x, start_y, 4*speed, 4, (50, 50, 50), ((x-start_x)/20)*speed, ((y-start_y)/20)*speed, "moon"))
                if selected == "dark matter":
                    bodies.append(orbital_body(start_x, start_y, 10*speed, -100, (255, 250, 250), ((x - start_x) / 150) * speed,((y - start_y) / 150) * speed, "dark matter"))






                clicked = False



            else:
                clicks += 1



        if event.type == MOUSEBUTTONDOWN:


            if not clicked:
                for button in buttons:
                    if button.clickable:
                        if button.check_input(x, y):
                            buy_planet(button, "small planet")
                            buy_planet(button, "small sun")
                            buy_planet(button, "Gas Giant")
                            buy_planet(button, "comet")
                            buy_planet(button, "black hole")
                            buy_planet(button, "moon")
                            buy_planet(button, "dark matter")


                            clicked = True
            elif clicked and not button.check_input(x, y) and clicks == 1:
                start_x = x
                start_y = y
                print("placed", selected)


    screen.fill((0, 0, 50))
    #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect()


    for body in bodies:
        #update(body)
        apply_gravity(body)
        square.append((body.x, body.y))
        body.display()



    for button in buttons:
        if gold < button.price:
            button.clickable = False

        else:
            button.clickable = True
        button.display()

    pygame.display.flip()
    fpsClock.tick(fps)
