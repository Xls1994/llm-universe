import pygame
import time
import random

pygame.init()

# 定义颜色
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 初始化游戏窗口
dis_width = 600
dis_height  = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('贪吃蛇')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

# 获取默认字体路径
#default_font_path = pygame.font.get_default_font()
#font_style = pygame.font.Font(default_font_path, 50)
#score_font = pygame.font.Font(default_font_path, 35)

font_style = pygame.font.SysFont("songti", 35)
score_font = pygame.font.SysFont("songti", 35)
score = 0

def your_score(score):
    value = score_font.render("得分: " + str(score), True, yellow)
    dis.blit(value,[0,0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False
    global score
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0       
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("你输了! 按Q退出或者C重新开始", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.circle(dis, yellow, (int(foodx + snake_block / 2), int(foody + snake_block / 2)), int(snake_block / 2))
        #pygame.draw.circle(dis, yellow, [foodx, foody, snake_block, snake_block])
        your_score(score)
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score+=1
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()

