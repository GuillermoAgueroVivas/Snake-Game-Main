import pygame
import time
import random

# Initializing PyGame
pygame.init()

# Defining colors
white = (255, 255, 255)
flower_blue = (100, 149, 237)  # Snake color
black = (0, 0, 0)  # Background
red = (255, 0, 0)  # 'Game Over' message
orange = (255, 165, 0)  # Food option 1
violet = (138, 43, 226)  # Food option 2

# Width and height of windows
width, height = 600, 400

# Setting up game display
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('The Crazy Snake Game')

clock = pygame.time.Clock()

snake_size = 10
snake_speed = 15

message_font = pygame.font.SysFont('friz-quadrata', 30)
score_font = pygame.font.SysFont('ubuntu', 25)

# The function, as its name suggests, is used to print the score in the game so far.
def print_score(score):
    text = score_font.render("Score:" + str(score), True, orange)
    game_display.blit(text, [0,0])

# The following function is in charge of drawing the snake to the screen according to the defied variable of 'snake_size' and another one referring to the amount of pixels it takes to
# draw the snake
def draw_snake(snake_size, snake_pixels):
    for pixel in snake_pixels:
        # Utilizing the 'draw' directory imported from PyGame we can use 'rect' to tell the code to show in the display
        # a rectangle for every pixel on the position of index 0 and index 1 utilizing those as coordinates in the X and Y axis and using the 'snake_size' assigned above as a reference to
        # how big they should be (10).
        pygame.draw.rect(game_display, flower_blue, [pixel[0], pixel[1], snake_size, snake_size])

# Main function to run the game
def run_game():
    game_over = False
    game_close = False

    # Defining a starting position using the width and height defined in the beginning of the code.
    x = width / 2
    y = height / 2

    x_speed = 0
    y_speed = 0

    # Defining the snake as a list since it will later grow in size.
    snake_pixels = []
    snake_length = 1 # Starts at one since we only have 1 pixel in the middle of the screen at the beginning

    # Defining the target (food) position using a random range in between '0' and the width minus the 'snake_size' so we have enough space to fit in the snake and divide by 10 so we get a floating
    # point result. Same with the height.
    target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
    target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0

    while not game_over:

        while game_close: # Also functions as an 'if' statement because if the game is closed then this will also execute
            game_display.fill(black)
            # Creating game over message using fonts defined above and displaying game over message.
            game_over_message = message_font.render("Game Over!", True, red)
            game_over_rect = game_over_message.get_rect(center =(width/2, height/3))
            game_display.blit(game_over_message, game_over_rect)
            # Updating score again
            print_score(snake_length - 1)
            # Creating a 'continue' message
            continue_message = message_font.render("Press 1 to Exit, 2 to Continue", True, white)
            continue_rect = continue_message.get_rect(center=(width/2, 350))
            game_display.blit(continue_message, continue_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: # If a key is pressed
                    if event.key == pygame.K_1: # If the key pressed is the number 1
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_2: # If the key pressed is the number 2
                        run_game()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            # If the 'x' is clicked to close the program
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_LEFT: # If the left key is pressed
                    x_speed = - snake_size
                    y_speed = 0
                if event.key == pygame.K_RIGHT: # If the right key is pressed
                    x_speed = snake_size
                    y_speed = 0
                if event.key == pygame.K_UP:  # If the up key is pressed
                    x_speed = 0
                    y_speed = - snake_size
                if event.key == pygame.K_DOWN:  # If the down key is pressed
                    x_speed = 0
                    y_speed = snake_size
        # Here we specify what happens when the snake hits the border of the window.
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        # The position of the head needs to be updated according to the speed
        x += x_speed
        y += y_speed
        # Filling in the background
        game_display.fill(black)
        # Creating the actual rectangle in screen representing the target (food) with the chosen color and using the
        # random positions generated above as 'target_x' and 'target_y'
        pygame.draw.rect(game_display, violet, [target_x, target_y, snake_size, snake_size])
        # Update the head of the snake which is constantly moving and add it to the list of the snake pixels while simultaneously removing the tail so the snake moves without stretching
        # all the time. This also needs to account for the fact that the snake will pick up at the food and at that moment we do not want to remove the tail because the snake is actaully
        # growing.
        snake_pixels.append([x,y])
        # Here we delete the tail
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]
        # For every pixel in 'snake_pixels' up until the last block before the end
        for pixel in snake_pixels[:-1]:
            # This line takes care of the snake crashing into itself. If the position of the pixel is where any of the other pixels are (so going right and then a sudden left for example)
            # then this also implies a game over.
            if pixel == [x,y]:
                game_close = True

        # Here we draw the snake using the 'draw_snake' function declared above.
        draw_snake(snake_size, snake_pixels)
        # Printing the score using the 'print_score' function declared above (we use the minus one because the snake already starts at 1 so that does not count as past of the score)
        print_score(snake_length - 1)
        # The line below keeps the display updating so the changes actually happen in real time.
        pygame.display.update()

        # Under we tell the code to spawn a new target if the position of the snake head matches the position of the target.
        if x == target_x and y == target_y:
            target_x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
            target_y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
            # And we increase the length by one
            snake_length += 1

        clock.tick(snake_speed)
    # If we get out of the loop we want to proceed to close the game.
    pygame.quit()
    quit()

run_game()