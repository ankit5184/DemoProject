import turtle as t
import random
import time

# Game setup
delay = 0.1
score = 0
high_score = 0

# Set up the screen
sc = t.Screen()
sc.title("Snake Game")
sc.bgcolor("black")
sc.setup(width=600, height=600)
sc.tracer(0)

# Snake head
head = t.Turtle()
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = t.Turtle()
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Scoreboard
pen = t.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Movement Functions
def go_up():
    if head.direction != "down": head.direction = "up"
def go_down():
    if head.direction != "up": head.direction = "down"
def go_left():
    if head.direction != "right": head.direction = "left"
def go_right():
    if head.direction != "left": head.direction = "right"

def move():
    if head.direction == "up": head.sety(head.ycor() + 20)
    if head.direction == "down": head.sety(head.ycor() - 20)
    if head.direction == "left": head.setx(head.xcor() - 20)
    if head.direction == "right": head.setx(head.xcor() + 20)

# Keyboard bindings
sc.listen()
sc.onkeypress(go_up, "w")
sc.onkeypress(go_down, "s")
sc.onkeypress(go_left, "a")
sc.onkeypress(go_right, "d")

# Main Game Loop
while True:
    sc.update()
    
    # Check for collision with border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"
        for segment in segments: segment.goto(1000, 1000)
        segments.clear()
        score = 0
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Check for collision with food
    if head.distance(food) < 20:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x, y)
        new_segment = t.Turtle()
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)
        score += 10
        if score > high_score: high_score = score
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Move segments
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()
    
    # Check for head collisions with body
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments: segment.goto(1000, 1000)
            segments.clear()
            score = 0
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    time.sleep(delay)
