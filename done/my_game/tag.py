import pygame
import pygame.locals
import random
import math

# Setup

pygame.init()
tick = 0
powerup_effects_list = ["speed_up", "speed_down", "jump_up", "dash"]
screen_width = 1800
screen_height = 1050
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My game")
a = int(input("Enter amount of seconds: "))
timer = a*60

clock = pygame.time.Clock()
global is_it
is_it = "red"
global tag_timer
tag_timer = 45

# Classes for objects

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass
class Player(GameObject):
    def __init__(self, x, y, image_path, keyleft, keyright, keyup, keydown, keyjump, keydash, color):
        super().__init__(x, y, image_path)
        self.powerup = "none"
        self.pad_jumping = False
        self.is_jumping = False 
        self.is_dashing = False


        self.speed = 6
        self.dash_speed = 24
        self.number_of_jumps = 1
        self.gravity = 1.3
        self.color = color

        self.jump_count = 5
        self.jump_height = 4

        
        self.dash_count = 0
        self.dash_timer = 8

        self.key_left = keyleft
        self.key_right = keyright
        self.key_up = keyup
        self.key_down = keydown
        self.key_jump = keyjump
        self.key_dash = keydash


        self.pad_jump_count = 6
        self.pad_jump_height = 6
        self.pad_jump_cooldown = 0


        self.powerup_length = 300
        self.powerup_image_path = "my_game/powerup_textures/blank_powerup.png"
        self.powerup_image = pygame.image.load(self.powerup_image_path).convert_alpha()
        self.powerup_rect = self.powerup_image.get_rect()
        self.powerup_placement = self.rect.midtop
        self.powerup_rect.midbottom = self.powerup_placement
        self.powerup_rect.y -= 10
    def update(self, keys):
        # Main update code
        global tag_timer
        tag_timer -= 1
        previous_x = self.rect.x
        previous_y = self.rect.y

        if self.powerup_length <= 0:
            self.powerup = "none"

        if self.powerup == "none" and self.dash_count == 0:
            self.powerup_image_path = "my_game/powerup_textures/blank_powerup.png"
            self.jump_height = 4
            self.speed = 6
            self.powerup_length = 300
        elif self.powerup == "speed_up":
            self.speed = 10
            self.powerup_length -= 1
            self.powerup_image_path = "my_game/powerup_textures/speed_powerup.png"
        elif self.powerup == "speed_down":
            self.speed = 3
            self.powerup_length -= 1
            self.powerup_image_path = "my_game/powerup_textures/slow_powerup.png"
        elif self.powerup == "jump_up":
            self.jump_height = 5
            self.powerup_length -= 1
            self.powerup_image_path = "my_game/powerup_textures/jump_boost_powerup.png"
        elif self.powerup == "dash":
            self.dash_count = 1
            self.powerup_image_path = "my_game/powerup_textures/dash_crystal.png"
            self.powerup = "none"
            
        self.powerup_image = pygame.image.load(self.powerup_image_path).convert_alpha()


        if self.pad_jump_cooldown > 0:
            self.pad_jump_cooldown -= 1


        dx, dy = 0, 0
        if keys[self.key_left]:
            dx -= 1
        if keys[self.key_right]:
            dx += 1
        if keys[self.key_up]:
            dy -= 1
        if keys[self.key_down]:
            dy += 1
        

        if keys[self.key_dash] and not self.is_dashing and (dx != 0 or dy != 0) and self.dash_count > 0:
            self.dash_direction = [dx, dy]
            self.is_dashing = True
            self.dash_timer = 8
            self.dash_count = 0
            length = (dx**2 + dy**2)**0.5  
            if length != 0:  
                self.dash_direction[0] /= length
                self.dash_direction[1] /= length


        if self.is_dashing:
            new_x = self.rect.x + self.dash_speed * self.dash_direction[0]
            new_y = self.rect.y + self.dash_speed * self.dash_direction[1]
            self.rect.x = new_x
            self.rect.y = new_y
            self.dash_timer -= 1
            
            if self.dash_timer <= 0:
                self.is_dashing = False


        collisions = pygame.sprite.spritecollide(self, platform_group, False)
        on_platform = False


        if keys[self.key_left] and not self.is_dashing:
            self.rect.x -= self.speed
        elif keys[self.key_right] and not self.is_dashing: 
            self.rect.x += self.speed
        for platform in collisions:
            if self.rect.y + self.rect.height <= platform.rect.top + 5:
                on_platform = True
    

        if on_platform and not self.is_jumping:
            self.number_of_jumps = 1
        

        was_on_ground = self.is_on_ground()


        if keys[self.key_jump] and self.number_of_jumps > 0 and not self.is_jumping and self.is_on_ground():
            self.is_jumping = True
            self.jump_count = self.jump_height

        
            
        if self.is_jumping:
            if self.jump_count >= -self.jump_height:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * self.gravity * neg 

                self.jump_count -= 0.2
            else:
                self.is_jumping = False
                self.jump_count = self.jump_height
        

        if self.pad_jumping:
            if self.pad_jump_count >= -self.pad_jump_count:
                neg = 1
                if self.pad_jump_count < 0:
                    neg = -1
                self.rect.y -= (self.pad_jump_count ** 2) * self.gravity * neg 

                self.pad_jump_count -= 0.2
            else:
                self.pad_jumping = False
                self.pad_jump_count = self.pad_jump_height
        

        if self.rect.y < screen_height - self.rect.height and not self.is_jumping and not self.is_dashing and not self.pad_jumping:
            self.rect.y += self.gravity * 10
        elif self.rect.y >= screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
            if not was_on_ground:
                self.number_of_jumps = 1


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0


        self.powerup_placement = self.rect.midtop
        self.powerup_rect.midbottom = self.powerup_placement
        self.powerup_rect.y -= 10


        self.handle_platform_collisions(previous_x, previous_y)
        self.handle_portal_collisions()
        self.handle_powerup_collisions()
        if not self.pad_jumping:
            self.handle_jump_pad_collisions()
        if is_it == self.color:
            self.image = pygame.image.load(f"my_game/player_textures/player_{self.color}_it.png").convert_alpha()
            self.handle_player_collisions()
        else:
            self.image = pygame.image.load(f"my_game/player_textures/player_{self.color}.png").convert_alpha() 


        return super().update()
    


    def handle_platform_collisions(self, previous_x, previous_y):
        collisions = pygame.sprite.spritecollide(self, platform_group, False)
        if not collisions:
            return
        for platform in collisions:
        
            if previous_y + self.rect.height <= platform.rect.top + 5: 
                self.rect.bottom = platform.rect.top
                self.is_jumping = False
                if self.number_of_jumps == 0:
                    self.number_of_jumps = 1
                self.dash_timer = 8
                return
            
            if previous_y >= platform.rect.bottom - 5: 
                self.rect.top = platform.rect.bottom
                self.jump_count = -self.jump_count 
                return
            
            if previous_x + self.rect.width <= platform.rect.left + 5:
                self.rect.right = platform.rect.left
            elif previous_x >= platform.rect.right - 5: 
                self.rect.left = platform.rect.right

    def handle_powerup_collisions(self):
        global powerup_effects_list
        powerup_hits = pygame.sprite.spritecollide(self, powerup_group, False)
        if powerup_hits:
            num = random.randint(0, 3)
            self.powerup = powerup_effects_list[num]
        for powerup in powerup_hits:
            powerup.kill()
        
            
    
    def handle_player_collisions(self):
        global tag_timer
        if tag_timer <= 0:
            if self.color == "red":
                collisions = pygame.sprite.spritecollide(self, blue_group, False)
                if collisions:
                    global is_it
                    is_it = "blue"
                    tag_timer = 30
            elif self.color == "blue":
                collisions = pygame.sprite.spritecollide(self, red_group, False)
                if collisions:
                    is_it = "red"
                    tag_timer = 30
    
    def handle_portal_collisions(self):
        portal_hits = pygame.sprite.spritecollide(self, portal_group, False)
        for portal in portal_hits:
            if portal.cooldown == 0:
                portal.teleport(self)
    def handle_jump_pad_collisions(self):
        pad_hits = pygame.sprite.spritecollide(self, jump_pad_group, False)
        if self.pad_jump_cooldown == 0:
            if pad_hits:
                self.pad_jumping = True
                self.pad_jump_cooldown = 20
        else:
            self.pad_jumping = False

    def is_on_ground(self):
        if self.rect.y >= screen_height - self.rect.height:
            return True
        
        if self.pad_jumping:
            return False
        
        for platform in platform_group:
            if (self.rect.bottom == platform.rect.top or 
                self.rect.bottom == platform.rect.top + 1) and (
                self.rect.right > platform.rect.left and 
                self.rect.left < platform.rect.right):
                return True
        
        return False
class Platform(GameObject):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
class Powerup(GameObject):
    def __init__(self, x, y, image_path):
        
        super().__init__(x, y, image_path)
class Jump_pad(GameObject):
    def __init__(self, x, y, image_path):
        
        super().__init__(x, y, image_path)
class Portal(GameObject):
    def __init__(self, x, y, image_path, destination_id):
        super().__init__(x, y, image_path)
        self.destination_id = destination_id
        self.cooldown = 0  

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def teleport(self, player):
        if self.cooldown == 0 and self.destination_id is not None:
         
            player.rect.x = self.destination_id.rect.x
            player.rect.y = self.destination_id.rect.y
  
            self.cooldown = 30
            self.destination_id.cooldown = 30
class Platform(GameObject):
    def __init__(self, x, y, image_path):
        
        super().__init__(x, y, image_path)
class MovingBlock(GameObject):
    def __init__(self, x, y, dir, tile_moves, speed, image_path):
        super().__init__(x, y, image_path)
        self.dir = dir
        
        self.x1 = x
        self.y1 = y
        
        self.x2 = x
        self.y2 = y
        if dir == "up":
            self.y2 -= 50 * tile_moves
        elif dir == "down":
            self.y2 += 50 * tile_moves
        elif dir == "left":
            self.x2 -= 50 * tile_moves
        elif dir == "right":
            self.x2 += 50 * tile_moves
        
        self.speed = speed

        self.moving_to_end = True
    
    def update(self):

        if self.moving_to_end:

            if self.dir == "up":
                self.rect.y -= self.speed
                if self.rect.y <= self.y2:
                    self.rect.y = self.y2
                    self.moving_to_end = False
            elif self.dir == "down":
                self.rect.y += self.speed
                if self.rect.y >= self.y2:
                    self.rect.y = self.y2
                    self.moving_to_end = False
            elif self.dir == "left":
                self.rect.x -= self.speed
                if self.rect.x <= self.x2:
                    self.rect.x = self.x2
                    self.moving_to_end = False
            elif self.dir == "right":
                self.rect.x += self.speed
                if self.rect.x >= self.x2:
                    self.rect.x = self.x2
                    self.moving_to_end = False
        else:

            if self.dir == "up":
                self.rect.y += self.speed
                if self.rect.y >= self.y1:
                    self.rect.y = self.y1
                    self.moving_to_end = True
            elif self.dir == "down":
                self.rect.y -= self.speed
                if self.rect.y <= self.y1:
                    self.rect.y = self.y1
                    self.moving_to_end = True
            elif self.dir == "left":
                self.rect.x += self.speed
                if self.rect.x >= self.x1:
                    self.rect.x = self.x1
                    self.moving_to_end = True
            elif self.dir == "right":
                self.rect.x -= self.speed
                if self.rect.x <= self.x1:
                    self.rect.x = self.x1
                    self.moving_to_end = True


def powerup_spawn():
    global all_sprites
    global powerup_group
    global powerup_spawn_list
    spawn_number = random.randint(1, int(len(powerup_spawns)/2))
    pX = powerup_spawns[f"x{spawn_number}"]
    pY = powerup_spawns[f"y{spawn_number}"]
    powerup_sprite = Powerup(pX, pY, "my_game/tile_textures/powerup.png")
    all_sprites.add(powerup_sprite)
    powerup_group.add(powerup_sprite)
    powerup_spawn_list.append(powerup_sprite)

# Sprite and other groups

red_group = pygame.sprite.Group()
blue_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
jump_pad_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()
portal_group = pygame.sprite.Group()

portals = [0, 0, 0, 0]
moving_blocks = []
powerup_spawn_list = []
spawn_points = {}
powerup_spawns = {}

# Create characters

character1 = Player(1, 1, "my_game/player_textures/player_red.png", pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE, pygame.K_LSHIFT, "red")
character2 = Player(100000, 100000, "my_game/player_textures/player_blue.png", pygame.K_j, pygame.K_l, pygame.K_i, pygame.K_k, pygame.K_n, pygame.K_PERIOD, "blue")

# Add sprites to groups

all_sprites.add(character1, character2)
red_group.add(character1)
blue_group.add(character2)
player_group.add(character1, character2)



# Level data

empty_level = [
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 000]

]
level_1 = [
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 72000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 10000, 51305, 51305, 51305, 10000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 54305, 10000, 51305, 10000, 52305, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 54305, 54305, 10000, 52305, 52305, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 54305, 10000, 53305, 10000, 52305, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 10000, 53305, 53305, 53305, 10000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 74000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [00000, 00000, 20000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 41000, 42000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000], 
    [10000, 10000, 10000, 00000, 30000, 30000, 30000, 00000, 00000, 00000, 00000, 10000, 10000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 71000, 00000, 00000, 00000, 00000, 00000, 00000, 73000, 00000, 00000, 00000, 00000, 00000, 00000, 00000, 00000]

]

# Building the level

def build_level(level_data):
    tile_size = 50

    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile == 71000:  
                portal_1 = Portal(x * tile_size, y * tile_size, "my_game/tile_textures/portal.png", None)
                portals[0] = portal_1
                portal_group.add(portal_1)
                all_sprites.add(portal_1)
            elif tile == 72000:
                portal_2 = Portal(x * tile_size, y * tile_size, "my_game/tile_textures/portal.png", None)
                portals[1] = portal_2
                portal_group.add(portal_2)
                all_sprites.add(portal_2)
            elif tile == 73000:  
                portal_3 = Portal(x * tile_size, y * tile_size, "my_game/tile_textures/portal_2.png", None)
                portals[2] = portal_3
                portal_group.add(portal_3)
                all_sprites.add(portal_3)
            elif tile == 74000:
                portal_4 = Portal(x * tile_size, y * tile_size, "my_game/tile_textures/portal_2.png", None)
                portals[3] = portal_4
                portal_group.add(portal_4)
                all_sprites.add(portal_4)
            
    if len(portals) >= 4:
        portals[0].destination_id = portals[1]
        portals[1].destination_id = portals[0]
        portals[2].destination_id = portals[3]
        portals[3].destination_id = portals[2]
    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile == 10000:
                platform = Platform(x * tile_size, y * tile_size, "my_game/tile_textures/platform.png")
                platform_group.add(platform)
                all_sprites.add(platform)
            elif tile == 20000:
                jumppad = Jump_pad(x * tile_size, y * tile_size + 35, "my_game/tile_textures/jumpPad.png")
                jump_pad_group.add(jumppad)
                all_sprites.add(jumppad)
            elif tile == 30000:
                powerup_spawns[f"x{int(len(powerup_spawns)/2 + 1)}"] = x*tile_size
                powerup_spawns[f"y{int(len(powerup_spawns)/2 + 0.5)}"] = y*tile_size
            elif tile == 41000:
                character1.rect.x = x*tile_size
                character1.rect.y = y*tile_size - 40
            elif tile == 42000:
                character2.rect.x = x*tile_size
                character2.rect.y = y*tile_size - 40
            elif str(tile)[0] == "5":
                if str(tile)[1] == "1":
                    dirTemp = "up"
                elif str(tile)[1] == "2":
                    dirTemp = "right"
                elif str(tile)[1] == "3":
                    dirTemp = "down"
                elif str(tile)[1] == "4":
                    dirTemp = "left"

                speedTemp = int(str(tile)[3])*10 + int(str(tile)[4])
                moving_block = MovingBlock(x*tile_size, y*tile_size, dirTemp, int(str(tile)[2]), speedTemp, "my_game/tile_textures/platform.png")
                platform_group.add(moving_block)
                moving_blocks.append(moving_block)
                all_sprites.add(moving_block)

build_level(level_1)

font = pygame.font.Font(None, 36)
text = "Time left:"
text_color = (255, 0, 0)
background_color = None

text_surface = font.render(text, True, text_color, background_color)
text_rect = text_surface.get_rect()
text_rect.center = (screen_width // 2, screen_height - 1000)


running = True
gameRunning = False
game_started = False
screen.fill((255, 255, 255))  

# Mainloop

while running:
    screen.fill((255, 255, 255))
    if not game_started:
        text = "Press P to start"
        text_surface = font.render(text, True, text_color, background_color)
        screen.blit(text_surface, text_rect)
    keys_2 = pygame.key.get_pressed()
    if keys_2[pygame.K_p]:
        gameRunning = True
        game_started = True
    if gameRunning:
        timer -= 1
        tick += 1
        if tick % 600 == 0:
            for powerup in powerup_spawn_list:
                powerup.kill()
            powerup_spawn_list = []
            powerup_spawn()
        
        
        keys = pygame.key.get_pressed()
        character1.update(keys)
        character2.update(keys)
        for portal in portals:
            portal.update()
        for sprite in all_sprites:
            if isinstance(sprite, MovingBlock):
                sprite.update()
        text = f"Time left: {math.ceil(timer/60)}" 
        text_surface = font.render(text, True, text_color, background_color)
        text_rect.center = (screen_width // 2, screen_height - 1000)
        screen.fill((255, 255, 255))  
        all_sprites.draw(screen)  
        if character1.powerup != "none" and character1.dash_count != 0:
            screen.blit(character1.powerup_image, character1.powerup_rect)
        if character2.powerup != "none" and character1.dash_count != 0:
            screen.blit(character2.powerup_image, character2.powerup_rect)
        screen.blit(text_surface, text_rect)
    

    if timer <= 0:
        gameRunning = False
        font = pygame.font.Font(None, 200)
        text = f"{is_it.capitalize()} lost." 
        text_surface = font.render(text, True, text_color, background_color)
        text_rect.center = (screen_width // 2 - 150, screen_height - 1000)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()