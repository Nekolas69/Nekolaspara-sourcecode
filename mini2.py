import pygame
import random
import time
pygame.init()
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
player_width = 75
player_height = 75
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 1
player_y_change = 0
player_vertical_speed = 2
obstacle_width = 100
obstacle_height = 100
obstacle_speed = 1
obstacle_list = []
collectible_width = 50
collectible_height = 75
collectibles = []
collectibles_spawn_intervals = [30000]  
last_collectible_spawn_times = [0] * len(collectibles_spawn_intervals)
collectible_sound = pygame.mixer.Sound("košíkus/collectible_sound.mp3")
collision_sound = pygame.mixer.Sound("košíkus/collision_sound.mp3")
collectible_img = pygame.Surface((collectible_width, collectible_height))
collectible_img.fill((0, 0, 255))  
color = (9, 255, 0)
RED=(255,0,0)
font = pygame.font.Font(None, 50)
background = pygame.image.load("košíkus/background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))
player_img = pygame.image.load("košíkus/player.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))
obstacle_img = pygame.image.load("košíkus/koska.png")
obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_width, obstacle_height))
collectible_img = pygame.image.load("košíkus/collectible.png")
collectible_img = pygame.transform.scale(collectible_img, (collectible_width, collectible_height))
clock = pygame.time.Clock()
def draw_player(x, y):
    screen.blit(player_img, (x, y))
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle[0], obstacle[1]))
def display_countdown(countdown_time):
    text = f"Zbyvající čas: {countdown_time}"
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (500, screen_height - 1000))
def check_collision(player_x, player_y, obstacle):
    if (player_x < obstacle[0] + obstacle[2] and
        player_x + player_width > obstacle[0] and
        player_y < obstacle[1] + obstacle[3] and
        player_y + player_height > obstacle[1]):
        return True
    return False
def draw_collectibles(collectibles):
    for collectible in collectibles:
        screen.blit(collectible_img, (collectible[0], collectible[1]))
def restart_game():
    global player_x, player_y, obstacle_list, obstacle_speed, game_over, player_y_change, collectibles,player_speed,player_vertical_speed
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 10
    obstacle_list = []
    obstacle_speed = 1
    game_over = False
    player_y_change = 0
    countdown_start = pygame.time.get_ticks()
    collectibles = []
    player_speed = 1
    player_y_change = 0
    player_vertical_speed = 2
def kosikhra():
    global player_x, player_y, obstacle_list, obstacle_speed, game_over, player_y_change,player_vertical_speed,player_speed
    game_over = False
    countdown_start = pygame.time.get_ticks() 
    countdown_duration = 180 * 1000  
    obstacle_spawn_interval = 2000  
    last_spawn_time = 0
    collected_collectibles = 0
    pygame.mixer.music.load("košíkus/hudba.mp3")  
    pygame.mixer.music.set_volume(0.5)  
    pygame.mixer.music.play(-1)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_y_change = -player_vertical_speed
                if event.key == pygame.K_DOWN:
                    player_y_change = player_vertical_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_y_change = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            if player_x < 0:  
                player_x = 0
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            if player_x > screen_width - player_width: 
                player_x = screen_width - player_width
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        player_y += player_y_change
        if player_y < 0:
            player_y = 0
        if player_y > screen_height - player_height:
            player_y = screen_height - player_height
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - countdown_start
        remaining_time = max((countdown_duration - elapsed_time) // 1000, 0)
        obstacle_speed = 1 + (3 - remaining_time / 40)  
        obstacle_speed = max(obstacle_speed, 1) 
        obstacle_spawn_interval = (75+(remaining_time*10))
        if current_time - last_spawn_time >= obstacle_spawn_interval:
            obstacle_x = random.randint(0, screen_width - obstacle_width)
            obstacle_list.append([obstacle_x, 0, obstacle_width, obstacle_height])
            last_spawn_time = current_time
        for obstacle in obstacle_list:
            obstacle[1] += obstacle_speed
            if obstacle[1] > screen_height:
                obstacle_list.remove(obstacle)
        for obstacle in obstacle_list:
            if check_collision(player_x, player_y, obstacle):
                collision_sound.play()
                time.sleep(3)
                restart_game()
                kosikhra()
        for i in range(len(collectibles_spawn_intervals)):
                if current_time - last_collectible_spawn_times[i] >= collectibles_spawn_intervals[i]:
                    collectible_x = random.randint(0, screen_width - collectible_width)
                    collectible_y = random.randint(0, screen_height - collectible_height)
                    collectibles.append([collectible_x, collectible_y])
                    last_collectible_spawn_times[i] = current_time
        for collectible in collectibles:
            if (player_x < collectible[0] + collectible_width and
                player_x + player_width > collectible[0] and
                player_y < collectible[1] + collectible_height and
                player_y + player_height > collectible[1]):
                collectibles.remove(collectible)
                collectible_sound.play()
                player_speed +=1
                player_vertical_speed +=1
                collected_collectibles += 1
        screen.blit(background, (0, 0))
        draw_player(player_x, player_y)
        draw_obstacles(obstacle_list)
        display_countdown(remaining_time)
        draw_collectibles(collectibles)
        collected_text = f"Piwka: {collected_collectibles}"
        collected_text_surface = font.render(collected_text, True, RED)
        screen.blit(collected_text_surface, (1300, screen_height - 1000))
        if collected_collectibles >= 5 and remaining_time == 0:
            game_over = True
            break
        elif remaining_time == 0:
            restart_game()
            kosikhra()
        pygame.display.update()
        clock.tick(60)
if __name__ == "__main__":
    kosikhra()
