# classic astroid game for two players
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
a_score = 0
b_score = 0
lives = 3
time = 0.5
VEL_COEFFICIENT = 0.08
ANG_VEL = 0.05
COEFFICIENT = 8
started = False
explosion_group = set()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False, special = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        self.special = special

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    def get_special(self):
        return self.special

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35, 50)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

EXPLOSION_CENTER = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]
ship_explosion_info = ImageInfo(EXPLOSION_CENTER, EXPLOSION_SIZE, 25, 60, True, True)
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, missile_group):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.age = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.missile_group = missile_group
        self.lifespan = info.get_lifespan()
        self.special = info.get_special()

    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]),\
                              self.image_size, self.pos, self.image_size, self.angle)
        elif self.special:
             explosion_index = [self.age % EXPLOSION_DIM[0], (self.age // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
             canvas.draw_image(self.image,
                                [EXPLOSION_CENTER[0] + explosion_index[0] * EXPLOSION_SIZE[0],
                                 EXPLOSION_CENTER[1] + explosion_index[1] * EXPLOSION_SIZE[1]],
                                 EXPLOSION_SIZE, self.pos, EXPLOSION_SIZE)
             self.age += 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # update the ship position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update the ship angle
        self.angle += self.angle_vel

        # compute forward vectors
        forward_vector = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward_vector[0]
            self.vel[1] += forward_vector[1]

        # add a friction coefficient
        self.vel[0] *= 1 - VEL_COEFFICIENT
        self.vel[1] *= 1 - VEL_COEFFICIENT

        if self.age < self.lifespan:
            return False
        else:
            return True

    def increment_angle_vel(self):
        self.angle_vel += ANG_VEL

    def decrement_angle_vel(self):
        self.angle_vel -= ANG_VEL

    def set_thrust_on(self):
        self.thrust = True
        ship_thrust_sound.play()

    def set_thrust_off(self):
        self.thrust = False
        ship_thrust_sound.rewind()

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def shoot(self):
       missile_pos = [self.pos[0] + self.radius * math.cos(self.angle),self.pos[1] + self.radius * math.sin(self.angle)]
       missile_vel = [self.vel[0] + COEFFICIENT * math.cos(self.angle), self.vel[1] + COEFFICIENT * math.sin(self.angle)]
       a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info,missile_sound)
       self.missile_group.add(a_missile)

    def collide(self,other_object):
        if dist(self.pos, other_object.get_position()) < self.radius + other_object.get_radius():
            return True;
        else:
            return False;

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if not self.animated:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
        else:
            explosion_center = self.image_center
            explosion_size = self.image_size
            explosion_lifespan = self.lifespan
            current_explosion_index = (self.age % explosion_lifespan) // 1
            current_explosion_center = [explosion_center[0] + current_explosion_index * explosion_size[0], explosion_center[1]]
            explosion_sound.play()
            canvas.draw_image(explosion_image, current_explosion_center, explosion_size, self.pos, explosion_size)

    def update(self):
        # update the rock position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self,other_object):
        if dist(self.pos, other_object.get_position()) < self.radius + other_object.get_radius():
            return True;
        else:
            return False;

# process sprite group
def process_sprite_group(group, canvas):
    for sprite in set(group):
        if (sprite.update()):
            group.remove(sprite)
        sprite.draw(canvas)

def group_collide(group, other_object):
    for sprite in set(group):
        if (not sprite.collide(other_object)):
            continue
        else:
            group.remove(sprite)
            explosion_sprite = Sprite(sprite.get_position(),[0,0], 0, 0, explosion_image, explosion_info)
            explosion_group.add(explosion_sprite)
            return True
    return False

# key down handler
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        b_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP["right"]:
        b_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP["up"]:
        b_ship.set_thrust_on()
    elif key == simplegui.KEY_MAP["down"]:
        b_ship.shoot()
    elif key == simplegui.KEY_MAP["a"]:
        a_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP["d"]:
        a_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP["w"]:
        a_ship.set_thrust_on()
    elif key == simplegui.KEY_MAP["s"]:
        a_ship.shoot()

# key up handler
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        b_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP["right"]:
        b_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP["up"]:
        b_ship.set_thrust_off()
    elif key == simplegui.KEY_MAP["a"]:
        a_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP["d"]:
        a_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP["w"]:
        a_ship.set_thrust_off()

def new_game():
    global a_ship, b_ship
    global a_score, b_score
    a_score = 0
    b_score = 0
    # initialize ship
    a_ship = Ship([WIDTH / 4, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, set([]))
    b_ship = Ship([3 * WIDTH / 4, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, set([]))
    # replay the sound
    soundtrack.rewind()
    soundtrack.play()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    # start or restart the game
    if (not started) and inwidth and inheight:
        started = True
        new_game()

def draw(canvas):
    global time, a_score, b_score, started
    global a_ship, b_ship
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw and update ship
    a_ship.draw(canvas)
    canvas.draw_text('L', a_ship.get_position(), 40, 'White')
    if(a_ship.update()):
        new_game()
    b_ship.draw(canvas)
    canvas.draw_text('R', b_ship.get_position(), 40, 'White')
    if(b_ship.update()):
        new_game()

    # draw and update missiles
    process_sprite_group(a_ship.missile_group, canvas)
    process_sprite_group(b_ship.missile_group, canvas)

    # draw lives and scores
    canvas.draw_text('Score_A', (1 * WIDTH / 12, HEIGHT / 12), 40, 'White')
    canvas.draw_text(str(a_score), (1 * WIDTH / 8, HEIGHT / 6), 40, 'White')
    canvas.draw_text('Score_B', (4 * WIDTH / 5, HEIGHT / 12), 40, 'White')
    canvas.draw_text(str(b_score), (5 * WIDTH / 6, HEIGHT / 6), 40, 'White')

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

    # when ship A collide with the B missle
    if group_collide(b_ship.missile_group,a_ship):
        b_score += 1

    # when ship B collide with the A missle
    if group_collide(a_ship.missile_group,b_ship):
        a_score += 1

    # deal with explosion group
    process_sprite_group(explosion_group, canvas)

    if a_ship.collide(b_ship):
        a_ship = Ship(a_ship.get_position(), [0, 0], 0, ship_explosion_image, ship_explosion_info, set([]))
        b_ship = Ship(b_ship.get_position(), [0, 0], 0, ship_explosion_image, ship_explosion_info, set([]))

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
# initialize ship
a_ship = Ship([WIDTH / 4, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, set([]))
b_ship = Ship([3 * WIDTH / 4, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, set([]))

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

# get things rolling
frame.start()
