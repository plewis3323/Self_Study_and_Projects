import turtle
import random

# Set up the screen
screen = turtle.Screen()
screen.title("Turtle Racing Game")
screen.bgcolor("white")
screen.setup(width=800, height=600)

# Create turtles
colors = ["red", "blue", "green", "yellow", "purple", "orange"]
turtles = []
start_y = -150

for color in colors:
    racer = turtle.Turtle()
    racer.color(color)
    racer.shape("turtle")
    racer.penup()
    racer.goto(-350, start_y)
    start_y += 60
    turtles.append(racer)

# Draw finish line
finish_line = turtle.Turtle()
finish_line.penup()
finish_line.goto(300, 200)
finish_line.pendown()
finish_line.right(90)
finish_line.forward(400)
finish_line.hideturtle()

# Function to start the race
def start_race():
    race_on = True
    while race_on:
        for racer in turtles:
            racer.forward(random.randint(1, 10))
            if racer.xcor() >= 300:
                race_on = False
                winner = racer.color()[0]
                print(f"The winner is the {winner} turtle!")
                break

# Key binding to start the race
screen.listen()
screen.onkey(start_race, "space")

# Main loop
screen.mainloop()
