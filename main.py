import pygame as pg
import random, time
import asyncio
pg.init()
clock = pg.time.Clock()

black = (0, 0, 0)
win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Fish')

font = pg.font.Font(None, 30)
speed = 7
score = 0
running = True
waiting = False

player_size = 40
player_pos = [win_width / 2, win_height - player_size]
player_image = pg.image.load('./assets/images/betta-removebg-preview.png')
player_image = pg.transform.scale(player_image, (player_size, player_size))

obj_size = 20
obj_data = []
obj = pg.image.load('./assets/images/food.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))

bg_image = pg.image.load('./assets/images/fishtank.png')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))


def create_object(obj_data):
    if len(obj_data) < 1 and random.random() < 0.1:            
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])




def update_objects(obj_data):
    global score

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            score -= 1


def collision_check(obj_data, player_pos):
    global running, score
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            score += 1
            obj_data.remove(object)

def restart_game():
    global score,obj_data
    score = 0
    obj_data = [] 

async def main():
    global running, player_pos

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_LEFT:
                    x -= 50
                elif event.key == pg.K_RIGHT:
                    x += 50
                player_pos = [x, y]

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Mood: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)

        if score == 15:
            game_over_text = font.render("Game Over. Your fish went hyper. Please press key R to restart",True,black)
            screen.blit(game_over_text,(win_width - 700, win_height - 80))
            pg.display.flip()
            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        running = False
                    if event.type == pg.KEYDOWN and event.key == pg.K_r:
                        waiting = False
                        restart_game()
            
        clock.tick(30)
        pg.display.flip()
        await asyncio.sleep(0)

    pg.quit()

asyncio.run(main())