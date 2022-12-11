"""
This is free program. Press space to pause game, press left mouse button to create another particle
"""

import random as rd
import sys
import pygame as pg


# DISPLAY
pg.init()
WIDTH = 1100
HEIGHT = 700
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Balls")
FPS = 60
clock = pg.time.Clock()

# SETTINGS
count_particles = 1000
radius = 10    # If Random_radius is False
mass = 10   # Need for physics
random_radius = [5, 30]     # Interval of random values != 0
speed_x = [-5, 6]     # Interval of random values
speed_y = [-5, 6]     # Interval of random values
speed_mouse = [1, 1]    # Speed mouse_particles

Random_colors = "Rainbow"   # False, True or "Rainbow". IF False, then choose selected_color below
Random_radius = False
Physics = False  # Physics in simulation
Spawn_particles = True  # Auto spawn

# COLORS
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ROZA = (200, 0, 55)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
YELLOW = (255, 255, 0)
COLORS = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (200, 0, 55), (255, 255, 255), (200, 200, 200), (255, 255, 0)]
selected_color = GREEN

# CONSTANTS
G = 6.67
g = 9.8
mouse_particles_spis = []


class Particle:
    def __init__(self, color, complete_particles, speed_mouse):
        self.color = color
        self.rand_colors = rand_colors()
        self.particles = complete_particles
        self.vx = speed_mouse[0]
        self.vy = speed_mouse[1]

    def draw_particles(self):
        if not Random_colors:
            for particle in self.particles:
                pg.draw.ellipse(screen, self.color, particle[0])

        elif Random_colors == "Rainbow":
            for particle in self.particles:
                pg.draw.ellipse(screen, rd.choice(COLORS), particle[0])

        else:
            i = 0
            for particle in self.particles:
                pg.draw.ellipse(screen, self.rand_colors[i], particle[0])
                i += 1

    def draw_mouse_particles(self):
        for particle in mouse_particles_spis:
            pg.draw.ellipse(screen, self.color, particle)

    #def attraction(self):
    #    for particle in self.particles:
    #        part = particle[0]
    #        other_x, other_y = part.x, part.y
    #        distance_x = other_x - self.x
    #        distance_y = other_y - self.y
    #        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    #    if planet.sun:
    #        self.distance_to_sun = distance

    #    force = self.G * self.mass * planet.mass / distance ** 2
    #    theta = math.atan2(distance_y, distance_x)
    #    force_x = math.cos(theta) * force
    #    force_y = math.sin(theta) * force
    #    return force_x, force_y

    def move_particles(self):
        if not Physics:
            for particle in self.particles:
                part = particle[0]
                part.x += particle[1][0]
                part.y += particle[1][1]

                if part.left <= 0:
                    particle[1][0] *= -1
                    part.x += 5

                if part.right >= WIDTH:
                    particle[1][0] *= -1
                    part.x -= 5

                if part.top <= 0:
                    particle[1][1] *= -1
                    part.y += 5

                if part.bottom >= HEIGHT:
                    particle[1][1] *= -1
                    part.y -= 5

            for particle in mouse_particles_spis:
                particle.x += self.vx
                particle.y += self.vy

                if particle.left <= 0:
                    self.vx *= -1
                    particle.x += 5

                if particle.right >= WIDTH:
                    self.vx *= -1
                    particle.x -= 5

                if particle.top <= 0:
                    self.vy *= -1
                    particle.y += 5

                if particle.bottom >= HEIGHT:
                    self.vy *= -1
                    particle.y -= 5

        else:
            for particle in self.particles:
                part = particle[0]
                if self == part:
                    if part.left <= 0:
                        particle[1][0] *= -1
                        part.x += 5

                    if part.right >= WIDTH:
                        particle[1][0] *= -1
                        part.x -= 5

                    if part.top <= 0:
                        particle[1][1] *= -1
                        part.y += 5

                    if part.bottom >= HEIGHT:
                        particle[1][1] *= -1
                        part.y -= 5


def rand_coord(count_particles):
    particles = []
    for particle in range(count_particles):
        x = rd.randint(0, WIDTH)
        y = rd.randint(0, HEIGHT)
        particles.append([x, y])
    return particles


def rand_colors():
    colors = []
    for i in range(count_particles):
        colors.append(rd.choice(COLORS))
    return colors


def rand_radius():
    global random_radius
    radius = []
    for i in range(count_particles):
        radius.append(rd.randint(random_radius[0], random_radius[1]))
    return radius


def create_particles(speed_x, speed_y, radius, ran_radius):
    particles = rand_coord(count_particles)
    rect_part = []
    speed = []
    if Random_radius:
        i = 0
        for particle in range(count_particles):
            x = particles[particle][0]
            y = particles[particle][1]
            vx = rd.randint(speed_x[0], speed_x[1])
            vy = rd.randint(speed_y[0], speed_y[1])
            part = pg.rect.Rect(x, y, ran_radius[i], ran_radius[i])
            rect_part.append(part)
            speed.append([vx, vy])
            i += 1
        complete_particles = list(zip(rect_part, speed))
        return complete_particles
    else:
        for particle in range(count_particles):
            x = particles[particle][0]
            y = particles[particle][1]
            vx = rd.randint(speed_x[0], speed_x[1])
            vy = rd.randint(speed_y[0], speed_y[1])
            part = pg.rect.Rect(x, y, radius, radius)
            rect_part.append(part)
            speed.append([vx, vy])
        complete_particles = list(zip(rect_part, speed))
        return complete_particles


def mouse_particles(x, y, radius):
    particle = pg.rect.Rect(x, y, radius, radius)
    mouse_particles_spis.append(particle)


def stop_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game_loop()


ran_radius = rand_radius()
complete_particles = create_particles(speed_x, speed_y, radius, ran_radius)

particle = Particle(selected_color, complete_particles, speed_mouse)


def game_loop():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    stop_loop()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coords = pg.mouse.get_pos()
                    mouse_particles(coords[0], coords[1], radius)


        screen.fill(BLACK)
        if Spawn_particles:
            particle.draw_particles()
        particle.draw_mouse_particles()
        particle.move_particles()

        clock.tick(FPS)
        pg.display.update()


if __name__ == "__main__":
    game_loop()
