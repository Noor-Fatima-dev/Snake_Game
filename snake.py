from tkinter import *
import random

# Game settings
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Create main window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Score and direction
score = 0
direction = "Right"

# Score label
label = Label(window, text=f"Score: {score}", font=('consolas', 30))
label.pack()

# Game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

# Snake class
class Snake:
    def __init__(self):
        self.coordinates = [[100, 50], [50, 50], [0, 50]]  # Initial snake position
        self.block = []

        for x, y in self.coordinates:
            block = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
            self.block.append(block)

# Food class
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        self.food = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR)

# Move function
def Move(snake, food):
    global score

    head_x, head_y = snake.coordinates[0]

    if direction == "Up":
        head_y -= SPACE_SIZE
    elif direction == "Down":
        head_y += SPACE_SIZE
    elif direction == "Left":
        head_x -= SPACE_SIZE
    elif direction == "Right":
        head_x += SPACE_SIZE

    new_head = [head_x, head_y]

    # Check collisions
    if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT or new_head in snake.coordinates:
        game_over()
        return

    snake.coordinates.insert(0, new_head)

    block = canvas.create_rectangle(head_x, head_y, head_x + SPACE_SIZE, head_y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.block.insert(0, block)

    # Eat food
    if new_head == food.coordinates:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete(food.food)
        food.__init__()  # Create new food
    else:
        # Remove last part of snake
        del snake.coordinates[-1]
        canvas.delete(snake.block[-1])
        del snake.block[-1]

    window.after(SPEED, Move, snake, food)

# Direction change
def change_dir(event):
    global direction
    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"

# Game over
def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, font=('consolas', 60), fill="red", text="GAME OVER")

# Bind keys
window.bind("<Key>", change_dir)

# Start game
snake = Snake()
food = Food()
Move(snake, food)

window.mainloop()