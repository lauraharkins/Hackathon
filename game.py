import pygame
import numpy

WIDTH = 512
HEIGHT = 512
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
        self.startx = startx
        self.starty = starty

        self.speed = 4
        self.jump_speed = 20
        self.animation_index = 0
        self.facing_left = False
        self.vsp = 0
        self.gravity = 1

        self.collision_scale = 0.5

        self.load_sprites()

    def load_sprites(self):
        self.idle = load_sprite_sheet("Assets/Pixel Adventure 1/Free/Main Characters/Pink Man/Idle (32x32).png", 11)
        self.run = load_sprite_sheet("Assets/Pixel Adventure 1/Free/Main Characters/Pink Man/Run (32x32).png", 12)
        self.jump_image = pygame.image.load("Assets/Pixel Adventure 1/Free/Main Characters/Pink Man/Jump (32x32).png")

    def get_collision(self, x, y, blocks):
        self.rect.move_ip([x,y])
        collide = pygame.sprite.spritecollideany(self, blocks)
        self.rect.move_ip([-x,-y])
        return collide

    def check_collision(self, x, y, spikes, goal):
        self.rect.move_ip([x,y])
        if pygame.sprite.spritecollideany(self, spikes):
            self.rect.move_ip([-x,-y])
            return 'S'
        elif pygame.sprite.spritecollideany(self, goal):
            self.rect.move_ip([-x,-y])
            return 'G'
        else:
            self.rect.move_ip([-x,-y])
            return ' '

    def reset(self):
        self.rect.x = self.startx-16
        self.rect.y = self.starty-16
        self.vsp = 0
        self.hsp = 0
    
    def move(self, x, y, blocks, spikes, goal):
        dx = x
        dy = y

        # Check for victory or spike first
        if self.check_collision(dx, dy, spikes, goal) == 'S':
            # back to start
            self.reset()
        
        elif self.check_collision(dx, dy, spikes, goal) == 'G':
            NEW_LEVEL = True

        if dy < 0:
            while self.get_collision(0, dy, blocks):
                dy += 1
                self.vsp = 0
        else:
            while self.get_collision(0, dy, blocks):
                dy -= 1
        while self.get_collision(dx, dy, blocks):
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

    def update(self, blocks, spikes, goal):
        self.hsp = 0
        onground = self.get_collision(0, 1, blocks)

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
        self.move(self.hsp, self.vsp, blocks, spikes, goal)

class Block(Sprite):
    def __init__(self, sprite, startx, starty):
        super().__init__(sprite, startx, starty)

class Spike(Sprite):
    def __init__(self, sprite, startx, starty):
        super().__init__(sprite, startx, starty)
        

def load_sprite_sheet(filename, n):
    sheet = pygame.image.load(filename).convert_alpha()
    anim = []
    for i in range(n):
        img = pygame.Surface((32,32), pygame.SRCALPHA).convert_alpha()
        img.blit(sheet, (0,0), (i*32, 0, 32, 32))
        anim.append(img)
    return anim

def load_2D_spritesheet(filename, n, m):
    sheet = pygame.image.load(filename).convert_alpha()
    sprites = [[0] * m for _ in range(n)]
    for j in range(m):
        for i in range(n):
            img = pygame.Surface((16,16), pygame.SRCALPHA).convert_alpha()
            img.blit(sheet, (0,0), (j*16, i*16, 16, 16))
            sprites[i][j] = img
    return sprites

def double_size(img):
    bigger_img = pygame.transform.scale(img, (32,32))
    return bigger_img

tilemap = {}
def load_tiles():
    tiles = load_2D_spritesheet("Assets/Pixel Adventure 1/Free/Terrain/Terrain (16x16).png", 11, 22)
    tilemap["grass_1"] = double_size(tiles[0][6])
    tilemap["grass_2"] = double_size(tiles[0][7])
    tilemap["grass_3"] = double_size(tiles[0][8])
    tilemap["grass_4"] = double_size(tiles[1][6])
    tilemap["grass_5"] = double_size(tiles[1][7])
    tilemap["grass_6"] = double_size(tiles[1][8])
    tilemap["grass_7"] = double_size(tiles[2][6])
    tilemap["grass_8"] = double_size(tiles[2][7])
    tilemap["grass_9"] = double_size(tiles[2][8])
    tilemap["background"] = pygame.image.load("Assets/Pixel Adventure 1/Free/Background/Brown.png")
    tilemap["spike"] = double_size(pygame.image.load("Assets/Pixel Adventure 1/Free/Traps/Spiked Ball/Spiked Ball.png"))
    tilemap["end"] = pygame.transform.scale(pygame.image.load("Assets/Pixel Adventure 1/Free/Items/Checkpoints/End/End (Idle).png"),(32,32))


#def choose_tile(x,y):

class Level:
    def __init__(self, block_map):
        self.block_map = block_map
        self.end_sprite = None

        for row in range(len(block_map)):
            for col in range(len(block_map[0])):
                if block_map[row][col] == 'S':
                    self.start = (col*32, row*32)
                if block_map[row][col] == 'E':
                    self.end = (col*32+16, row*32+16)

    def draw(self, blocks, spikes, goal):
        for row in range(len(self.block_map)):
            for col in range(len(self.block_map[0])):
                if self.block_map[row][col] == ' ' or self.block_map[row][col] == 'S':
                    continue
                elif self.block_map[row][col] == 'H':
                    spikes.add(Spike(tilemap["spike"], col*32+16, row*32+16))
                    continue
                elif self.block_map[row][col] == 'E':
                    self.end_sprite = goal.add(Sprite(tilemap["end"], col*32+16, row*32+16))
                    continue
                else:
                    name = "grass_2"
                    if not (row == 0):
                        if self.block_map[row-1][col] == '#':
                            name = "grass_5"
                    blocks.add(Block(tilemap[name], col*32+16, row*32+16))

def load_level(filename):
    #open and read the file after the overwriting:
    f = open(filename, "r")
    level=[]
    for i in range(16):
        line = f.readline()
        row=[]
        for c in line:
            row.append(c)
        level.append(row)
    f.close()
    return level

# flag
NEW_LEVEL = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    blocks = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    goal = pygame.sprite.Group()
    background = pygame.sprite.Group()
    load_tiles()
    level = Level(load_level("levels_10.txt"))
    player = Player(level.start[0]+16, level.start[1]+16)
    level.draw(blocks, spikes, goal)

    # for blk in range(8, WIDTH, 16):
    #     blocks.add(Block(tilemap["grass_2"], blk, HEIGHT-8))

    for x in range(32, WIDTH+64, 64):
        for y in range(32, HEIGHT+64, 64):
            background.add(Sprite(tilemap["background"], x, HEIGHT-16-y))

    while True:
        pygame.event.pump()
        player.update(blocks, spikes, goal)

        if NEW_LEVEL:
            blocks = pygame.sprite.Group()
            spikes = pygame.sprite.Group()
            goal = pygame.sprite.Group()
            load_tiles()
            # HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
            level = Level("HEREEEE")
            player = Player(level.start[0]+16, level.start[1]+16)
            level.draw(blocks, spikes, goal)

        # Draw loop
        screen.fill(BACKGROUND)

        background.draw(screen)
        player.draw(screen)
        blocks.draw(screen)
        spikes.draw(screen)
        goal.draw(screen)
        pygame.display.flip()

        clock.tick(50)



if __name__ == "__main__":
    main()