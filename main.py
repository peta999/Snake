# Example file showing a circle moving on screen
import copy
import random

import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DIRECTIONS = ["up", "down", "left", "right"]




def main():
    # pygame setup
    pygame.init()
    MOVEEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVEEVENT, 500)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    circle_radius = 20

    trail = []
    trail.append(pygame.Vector2(440, 400))
    head_direction = "left"
    last_pressed = "left"

    player_pos = pygame.Vector2(400, 400)

    food_pos = addFood(player_pos, trail)
    increase_length = False

    drawGrid(screen, pygame.Color("white"))

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOVEEVENT:
                head_direction = turn(head_direction, last_pressed)
                player_pos = move(player_pos, head_direction, trail, increase_length)
                increase_length = False
                if collision_wall(player_pos) == False:
                    running = False
                if trail_collision(player_pos, trail):
                    running = False
                if food_collision(player_pos, food_pos):
                    food_pos = addFood(player_pos, trail)
                    increase_length = True


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("gray")

        pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(player_pos.x, player_pos.y, 40, 40))
        print(len(trail))
        for item in trail:
            print(item.x, item.y)
            pygame.draw.rect(screen, pygame.Color("red"), pygame.Rect(item.x, item.y, 40, 40))

        pygame.draw.rect(screen, pygame.Color("green"), pygame.Rect(food_pos.x, food_pos.y, 40, 40))

        drawGrid(screen, pygame.Color("white"))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            last_pressed = "up"
        if keys[pygame.K_s]:
            last_pressed = "down"
        if keys[pygame.K_a]:
            last_pressed = "left"
        if keys[pygame.K_d]:
            last_pressed = "right"



        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        clock.tick_busy_loop(60)
    pygame.quit()

def turn(head_direction, direction):
    if head_direction != direction:
        if direction == "up":
            if head_direction == "left":
                head_direction = "up"
            elif head_direction == "right":
                head_direction = "up"
        elif direction == "down":
            if head_direction == "left":
                head_direction = "down"
            elif head_direction == "right":
                head_direction = "down"
        elif direction == "left":
            if head_direction == "up":
                head_direction = "left"
            elif head_direction == "down":
                head_direction = "left"
        elif direction == "right":
            if head_direction == "up":
                head_direction = "right"
            elif head_direction == "down":
                head_direction = "right"

    return head_direction

def move(player_pos, head_direction, trail, increase_length):

    if not increase_length:
        t1 = trail[0]
        temp_pos = pygame.Vector2(t1.x, t1.y)
        t1.x = copy.copy(player_pos.x)
        t1.y = copy.copy(player_pos.y)
        for item in trail[1:]:
            t2 = copy.copy(item)
            item.x = copy.copy(temp_pos.x)
            item.y = copy.copy(temp_pos.y)
            temp_pos.x = t2.x
            temp_pos.y = t2.y
    else:
        trail.insert(0, pygame.Vector2(copy.copy(player_pos.x), copy.copy(player_pos.y)))


    if head_direction == "up":
        player_pos.y -= 40
    elif head_direction == "down":
        player_pos.y += 40
    elif head_direction == "left":
        player_pos.x -= 40
    elif head_direction == "right":
        player_pos.x += 40
    return snapToGrid(player_pos)

def collision_wall(pos):
    if pos.x < 0:
        return False
    elif pos.x > WINDOW_WIDTH:
        return False
    elif pos.y < 0:
        return False
    elif pos.y > WINDOW_HEIGHT:
        return False



def snapToGrid(pos):
    blockSize = 40 #Set the size of the grid block
    x = (pos.x - pos.x % blockSize)
    y = (pos.y - pos.y % blockSize)
    return pygame.Vector2(x, y)

def drawGrid(screen, color):
    blockSize = 40 #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, color, rect, 1)

def addFood(player_pos, trail):
    # place food on a random spot on the grid that is not occupied by the snake
    while True:
        randomX, randomY = randomCoords20()
        if randomX == player_pos.x and randomY == player_pos.y:
            continue
        for item in trail:
            if randomX == item.x and randomY == item.y:
                continue
        break


    return pygame.Vector2(randomX, randomY)

def randomCoords20():
    randomX = random.randint(0, WINDOW_WIDTH / 40) * 40
    randomY = random.randint(0, WINDOW_HEIGHT / 40) * 40
    return randomX, randomY

def food_collision(player_pos, food_pos):
    if player_pos.x == food_pos.x and player_pos.y == food_pos.y:
        return True
    else:
        return False


def trail_collision(player_pos, trail):
    for item in trail:
        if player_pos.x == item.x and player_pos.y == item.y:
            return True
    return False


if __name__ == "__main__":
    main()



