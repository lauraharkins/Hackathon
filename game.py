import pygame
import numpy

WIDTH = 720
HEIGHT = 480
BACKGROUND = (0, 0, 0)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__(pygame.image.load("Assets/Pixel Adventure 1/Free/Main Characters/Pink Man/Jump (32x32).png"), startx, starty)

        self.speed = 4
        self.jump_speed = 20
        self.animation_index = 0
        self.facing_left = False
        self.vsp = 0
        self.gravity = 1

        self.load_sprites()

    def load_sprites(self):
        self.idle = load_sprite_sheet("Assets/Pixel Adventure 1/Free/Main Characters/Pink Man/Idle (32x32).png", 11)
        self.run = load_sprite_sheet("Assets/Pixel Adventure 1/Free/Main Characters/Pink Man/Run (32x32).png", 12)
        self.jump_image = pygame.image.load("Assets/Pixel Adventure 1/Free/Main Characters/Pink Man/Jump (32x32).png")

    def check_collision(self, x, y, blocks):
        self.rect.move_ip([x,y])
        collide = pygame.sprite.spritecollideany(self, blocks)
        self.rect.move_ip([-x,-y])
        return collide
    
    def move(self, x, y, blocks):
        dx = x
        dy = y

        while self.check_collision(0, dy, blocks):
            dy -= 1
        while self.check_collision(dx, dy, blocks):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx,dy])

    def idle_animation(self):
        if self.animation_index < len(self.idle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

        self.image = self.idle[self.animation_index]

        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def run_animation(self):
        self.image = self.run[self.animation_index]

        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.run)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_image
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, blocks):
        self.hsp = 0
        onground = self.check_collision(0, 1, blocks)

        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.run_animation()
            self.hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.hsp = self.speed
            self.facing_left = False
            self.run_animation()
        if key[pygame.K_UP] and onground:
            self.vsp = -self.jump_speed
        else:
            self.idle_animation()

        if self.vsp < 10 and not onground:
            self.jump_animation()
            self.vsp += self.gravity
        
        if self.vsp > 0 and onground:
            self.vsp = 0

        # movement 
        self.move(self.hsp, self.vsp, blocks)

class Block(Sprite):
    def __init__(self, sprite, startx, starty):
        super().__init__(sprite, startx, starty)

def load_sprite_sheet(filename, n):
    sheet = pygame.image.load(filename).convert_alpha()
    anim = []
    for i in range(n):
        img = pygame.Surface((32,32)).convert_alpha()
        img.blit(sheet, (0,0), (i*32, 0, 32, 32))
        anim.append(img)
    return anim

def load_2D_spritesheet(filename, n, m):
    sheet = pygame.image.load(filename).convert_alpha()
    sprites = [[0] * m for _ in range(n)]
    for j in range(m):
        for i in range(n):
            img = pygame.Surface((16,16)).convert_alpha()
            img.blit(sheet, (0,0), (j*16, i*16, 16, 16))
            sprites[i][j] = img
    return sprites

tilemap = {}
def load_tiles():
    tiles = load_2D_spritesheet("Assets/Pixel Adventure 1/Free/Terrain/Terrain (16x16).png", 11, 22)
    tilemap["grass_1"] = tiles[0][6]
    tilemap["grass_2"] = tiles[0][7]
    tilemap["grass_3"] = tiles[0][8]
    tilemap["grass_4"] = tiles[1][6]
    tilemap["grass_5"] = tiles[1][7]
    tilemap["grass_6"] = tiles[1][8]
    tilemap["grass_7"] = tiles[2][6]
    tilemap["grass_8"] = tiles[2][7]
    tilemap["grass_9"] = tiles[2][8]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)

    blocks = pygame.sprite.Group()
    load_tiles()

    for blk in range(8, WIDTH, 16):
        blocks.add(Block(tilemap["grass_2"], blk, HEIGHT-8))

    while True:
        pygame.event.pump()
        player.update(blocks)

        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        blocks.draw(screen)
        pygame.display.flip()

        clock.tick(60)



if __name__ == "__main__":
    main()