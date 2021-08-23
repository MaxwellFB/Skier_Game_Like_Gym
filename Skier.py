# Listing_10-1.py
# Copyright Warren & Carter Sande, 2013
# Released under MIT license   http://www.opensource.org/licenses/mit-license.php
# Version $version  ----------------------------

# Skier program

import pygame, os, random

import time

# different images for the skier depending on his direction
"""
start = time. time()
"the code you want to test stays here"
end = time. time()
print(end - start)
"""

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path_image = '{}/images/'.format(dir_path)


def load_images():
    image_names = []

    for filename in os.listdir(dir_path_image):
        if any([filename.endswith(x) for x in ['.png']]):
            img_name = os.path.join(filename)
            if not filename.startswith(('skier_crash.png', 'skier_flag.png', 'skier_tree.png')):
                image_names.append(img_name)

    return image_names


def sort_images():
    image_order = ["skier_down.png", "skier_right1.png", "skier_right2.png", "skier_left2.png", "skier_left1.png"]
    unsorted_images = load_images()
    order_map = {}
    for pos, item in enumerate(image_order):
        order_map[item] = pos

    sorted_images = sorted(unsorted_images, key=order_map.get)

    return sorted_images


skier_images = sort_images()

"""
class GetImages(object):

    def __init__(self):
        self.folder = 'images/'
        self.image_order = ["skier_down.png", "skier_right1.png", "skier_right2.png","skier_left2.png", "skier_left1.png"]
        self.order_map = {}
        
        

    def load_images(self):
        self.image_names = []
        for filename in os.listdir(self.folder):
            if any([filename.endswith(x) for x in ['.png']]):
                img_name = os.path.join(filename)
                if not filename.startswith(('skier_crash.png', 'skier_flag.png', 'skier_tree.png')):
                    self.image_names.append(img_name)

        return self.image_names

    def sort_images(self):
        #self.sorted_images = self.load_images()
        
        for pos, item in enumerate(self.image_order):
            self.order_map[item] = pos

        #self.sorted_images = self.load_images(), self.sorted_images.sort(key=self.order_map.get)
        self.loaded_images = self.load_images()
        self.sorted_images = sorted(self.loaded_images, key=self.order_map.get)
        
        return self.sorted_images


#Sorted skier_images
#Simages = GetImages()

print(GetImages().load_images())
print(GetImages().sort_images())
skier_images1 = GetImages().sort_images()
print(skier_images1)
end = time. time()
print(end - start)

"""


# class for the Skier sprite
class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("{}skier_down.png".format(dir_path_image))
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0

    def turn(self, direction, speed, max_speed):
        # load new image and change speed when the skier turns
        self.angle = direction
        # self.angle = self.angle + direction
        # if self.angle < -2:  self.angle = -2
        # if self.angle > 2:  self.angle = 2

        center = self.rect.center
        self.image = pygame.image.load(dir_path_image + skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, speed]
        if speed[1] > max_speed: speed[1] = max_speed
        return speed

    def move(self):
        # move the skier right and left
        newSpeed = 0
        if self.angle == -1:  newSpeed= -10
        if self.angle == -2:  newSpeed= -20
        if self.angle == 1:  newSpeed = 10
        if self.angle == 2:  newSpeed = 20
        self.rect.centerx = self.rect.centerx + newSpeed
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620

    # class for obstacle sprites (trees and flags)


class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = dir_path_image + image_file
        self.image = pygame.image.load(self.image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False

    def update(self, speed):
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()


class Game():
    # create one "screen" of obstacles: 640 x 640
    # use "blocks" of 64 x 64 pixels, so objects aren't too close together
    def create_map(self):
        locations = []
        for _i in range(10):  # 10 obstacles per screen
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            location = [col * 64 + 32, row * 64 + 32 + 640]  # center x, y for obstacle
            if not (location in locations):  # prevent 2 obstacles in the same place
                locations.append(location)
                type = random.choice(["tree", "flag"])
                if type == "tree":
                    img = "skier_tree.png"
                elif type == "flag":
                    img = "skier_flag.png"
                obstacle = ObstacleClass(img, location, type)
                self.obstacles.add(obstacle)

    # redraw the screen, including all sprites
    def animate(self):
        self.screen.fill([255, 255, 255])
        self.obstacles.draw(self.screen)
        self.screen.blit(self.skier.image, self.skier.rect)
        self.screen.blit(self.score_text, [10, 10])
        pygame.display.flip()

    def start(self, keyboard_game=True, increase_speed=1, low_speed=6, max_speed=15):
        # initialize everything
        pygame.init()
        self.clock = pygame.time.Clock()
        self.increase_speed = increase_speed
        self.low_speed = low_speed
        self.max_speed = max_speed
        self.speed = [0, self.low_speed]
        self.obstacles = pygame.sprite.Group()  # group of obstacle objects
        self.skier = SkierClass()
        self.map_position = 0
        self.points = 0
        self.create_map()  # create one screen full of obstacles
        self.font = pygame.font.Font(None, 50)

        self.screen = pygame.display.set_mode([640, 640])

        if keyboard_game:
            # main Pygame event loop
            running = True
            key = 0
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:  # check for key presses
                       if event.key == pygame.K_LEFT:  # left arrow turns left
                           key = 1
                       elif event.key == pygame.K_RIGHT:  # right arrow turns right
                           key = 2
                       elif event.key == pygame.K_ESCAPE:  # ESC
                           running = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT and key == 1:
                            key = 0
                        elif event.key == pygame.K_RIGHT and key == 2:
                            key = 0
                self.step(key)

    def step(self, action):
        #while self.running:
        self.clock.tick(30)
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT: running = False

            #if event.type == pygame.KEYDOWN:  # check for key presses
            #    if event.key == pygame.K_LEFT:  # left arrow turns left
            #        speed = self.skier.turn(-1)
            #    elif event.key == pygame.K_RIGHT:  # right arrow turns right
            #        speed = self.skier.turn(1)
        # Straight
        if action == 0:
            self.speed = self.skier.turn(0, self.speed[1], self.max_speed)
        # Left
        elif action == 1:
            self.speed = self.skier.turn(-1, self.speed[1], self.max_speed)
        # Right
        elif action == 2:
            self.speed = self.skier.turn(1, self.speed[1], self.max_speed)

        self.skier.move()  # move the skier (left or right)
        self.map_position += self.speed[1]  # scroll the obstacles

        # create a new block of obstacles at the bottom
        if self.map_position >= 640:
            self.create_map()
            self.map_position = 0

        # check for hitting trees or getting flags
        hit = pygame.sprite.spritecollide(self.skier, self.obstacles, False)
        if hit:
            if hit[0].type == "tree" and not hit[0].passed:  # crashed into tree
                self.points = self.points - 100
                self.skier.image = pygame.image.load("{}skier_crash.png".format(dir_path_image))  # crash image
                self.animate()
                pygame.time.delay(1000)
                self.skier.image = pygame.image.load("{}skier_down.png".format(dir_path_image))  # resume skiing
                self.skier.angle = 0
                self.speed = [0, self.low_speed]
                hit[0].passed = True
            elif hit[0].type == "flag" and not hit[0].passed:  # got a flag
                self.points += 10
                self.speed[1] += self.increase_speed
                hit[0].kill()  # remove the flag

        self.obstacles.update(self.speed)
        self.score_text = self.font.render("Score: " + str(self.points), 1, (0, 0, 0))
        self.animate()

    def quit(self):
        pygame.quit()
