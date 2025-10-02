
import pygame
import random


def draw_board(screen, size, cell_width, cell_height, width, height):
    """
    This function draws the game board using the pygame.draw.line function.
    First, fill the screen with the desired background color, then draw the lines.
    If you are looking for more colors, visit https://www.pygame.org/docs/ref/color_list.html
    If you forget how to draw a line, visit https://www.pygame.org/docs/ref/draw.html#pygame.draw.lines

    :param screen: The surface to draw on.
    :param size: The board size (15x15 by default).
    :param cell_width: The number of pixels between each column.
    :param cell_height: The number of pixels between each row.
    :param width: Number of pixels for the screen width (default 450).
    :param height: Number of pixels for the screen height (default 450).
    :return: No return, just draw on the screen.
    """
    screen.fill('white')
    for i in range(size):
        pygame.draw.line(screen, 'black', (i * cell_width, 0), (i * cell_width, height), 1)
        pygame.draw.line(screen, 'black', (0, i * cell_height), (width, i * cell_height), 1)


def draw_snake(screen, snake, cell_width, cell_height):
    """
    This function draws the snake using pygame.draw.rect function.
    The head is drawn in a darker green to show where the snake is heading.

    :param screen: The surface to draw on.
    :param snake: The list of tuples representing the (x, y) coordinates where the snakes body is.
    :param cell_width: The number of pixels between each column.
    :param cell_height: The number of pixels between each row.
    :return: No return, just draw the snake.
    """
    pygame.draw.rect(screen, 'green3',
                     (snake[-1][0] * cell_width, snake[-1][1] * cell_height, cell_width, cell_height))
    for pos in snake[:-1]:
        pygame.draw.rect(screen, 'green',
                         (pos[0] * cell_width, pos[1] * cell_height, cell_width, cell_height))


def draw_apple(screen, apple, cell_width, cell_height):
    """
    In this function we will use pygame.draw.rect function to draw the apple.

    :param screen: The surface to draw on.
    :param apple: A tuple representing the (x, y) position of the apple.
    :param cell_width: The number of pixels between each column.
    :param cell_height: The number of pixels between each row.
    :return: No return, just draw the apple.
    """
    pygame.draw.rect(screen, 'red', (apple[0] * cell_width, apple[1] * cell_height, cell_width, cell_height))


def move_snake(snake, direction, size):
    """
    In this function you will move the head of the snake to the next position it is heading.
    Don't worry about removing the tail of the snake since we will only remove the tail
    in the condition that we did not hit the apple.

    :param snake: A list of tuples representing the (x, y) position of each body piece.
    :param direction: Tuple representing the change in direction for where snake is heading.
    :param size: The size of the board (default is 15x15).
    :return: Nothing to return, just move the snake.
    """

    tup = (snake[len(snake)-1][0] + direction[0], snake[len(snake)-1][1] + direction[1])
    snake.append(tup)
    snake.pop(0)

def hit_apple(apple, snake):
    """
    In this function you will detect if you have hit the apple.
    Remember, the snake head will collide first.

    :param apple: A tuple representing the (x, y) position of the apple.
    :param snake: A list of tuples representing the (x, y) position of each body piece.
    :return: Return True if there is a collision, or False if there is not.
    """

    if snake[len(snake)-1] == apple:
        return True
    else:
        return False


def move_apple(snake, size):
    """
    In this function you will find a new position for your apple. Remember,
    the new apple position should not land on top of the snake!

    :param snake: A list of tuples representing the (x, y) position of each body piece.
    :return: Return a tuple (x, y) which will be the new position of the apple.
    """

    testx = random.randint(0, size-1)
    testy = random.randint(0, size-1)
    while (testx, testy) in snake:
        test = random.randint(0, size-1)

    return (testx, testy)


def self_collision(snake):
    """
    This function will detect if the snake has run into itself.
    The self collision will end the game.

    :param snake: A list of tuples representing the (x, y) position of each body piece.
    :return: Return True if there is a self collision, or False if not.
    """
    
    if snake[len(snake)-1] in snake[:-2]:
        return True
    else:
        return False



# Variables needed for the game
SIZE = 15
SCREEN_SIZE = WIDTH, HEIGHT = 450, 450
CELL_SIZE = CELL_WIDTH, CELL_HEIGHT = WIDTH / SIZE, HEIGHT / SIZE
snake = [(0, 0)]
direction = (1, 0)
apple = (2, 1)
score = 0

# variables needed for pygame
FPS = 10
clock = pygame.time.Clock()
pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Snake!')

# Main game loop (where the game begins)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        if event.type == pygame.KEYDOWN:
            # remember, you can't move the opposite direction you are heading!
            if event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            if event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            if event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)

    # draw what we need
    draw_board(SCREEN, SIZE, CELL_WIDTH, CELL_HEIGHT, WIDTH, HEIGHT)
    draw_snake(SCREEN, snake, CELL_WIDTH, CELL_HEIGHT)
    draw_apple(SCREEN, apple, CELL_WIDTH, CELL_HEIGHT)

    # move the snake
    move_snake(snake, direction, SIZE)

    # check for collisions
    if hit_apple(apple, snake):
        score += 1
        print('Score: %d' % score)
        snake.append(apple)
        apple = move_apple(snake, SIZE)
        
    else:
        pass
        # what should we do if we don't hit the apple?

    # check to see if we lose
    if self_collision(snake):
        print('Game over! Final score: %d' % score)
        pygame.quit()
        exit(0)

    pygame.display.update()
    clock.tick(FPS)