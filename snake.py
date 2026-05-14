import turtle as t
import random
import time

# =========================
# GAME CONFIG
# =========================
WIDTH = 600
HEIGHT = 600
STEP = 20
DELAY = 0.08

score = 0
high_score = 0

# =========================
# SCREEN SETUP
# =========================
sc = t.Screen()
sc.title("Immortal Snake Game")
sc.bgcolor("black")
sc.setup(width=WIDTH, height=HEIGHT)
sc.tracer(0)

# =========================
# SNAKE HEAD
# =========================
head = t.Turtle()
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# =========================
# FOOD
# =========================
food = t.Turtle()
food.shape("circle")
food.color("red")
food.penup()

segments = []

# =========================
# SCOREBOARD
# =========================
pen = t.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(0, 260)

def update_score():
    pen.clear()
    pen.write(
        f"Score: {score}   High Score: {high_score}",
        align="center",
        font=("Courier", 24, "normal")
    )

update_score()

# =========================
# FOOD POSITION
# =========================
def random_food_position():
    x = random.randrange(-280, 281, STEP)
    y = random.randrange(-280, 281, STEP)
    return x, y

food.goto(random_food_position())

# =========================
# MOVEMENT FUNCTIONS
# =========================
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# =========================
# MOVE SNAKE
# =========================
def move():

    x = head.xcor()
    y = head.ycor()

    # Move head
    if head.direction == "up":
        y += STEP
    elif head.direction == "down":
        y -= STEP
    elif head.direction == "left":
        x -= STEP
    elif head.direction == "right":
        x += STEP

    # =========================
    # WALL WRAP (IMMORTAL MODE)
    # =========================
    if x > 290:
        x = -290
    elif x < -290:
        x = 290

    if y > 290:
        y = -290
    elif y < -290:
        y = 290

    head.goto(x, y)

# =========================
# AUTO AVOID SELF COLLISION
# =========================
def safe_move():

    next_x = head.xcor()
    next_y = head.ycor()

    if head.direction == "up":
        next_y += STEP
    elif head.direction == "down":
        next_y -= STEP
    elif head.direction == "left":
        next_x -= STEP
    elif head.direction == "right":
        next_x += STEP

    # Check if next move hits body
    for segment in segments:
        if segment.distance(next_x, next_y) < 5:

            # Automatically choose a safe direction
            directions = ["up", "down", "left", "right"]
            random.shuffle(directions)

            for d in directions:

                test_x = head.xcor()
                test_y = head.ycor()

                if d == "up":
                    test_y += STEP
                elif d == "down":
                    test_y -= STEP
                elif d == "left":
                    test_x -= STEP
                elif d == "right":
                    test_x += STEP

                collision = False

                for s in segments:
                    if s.distance(test_x, test_y) < 5:
                        collision = True
                        break

                if not collision:
                    head.direction = d
                    return

# =========================
# KEYBOARD CONTROLS
# =========================
sc.listen()
sc.onkeypress(go_up, "w")
sc.onkeypress(go_down, "s")
sc.onkeypress(go_left, "a")
sc.onkeypress(go_right, "d")

# =========================
# MAIN GAME LOOP
# =========================
while True:

    sc.update()

    # Auto-protect snake
    safe_move()

    # Move body
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # Move head
    move()

    # =========================
    # FOOD COLLISION
    # =========================
    if head.distance(food) < 20:

        food.goto(random_food_position())

        # Add new segment
        segment = t.Turtle()
        segment.speed(0)
        segment.shape("square")
        segment.color("grey")
        segment.penup()

        segments.append(segment)

        # Update score
        score += 10

        if score > high_score:
            high_score = score

        update_score()

        # Increase speed slightly
        if DELAY > 0.03:
            DELAY -= 0.001

    time.sleep(DELAY)