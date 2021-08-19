import pygame
from sys import exit
from random import randint

pygame.init()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = large_font.render(f'score: {current_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH/2, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 

            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)
        
        obstacle_rect = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

""" SETUP """
# screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 400)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_version = '0.0.1'  # current version of the game (major update, minor update, path/fixes)

# window title setup
WINDOW_TITLE = 'build : v' + game_version
pygame.display.set_caption(WINDOW_TITLE)

# fps setup
FPS = 60
clock = pygame.time.Clock()

""" VARIABLES """
game_active = False
start_time = 0
score = 0 

large_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
small_font = pygame.font.Font('fonts/Pixeltype.ttf', 20)

ground_surf = pygame.image.load('graphics/Ground.png').convert()

# score_surf = pixel_font.render('SCORE', False, (255, 255, 255))
# score_rect = score_surf.get_rect(center=(SCREEN_WIDTH / 2, 50))

# obstacles
snail_surf = pygame.image.load('graphics/turtle/turtle.png').convert_alpha()
fly_surf = pygame.image.load('graphics/fly/fly.png').convert_alpha()

obstacle_rect_list = []

# how to jump text
x_jump_text = small_font.render('press "X" to jump', False, (255, 255, 255))
x_jump_text_rect = x_jump_text.get_rect(center= (60, 15))

# player
player_surf = pygame.image.load('graphics/player/player.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0
gravity_pull = 0.9
jump_speed = -15

# intro screen
player_scale = 2
player_stand = pygame.image.load('graphics/player/player.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand, (45*player_scale, 75*player_scale))
player_stand_rect = player_stand.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

game_name = large_font.render('[  JUMP  ]', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH/2, 50))
restart_text = large_font.render('press "Z" to start', False, (255, 255, 255))
restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-50))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

""" GAME LOOP """
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # player input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = jump_speed

            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                if player_rect.bottom >= 160:
                    player_gravity = jump_speed
        
        else: # if game !active
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                game_active = True
                start_time = 0
                start_time = int(pygame.time.get_ticks() / 1000) - start_time
        
        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
            else: 
                obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 215)))

    if game_active: # game
        # background
        # screen.blit(sky_surf, (0, 0))
        screen.fill('#181425')
        screen.blit(ground_surf, (0, 300))

        # snail
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)

        # player
        player_gravity += gravity_pull
        player_rect.y += player_gravity

        if player_rect.bottom >= 300: player_rect.bottom = 300

        screen.blit(player_surf, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        game_active = collisions(player_rect, obstacle_rect_list)

        # HUD
        score = display_score()
        screen.blit(x_jump_text, x_jump_text_rect)
    else: # intro/game over screen
        # background
        screen.fill('#181425')
        # screen.blit(sky_surf, (0, 0))

        # clear all enemies / reset players position when game is over
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 100)
        player_gravity = 0
 
        # score / HUD
        score_display = large_font.render(f'score: {score}', False, (255, 255, 255))
        score_display_rect = score_display.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-50))
        if score == 0:
            screen.blit(restart_text, restart_text_rect)
        else:
            screen.blit(score_display, score_display_rect)

        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand, player_stand_rect)
        


    pygame.display.update()
    clock.tick(FPS)
