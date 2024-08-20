import pygame
import random

# Инициализация Pygame
pygame.init()

# Задание параметров окна игры
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Rex")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройка спрайтов
DINO_WIDTH, DINO_HEIGHT = 50, 50
DINO_COLOR = (0, 255, 0)
GROUND_HEIGHT = HEIGHT - 70
GRAVITY = 1

# Настройка препятствий
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 50
OBSTACLE_COLOR = (255, 0, 0)
OBSTACLE_VELOCITY = 10

# Создание класса Dino
class Dino:
    def __init__(self):
        self.x = 50
        self.y = GROUND_HEIGHT - DINO_HEIGHT
        self.width = DINO_WIDTH
        self.height = DINO_HEIGHT
        self.is_jumping = False
        self.jump_vel = 15
        self.fall_vel = 0
    
    def draw(self):
        pygame.draw.rect(WIN, DINO_COLOR, (self.x, self.y, self.width, self.height))
    
    def jump(self):
        if self.is_jumping:
            self.fall_vel -= GRAVITY
            self.y -= self.jump_vel + self.fall_vel
            if self.y >= GROUND_HEIGHT - self.height:
                self.y = GROUND_HEIGHT - self.height
                self.is_jumping = False
                self.fall_vel = 0

# Создание класса препятствия
class Obstacle:
    def __init__(self):
        self.x = WIDTH
        self.y = GROUND_HEIGHT - OBSTACLE_HEIGHT
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT
    
    def draw(self):
        pygame.draw.rect(WIN, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self):
        self.x -= OBSTACLE_VELOCITY
        if self.x < -self.width:
            self.x = WIDTH + random.randint(200, 400)

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    run = True
    dino = Dino()
    obstacle = Obstacle()
    score = 0
    
    while run:
        clock.tick(30)
        WIN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dino.is_jumping:
                    dino.is_jumping = True
                    dino.fall_vel = dino.jump_vel
        
        # Движение и отрисовка персонажа
        dino.jump()
        dino.draw()
        
        # Движение и отрисовка препятствия
        obstacle.move()
        obstacle.draw()
        
        # Проверка столкновения
        if dino.x + dino.width > obstacle.x and dino.x < obstacle.x + obstacle.width:
            if dino.y + dino.height > obstacle.y:
                run = False
        
        # Подсчет очков
        if obstacle.x + obstacle.width < dino.x and not dino.is_jumping:
            score += 1
        
        # Отображение счета
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        WIN.blit(text, (10, 10))
        
        # Обновление экрана
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
