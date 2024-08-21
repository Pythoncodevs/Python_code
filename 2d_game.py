import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter with Bosses")

MAP_WIDTH, MAP_HEIGHT = 1600, 1200

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

player_size = 50
player_x = MAP_WIDTH // 2
player_y = MAP_HEIGHT // 2
player_speed = 5
ammo = 100  
max_ammo = 100  
reload_time = 120  
reload_timer = 0
reloading = False
shooting = False


bullet_speed = 15
bullets = []


zombie_size = 50
zombies = []
zombie_spawn_rate = 30
zombie_speed = 1
zombie_increase_rate = 0.05
zombie_spawn_distance = 300
zombie_health = 1


boss_size = 100
bosses = []
boss_health = 50
kills_for_boss = 5
boss_spawned = False


obstacles = [
    pygame.Rect(300, 300, 200, 100),
    pygame.Rect(700, 800, 300, 50),
    pygame.Rect(1100, 500, 100, 300),
    pygame.Rect(500, 1100, 150, 150),
]

clock = pygame.time.Clock()
run = True
score = 0
kills = 0

while run:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ammo > 0 and not shooting and not reloading:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - HEIGHT // 2, mouse_x - WIDTH // 2)
                bullets.append({
                    "x": player_x + player_size // 2,
                    "y": player_y + player_size // 2,
                    "angle": angle
                })
                ammo -= 1
                shooting = True
            if event.key == pygame.K_1 and not reloading:
                reloading = True
                reload_timer = reload_time
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shooting = False

    if reloading:
        reload_timer -= 1
        if reload_timer <= 0:
            ammo = max_ammo
            reloading = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x - player_speed > 0:
        player_x -= player_speed
    if keys[pygame.K_d] and player_x + player_speed + player_size < MAP_WIDTH:
        player_x += player_speed
    if keys[pygame.K_w] and player_y - player_speed > 0:
        player_y -= player_speed
    if keys[pygame.K_s] and player_y + player_speed + player_size < MAP_HEIGHT:
        player_y += player_speed

    for bullet in bullets[:]:
        bullet["x"] += bullet_speed * math.cos(bullet["angle"])
        bullet["y"] += bullet_speed * math.sin(bullet["angle"])
        if bullet["x"] < 0 or bullet["x"] > MAP_WIDTH or bullet["y"] < 0 or bullet["y"] > MAP_HEIGHT:
            bullets.remove(bullet)

    if random.randint(1, zombie_spawn_rate) == 1 and len(zombies) < 10:
        while True:
            x = random.randint(0, MAP_WIDTH)
            y = random.randint(0, MAP_HEIGHT)
            if abs(x - player_x) > zombie_spawn_distance and abs(y - player_y) > zombie_spawn_distance:
                zombies.append({
                    "rect": pygame.Rect(x, y, zombie_size, zombie_size),
                    "hp": zombie_health
                })
                break

    for zombie in zombies[:]:
        angle = math.atan2(player_y - zombie["rect"].y, player_x - zombie["rect"].x)
        zombie["rect"].x += zombie_speed * math.cos(angle)
        zombie["rect"].y += zombie_speed * math.sin(angle)
        
        if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(zombie["rect"]):
            run = False

        for bullet in bullets[:]:
            if zombie["rect"].collidepoint(bullet["x"], bullet["y"]):
                zombie["hp"] -= 1
                bullets.remove(bullet)
                if zombie["hp"] <= 0:
                    zombies.remove(zombie)
                    score += 10
                    kills += 1
                break

    if kills >= kills_for_boss and not boss_spawned:
        boss_spawned = True
        boss_x = random.randint(0, MAP_WIDTH)
        boss_y = random.randint(0, MAP_HEIGHT)
        bosses.append({"rect": pygame.Rect(boss_x, boss_y, boss_size, boss_size), "hp": boss_health})

    for boss in bosses[:]:
        angle = math.atan2(player_y - boss["rect"].y, player_x - boss["rect"].x)
        boss["rect"].x += zombie_speed * math.cos(angle)
        boss["rect"].y += zombie_speed * math.sin(angle)

        if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(boss["rect"]):
            run = False

        for bullet in bullets[:]:
            if boss["rect"].collidepoint(bullet["x"], bullet["y"]):
                boss["hp"] -= 1
                bullets.remove(bullet)
                if boss["hp"] <= 0:
                    bosses.remove(boss)
                    score += 50
                    kills = 0
                    boss_spawned = False
                break


    zombie_speed += zombie_increase_rate / 1000

    win.fill(BLACK)
    offset_x = player_x - WIDTH // 2
    offset_y = player_y - HEIGHT // 2

    pygame.draw.rect(win, GREEN, (WIDTH // 2, HEIGHT // 2, player_size, player_size))

    for bullet in bullets:
        pygame.draw.circle(win, WHITE, (int(bullet["x"]) - offset_x, int(bullet["y"]) - offset_y), 5)

    for zombie in zombies:
        pygame.draw.rect(win, RED, (zombie["rect"].x - offset_x, zombie["rect"].y - offset_y, zombie_size, zombie_size))
        health_bar_length = zombie_size
        health_bar_height = 5
        health_ratio = zombie["hp"] / zombie_health
        pygame.draw.rect(win, RED, (zombie["rect"].x - offset_x, zombie["rect"].y - offset_y - 10, health_bar_length, health_bar_height))
        pygame.draw.rect(win, GREEN, (zombie["rect"].x - offset_x, zombie["rect"].y - offset_y - 10, health_bar_length * health_ratio, health_bar_height))

    for boss in bosses:
        pygame.draw.rect(win, YELLOW, (boss["rect"].x - offset_x, boss["rect"].y - offset_y, boss_size, boss_size))
        health_bar_length = boss_size
        health_bar_height = 10
        health_ratio = boss["hp"] / boss_health
        pygame.draw.rect(win, RED, (boss["rect"].x - offset_x, boss["rect"].y - offset_y - 10, health_bar_length, health_bar_height))
        pygame.draw.rect(win, GREEN, (boss["rect"].x - offset_x, boss["rect"].y - offset_y - 10, health_bar_length * health_ratio, health_bar_height))

    for obstacle in obstacles:
        pygame.draw.rect(win, GRAY, (obstacle.x - offset_x, obstacle.y - offset_y, obstacle.width, obstacle.height))

    font = pygame.font.SysFont("comicsans", 30)
    score_text = font.render(f"Score: {score}", 1, WHITE)
    ammo_text = font.render(f"Ammo: {ammo}", 1, WHITE)
    win.blit(score_text, (10, 10))
    win.blit(ammo_text, (10, 40))
    
    pygame.display.update()

pygame.quit()
 