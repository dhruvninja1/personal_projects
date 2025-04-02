import pygame
import pygame.locals

pygame.init()

screen_width = 1800
screen_height = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My game")

clock = pygame.time.Clock()

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
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.speed = 4
        self.number_of_jumps = 1
        self.is_jumping = False
        self.jump_count = 5
        self.gravity = 1.3
        self.jump_height = 4
        self.dash_speed = 24
        self.is_dashing = False
        self.dash_count = 1
        self.dash_timer = 8
    def update(self, keys):
        
        previous_x = self.rect.x
        previous_y = self.rect.y
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        
        if keys[pygame.K_x] and not self.is_dashing and (dx != 0 or dy != 0) and self.dash_count > 0:
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


        if keys[pygame.K_LEFT] and not self.is_dashing:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and not self.is_dashing:
            self.rect.x += self.speed
        for platform in collisions:
            if self.rect.y + self.rect.height <= platform.rect.top + 5:
                on_platform = True
    
        if on_platform and not self.is_jumping:
            self.number_of_jumps = 1
            self.dash_count = 1
        
        was_on_ground = self.is_on_ground()

        if keys[pygame.K_SPACE] and self.number_of_jumps > 0 and not self.is_jumping and self.is_on_ground():
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

            
        if self.rect.y < screen_height - self.rect.height and not self.is_jumping and not self.is_dashing:
            self.rect.y += self.gravity * 10
        elif self.rect.y >= screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
            if not was_on_ground:
                self.number_of_jumps = 1
                self.dash_count = 1

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        
        self.handle_spike_collisions()
        self.handle_platform_collisions(previous_x, previous_y)
        self.handle_dash_crystal_collisions()


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
                self.dash_count = 1
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

    def handle_spike_collisions(self):
        spike_hits = pygame.sprite.spritecollide(self, spike_group, False)
        if spike_hits:
            self.rect.x = 50
            self.rect.y = 850
    def handle_dash_crystal_collisions(self):
        dash_crystal_hits = pygame.sprite.spritecollide(self, dash_crystal_group, False)
        if dash_crystal_hits:
            print("Crystal collided")
            self.dash_count = 1

    def is_on_ground(self):
        if self.rect.y >= screen_height - self.rect.height:
            return True
            
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
    
class Spike(GameObject):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
class Dash_crystal(GameObject):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)

character = Player(500, 1000, "my_game/player.png")
platform_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
dash_crystal_group = pygame.sprite.Group()
all_sprites.add(character)

empty_level = [
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00]

]

level_1 = [
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 10, 10, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 30, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 20, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 10, 10, 00], 
    [00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 23, 10, 10, 10, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [10, 10, 00, 00, 10, 10, 00, 00, 00, 00, 00, 00, 10, 10, 00, 00, 00, 00, 22, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00, 00], 
    [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]

]

def build_level(level_data):
    tile_size = 50
    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile == 10:
                platform = Platform(x * tile_size, y * tile_size, "my_game/platform.png")
                platform_group.add(platform)
                all_sprites.add(platform)
            elif tile == 20:
                spike = Spike(x * tile_size, y * tile_size + 35, "my_game/spikes.png")
                spike_group.add(spike)
                all_sprites.add(spike)
            elif tile == 21:
                spike = Spike(x * tile_size - 35, y * tile_size, "my_game/spikes_facing_right.png")
                spike_group.add(spike)
                all_sprites.add(spike)
            elif tile == 22:
                spike = Spike(x * tile_size, y * tile_size, "my_game/spikes_downwards.png")
                spike_group.add(spike)
                all_sprites.add(spike)
            elif tile == 23:
                spike = Spike(x * tile_size + 35, y * tile_size, "my_game/spikes_facing_left.png")
                spike_group.add(spike)
                all_sprites.add(spike)
            elif tile == 24:
                spike = Spike(x * tile_size, y * tile_size, "my_game/spinner.png")
                spike_group.add(spike)
                all_sprites.add(spike)
            elif tile == 30:
                dash_crystal = Dash_crystal(x * tile_size, y * tile_size, "my_game/dash_crystal.png")
                dash_crystal_group.add(dash_crystal)
                all_sprites.add(dash_crystal)

build_level(level_1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    character.update(keys)

    screen.fill((255, 255, 255))  
    all_sprites.draw(screen)  

    pygame.display.flip()
    clock.tick(60)

pygame.quit()