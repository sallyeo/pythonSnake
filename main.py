from tkinter import *
import random


GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50     # the lower the num, the faster the game
BODY_PARTS = 3  # size of the item in the game
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # create a list of coordinates
        for i in range (0, BODY_PARTS):
            # coordinate of each body part starts at 0,0, snake at top left corner
            self.coordinates.append([0, 0])

        # create some squares
        # using x, y because we have a list of lists
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        # in 700 game width/height, each space is 50, so there's 700/50 = 14 spots
        # the random number is from 0 to 13 both included
        # so the food object will be placed randomly
        # convert to pixel by * SPACE_SIZE
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]

        # draw the food object on the canvas
        # 1st & 2nd arg is the starting coordinates
        # 3rd & 4th arg is the ending coordinates
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):

    # unpack the head of the snake
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # update the coordinates for the head of the snake before moving on to next turn
    # 0 the index, the head of the snake
    snake.coordinates.insert(0, (x, y))

    # create the new graphic for the head of the snake
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    # update snake's list of squares
    snake.squares.insert(0, square)

    # coordinate of the head of the snake & food object
    if x == food.coordinates[0] and y == food.coordinates[1]: # means they're overlapping

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        # only delete last body part of a snake if we do not eat the food object
        del snake.coordinates[-1]

        # update the canvas
        # -1 means the last set of coordinate
        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):

    # unpack the head of the snake
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # 1: means setting everything after the head of the snake
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)

    # show GAME OVER text in the center of the canvas
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")


window = Tk()   # object of Tk
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

# score label
label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# game board
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# so that it renders
window.update()

# to center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# how much we going to adjust the position of our window
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# control for the snake
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
