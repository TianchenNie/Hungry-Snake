import pygame
from pygame.math import Vector2
import sys
import random

pygame.init()

CELLS = 40
CELL_SIZE = 20
SCREEN_WIDTH = CELLS * CELL_SIZE
SCREEN_HEIGHT = CELLS * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇")
game_over = pygame.image.load("game-over.png").convert_alpha()
game_over = pygame.transform.scale(game_over, (SCREEN_WIDTH, SCREEN_HEIGHT))
apple = pygame.image.load("apple.jpg").convert_alpha()
apple = pygame.transform.scale(apple, (CELL_SIZE, CELL_SIZE))

def show_game_over(surface):
    surface.blit(game_over, (0, 0))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

class Fruit:
    def __init__(self, snake, image):
        # create a fruit at a random location, make sure it isn't created in the snakes body
        self.x = random.randint(1, CELLS - 1)
        self.y = random.randint(1, CELLS - 1)
        self.pos = Vector2(self.x, self.y)
        self.image = image
        while self.pos in snake.body:
            self.x = random.randint(1, CELLS - 1)
            self.y = random.randint(1, CELLS - 1)
            self.pos = Vector2(self.x, self.y)
        
    def draw(self, surface):
        fruit_rect = pygame.Rect(CELL_SIZE * self.pos.x, CELL_SIZE * self.pos.y, CELL_SIZE, CELL_SIZE)
        surface.blit(self.image, fruit_rect)



class Snake:
    def __init__(self):
        self.body = []
        for i in range(25, 28):
            self.body.append(Vector2(i, 10))

        self.direction = "left"

    def draw(self, surface):
        for block in self.body:
            body_rect = pygame.Rect(CELL_SIZE * block.x, CELL_SIZE * block.y, CELL_SIZE, CELL_SIZE)
            color = (255, 255, 255)
            pygame.draw.rect(surface, color, body_rect)


    def move(self, direction = None):
        if direction is None:
            direction = self.direction


        elif direction is not None:
            # Can't move left while moving right
            if direction == "right" and self.direction == "left":
                direction = "left"

            # Can't move right while moving left
            elif direction == "left" and self.direction == "right":
                direction = "right"

            # Can't move down while moving up
            elif direction == "down" and self.direction == "up":
                direction = "up"

            # Can't move up while moving down
            elif direction == "up" and self.direction == "down":
                direction = "down"

        # print(direction)

        if direction == "left":
            self.direction = direction
            old_pos = Vector2(self.body[0])
            self.body[0].x -= 1
            for i in range(1, len(self.body)):
                temp_pos = self.body[i]
                self.body[i] = Vector2(old_pos)
                old_pos = temp_pos
            
        elif direction == "right":
            self.direction = direction
            old_pos = Vector2(self.body[0])
            self.body[0].x += 1
            for i in range(1, len(self.body)):
                temp_pos = self.body[i]
                self.body[i] = Vector2(old_pos)
                old_pos = temp_pos


        elif direction == "up":
            self.direction = direction
            old_pos = Vector2(self.body[0])
            self.body[0].y -= 1
            for i in range(1, len(self.body)):
                temp_pos = self.body[i]
                self.body[i] = Vector2(old_pos)
                old_pos = temp_pos


        elif direction == "down":
            self.direction = direction
            old_pos = Vector2(self.body[0])
            self.body[0].y += 1
            for i in range(1, len(self.body)):
                temp_pos = self.body[i]
                self.body[i] = Vector2(old_pos)
                old_pos = temp_pos

    def is_valid_grow(self, block):
        block_x = block.x * CELL_SIZE
        block_y = block.y * CELL_SIZE
        invalid = block_x < 0 or block_x == CELLS * CELL_SIZE or block_y < 0 or block_y == CELLS * CELL_SIZE

        if invalid:
            return False

        invalid = block in self.body

        if invalid:
            return False

        return True

    def grow_body(self):
        tail = self.body[-1]
        block1 = Vector2(tail.x + 1, tail.y)
        block2 = Vector2(tail.x, tail.y + 1)
        block3 = Vector2(tail.x - 1, tail.y)
        block4 = Vector2(tail.x, tail.y - 1)
        candidates = [block1, block2, block3, block4]
        free_blocks = [block for block in candidates if self.is_valid_grow(block)]
        if (len(free_blocks) == 0):
            print("Panic: no free blocks to grow tail, debug please")
            pygame.time.wait(10000)
            pygame.quit()
            sys.exit("no way to grow tail")

        self.body.append(free_blocks[0])


    def should_eat_fruit(self, fruit):
        head = self.body[0]
        return head.x == fruit.x and head.y == fruit.y
        
        
    def check_crash(self):
        head = self.body[0]
        head_x = head.x * CELL_SIZE
        head_y = head.y * CELL_SIZE
        game_done = head_x < 0 or head_x == CELLS * CELL_SIZE or head_y < 0 or head_y == CELLS * CELL_SIZE
        if not game_done:
            game_done = head in self.body[1:]

        return game_done

        
# icon = pygame.image.load("./icons/snake.jpg").set_colorkey((0,0,0))
# pygame.display.set_icon(icon)
clock = pygame.time.Clock()
snake = Snake()
fruit = Fruit(snake, apple)
score = 0
while True:
    screen.fill((175,215,70))
    keyCaptured = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN and not keyCaptured:
            if event.key == pygame.K_LEFT:
                snake.move("left")
                keyCaptured = True
            elif event.key == pygame.K_RIGHT:
                snake.move("right")
                keyCaptured = True
            elif event.key == pygame.K_UP:
                snake.move("up")
                keyCaptured = True
            elif event.key == pygame.K_DOWN:
                snake.move("down")
                keyCaptured = True

    # print("Blocks: ", snake.body)
    # fruit = Fruit()
    # fruit.draw(screen)
    # snake.move("up")
    if not keyCaptured:
        snake.move()

    if snake.should_eat_fruit(fruit):
        score += 1
        snake.grow_body()
        fruit = Fruit(snake, apple)

    snake.draw(screen)
    fruit.draw(screen)

    if snake.check_crash():
        show_game_over(screen)
    
    pygame.display.update()
    clock.tick(5)
    