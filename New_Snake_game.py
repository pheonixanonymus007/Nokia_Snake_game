import pygame
import random

# Colors ### Easily Editable
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 250, 0)

#Initialisation
pygame.init()
width_of_screen = 900
height_of_screen = 600
gameWindow = pygame.display.set_mode((width_of_screen, height_of_screen))
pygame.display.set_caption("Nokia Snake Game - Made by Achyut")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Display score on the screen
def score_on_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Plotting the snake
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Making the welcome screen
def welcome():  #starting screen
    game_exit = False
    while not game_exit:
        gameWindow.fill((255, 182, 193))
        score_on_screen("Welcome to the Snake Game", black, 90, 250) 
        score_on_screen("Made by Achyut", green, 90, 290)
        score_on_screen("Press SPACEBAR to play", blue, 90, 330)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()
        pygame.display.update()
        clock.tick(60)

# Snake game function
def game():
    game_exit = False
    game_over = False
    snake_x = 45 #lenghth of the snake 
    snake_y = 55 #width of the snake
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    score = 0
    apple_x = random.randint(20, width_of_screen - 20)
    apple_y = random.randint(20, height_of_screen - 20)
    snake_size = 30
    snake_list = []
    snake_length = 1
    fps = 40
    
    # High score handling with error check
    try:
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())
    except (FileNotFoundError, ValueError):
        highscore = 0

    while not game_exit:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            score_on_screen("Game Over! Press ENTER to continue", red, 100, 250)#game over screen
            score_on_screen("Ma'am, Please give marks for this", black, 90, 290)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()#return back to the starting screen
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:#marking controls to move the snake
                    if event.key == pygame.K_RIGHT and velocity_x == 0:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT and velocity_x == 0:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP and velocity_y == 0:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN and velocity_y == 0:
                        velocity_y = init_velocity
                        velocity_x = 0
                        
            snake_x += velocity_x
            snake_y += velocity_y

            # Apple eating logic
            if abs(snake_x - apple_x) < 20 and abs(snake_y - apple_y) < 20:
                score += 1
                apple_x = random.randint(20, width_of_screen - 20)
                apple_y = random.randint(20, height_of_screen - 20)
                
                # Ensure apple doesn't spawn inside the snake, Till the dry run it didn't happen, but will
                while [apple_x, apple_y] in snake_list:
                    apple_x = random.randint(20, width_of_screen - 20)
                    apple_y = random.randint(20, height_of_screen - 20)
                
                snake_length += 1
                if score > highscore:
                    highscore = score

            gameWindow.fill(white)
            score_on_screen("Score: " + str(score) + " Highscore: " + str(highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [apple_x, apple_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > width_of_screen or snake_y < 0 or snake_y > height_of_screen:
                game_over = True

            plot_snake(gameWindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps + (score // 50))  # Increase speed based on score
    
    pygame.quit()
    quit()

welcome()
