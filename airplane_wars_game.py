import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("飞机大战")

# 设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
score = 0
font = pygame.font.Font(None, 36)  # 创建字体对象
vanished_enemies = 0
max_vanished_enemies = 10

# 飞机类
class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        #if keys[pygame.K_UP] and self.rect.top > 0:
        #    self.rect.y -= self.speed
        #if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
        #    self.rect.y += self.speed
        
        # 检查飞机是否撞到敌人
        if pygame.sprite.spritecollide(self, enemies, False):
            self.kill()  # 撞到敌人后销毁飞机
            running = False  # 游戏结束


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), -50))
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# 初始化游戏
plane = Plane()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(plane)

# 游戏循环
clock = pygame.time.Clock()
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 按下空格键发射子弹
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bullet = Bullet(plane.rect.centerx, plane.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)

    # 更新所有精灵
    all_sprites.update()

    # 创建敌人
    if random.random() < 0.01:
        enemy = Enemy()
        enemies.add(enemy)
        all_sprites.add(enemy)

    # 碰撞检测
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    
    for hit in hits:
        # 在这里可以添加敌机被击中的效果或得分逻辑
        score+=100
    
    for enemy in enemies:
        if enemy.rect.top > HEIGHT:
            enemy.kill()
            vanished_enemies += 1  # 增加消失的敌人数量

    # 检查游戏是否结束
    if not plane.alive() or vanished_enemies >= max_vanished_enemies:
        running = False  # 游戏结束
        

    # 绘制背景和精灵
    # 在游戏循环中添加得分显示
    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.fill(BLACK)
    all_sprites.draw(SCREEN)
    SCREEN.blit(score_text, (10, 10))
    
    
    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(30)

game_over_text = font.render("Game Over", True, WHITE)
SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
pygame.display.flip()
# 等待几秒钟后退出游戏
pygame.time.wait(300)
# 退出游戏
pygame.quit()

