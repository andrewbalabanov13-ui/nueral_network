from doctest import FAIL_FAST
import time
import pygame
import random


pygame.init()
WIDTH = 640
HEIGHT = 480
FONT_SIZE_36 = pygame.font.SysFont('Arial', 36)
FONT_SIZE_15 = pygame.font.SysFont('Arial', 15)
AMOUNT_ENEMY = 50
COIN_AMOUNT = 2
PLAYER_AMOUNT = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (153, 0, 255) 
WHITE = (255,255,255)
BLACK = (0,0,0)

class Enemy():
    def __init__(self,enemy_pos,direction) -> None:
        self.pos = enemy_pos
        self.direction = direction

    def draw(self,all_size):
        pygame.draw.rect(screen,RED,(self.pos.x - all_size / 2,self.pos.y - all_size / 2,all_size,all_size))

class Player():
    def __init__(self,player_pos,direction) -> None:
        self.pos = player_pos
        self.direction = direction

    def draw(self,all_size):
        pygame.draw.rect(screen,GREEN,(self.pos.x - all_size / 2,self.pos.y - all_size / 2,all_size,all_size))


class Coin():
    def __init__(self,coin_pos) -> None:
        self.pos = coin_pos

    def draw(self,all_size):
        pygame.draw.rect(screen,YELLOW,(self.pos.x - all_size / 2,self.pos.y - all_size / 2,all_size,all_size))


def _rect_at_center(center: pygame.Vector2, size: float) -> pygame.Rect:
    half = size / 2
    return pygame.Rect(center.x - half, center.y - half, size, size)

def _overlap(center_a: pygame.Vector2, center_b: pygame.Vector2, size: float) -> bool:
    """True if two same-sized axis-aligned squares (center + half-extent) intersect."""
    return _rect_at_center(center_a, size).colliderect(_rect_at_center(center_b, size))

def get_coin_pos_at_setup(player_list,half,all_size):
    coin = Coin(pygame.Vector2((random.randint(half, WIDTH - half), random.randint(half, HEIGHT - half))))
    while True:
        should_break = True
        for player in player_list:
            if _overlap(coin.pos, player.pos, all_size):
                should_break = False
                break
        if should_break:
            return coin

def get_enemy_pos_at_setup(player_list,half,all_size):
    enemy = Enemy(
        pygame.Vector2((random.randint(half, WIDTH - half), random.randint(half, HEIGHT - half))),
        pygame.Vector2(random.randint(-1,1),random.randint(-1,1)))
    while True:
        should_break = True
        for player in player_list:
            if _overlap(enemy.pos, player.pos, all_size):
                should_break = False
                break
        if should_break:
            return enemy


def setup():
    enemy_list = []
    coin_list = []
    all_size = 10
    half = int(all_size / 2)
    player_list = []
    # pygame.Vector2(all_size / 2, half)
    for x in range(PLAYER_AMOUNT):
        player_list.append(Player(pygame.Vector2(all_size / 2, half),-1))
    
    for x in range(COIN_AMOUNT):
        coin_list.append(get_coin_pos_at_setup(player_list,half,all_size))

    for x in range(AMOUNT_ENEMY):
        enemy_list.append(get_enemy_pos_at_setup(player_list,half,all_size))

    return (all_size, player_list, enemy_list, coin_list)

def move_enemy(direction,enemy_pos,speed, all_size):
    dx = 0
    dy = 0
    if direction.x == 1:
        #right
        dx += speed
    if direction.x == -1:
        #left
        dx -= speed
    if direction.y == 1:
        #up
        dy -= speed
    if direction.x == -1:
        #down
        dy += speed
    enemy_pos.x += dx
    enemy_pos.y += dy
    if is_colliding_with_border(enemy_pos,all_size):
        enemy_pos.x -= dx
        enemy_pos.y -= dy
        direction = pygame.Vector2(random.randint(-1,1),random.randint(-1,1))
        return direction
    return direction

def move_player(direction, player_pos, speed, all_size):
    dx = 0
    dy = 0
    if direction.x == 1:
        #right
        dx += speed
    if direction.x == -1:
        #left
        dx -= speed
    if direction.y == 1:
        #up
        dy -= speed
    if direction.y == -1:
        #down
        dy += speed
    player_pos.x += dx
    player_pos.y += dy
    if is_colliding_with_border(player_pos,all_size):
        player_pos.x -= dx
        player_pos.y -= dy

def is_colliding_with_border(pos, size):
    if pos.x - size / 2 < 0:
        return True
    if pos.x + size / 2 > WIDTH:
        return True
    if pos.y - size / 2 < 0:
        return True
    if pos.y + size / 2 > HEIGHT:
        return True
    return False

def get_player_arrow_keys_input():
    direction = pygame.Vector2(0,0)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        direction.x = 1
    if keys[pygame.K_LEFT]:
        direction.x = -1
    if keys[pygame.K_UP]:
        direction.y = 1
    if keys[pygame.K_DOWN]:
        direction.y = -1
    return direction

def play():
    running_after_death = False
    coins_collected = 0
    enemy_dir = pygame.Vector2(0,0)
    running = True
    all_size, player_list, enemy_list, coin_list = setup()
    while running:
        screen.fill(WHITE)
        speed = 1
        player_input = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #moving player
        direction = get_player_arrow_keys_input()
        for player in player_list:
            move_player(direction,player.pos,speed, all_size)
        #moving enemy
        for enemy in enemy_list:
            if random.randint(1,75) == 1:
                enemy.direction = pygame.Vector2(random.randint(-1,1),random.randint(-1,1))
            enemy.direction = move_enemy(enemy.direction,enemy.pos,speed,all_size)
        #drawing evrething
        for player in player_list:
            player.draw(all_size)
        for enemy in enemy_list:
            enemy.draw(all_size)
        for coin in coin_list:
            coin.draw(all_size)
        

        for player in player_list:
            for enemy in enemy_list:
                if _overlap(player.pos, enemy.pos, all_size):
                    running = False
                    text_surface = FONT_SIZE_36.render('You Lost!', True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(text_surface, text_rect)
                    running_after_death = True

            for coin in coin_list:
                if _overlap(player.pos, coin.pos, all_size):
                    coin_list.remove(coin)
                    coins_collected += 1
                    if coins_collected == COIN_AMOUNT:
                        running = False
                        text_surface = FONT_SIZE_36.render('You Win!', True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(text_surface, text_rect)
                        running_after_death = True
        
        text_surface = FONT_SIZE_15.render(f"Your score: {coins_collected}", True, BLACK)
        text_rect = text_surface.get_rect(center=(45,10))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(60)

        
    while running_after_death:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_after_death = False
        clock.tick(60)

play()