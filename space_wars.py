# Space War

import random
import turtle

# Set up the turtle
turtle.speed(0)
turtle.bgcolor("black")
turtle.ht()
# This saves memory
turtle.setundobuffer(1)
# This speeds up drawing
turtle.tracer(3)


class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

        # Boundary checking
        if self.xcor() > 240:
            self.setx(240)
            self.rt(60)
        if self.xcor() < -240:
            self.setx(-240)
            self.rt(60)
        if self.ycor() > 240:
            self.sety(240)
            self.rt(60)
        if self.ycor() < -240:
            self.sety(-240)
            self.rt(60)

    def isCollision(self, other):
        if ((((self.xcor() - other.xcor()) ** 2) + ((self.ycor() - other.ycor()) ** 2)) ** (0.5)) <= 15:
            return True
        else:
            return False


class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        # self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1


class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0, 360))


class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)

        # Boundary checking
        if self.xcor() > 240:
            self.setx(240)
            self.lt(60)
        if self.xcor() < -240:
            self.setx(-240)
            self.lt(60)
        if self.ycor() > 240:
            self.sety(240)
            self.lt(60)
        if self.ycor() < -240:
            self.sety(-240)
            self.lt(60)


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(0.4)
        self.speed = 20
        self.status = "ready"
        self.goto(700, 700)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(700, 700)

        if self.status == "firing":
            self.fd(self.speed)

        # Border checking
        if self.xcor() < -240 or self.xcor() > 240 or self.ycor() > 240 or self.ycor() < -240:
            self.goto(700, 700)
            self.status = "ready"


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        # draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-250, 250)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(500)
            self.pen.rt(90)
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" % (self.score)
        self.pen.penup()
        self.pen.goto(-250, 260)
        self.pen.write(msg, font=("Comic Sans MS", 16, "normal"))

    def game_over(self):
        self.pen.pendown()
        self.pen.goto(-100, 0)
        self.pen.write("GAME OVER", font=("Arial", 30, "normal"))
        self.pen.goto(-105, -5)
        self.pen.write("GAME OVER", font=("Arial", 30, "normal"))


# Create the game object
game = Game()
game.draw_border()

game.show_status()

# Create the sprites
player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)
# ally = Ally("square", "blue", 0, 0)
allies = []
for i in range(10):
    allies.append(Ally("square", "blue", 100, 100))


# Create The Enemeies
# enemy = Enemy("circle", "red", random.randint(-200, 200), random.randint(-200, 200))

enemies = []
for i in range(10):
    enemies.append(Enemy("circle", "red", random.randint(-200, -100), random.randint(-200, -100)))


# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()


# Main Game Loop
while True:
    turtle.update()
    player.move()
    # enemy.move()
    for enemy in enemies:
        enemy.move()
        if Sprite.isCollision(player, enemy):
            enemy.goto(random.randint(-200, 200), random.randint(-200, 200))

            game.score -= 100
            game.show_status()

        if Sprite.isCollision(missile, enemy):
            enemy.goto(random.randint(-200, 200), random.randint(-200, 200))
            missile.status = "ready"
            # increase the score
            game.score += 100
            game.show_status()

    missile.move()

    for ally in allies:
        ally.move()

        if Sprite.isCollision(missile, ally):
            ally.goto(random.randint(-200, 200), random.randint(-200, 200))
            missile.status = "ready"

            game.score -= 50
            game.show_status()

    # Collision checking
    if Sprite.isCollision(player, enemy):
        enemy.goto(random.randint(-200, 200), random.randint(-200, 200))

        game.score -= 100
        game.show_status()
        game.game_over()

    if Sprite.isCollision(missile, enemy):
        enemy.goto(random.randint(-200, 200), random.randint(-200, 200))
        missile.status = "ready"
        # increase the score
        game.score += 100
        game.show_status()

    if Sprite.isCollision(missile, ally):
        ally.goto(random.randint(-200, 200), random.randint(-200, 200))
        missile.status = "ready"

        game.score -= 50
        game.show_status()


turtle.mainloop()
