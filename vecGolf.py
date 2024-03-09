import os
import random
import time
import turtle
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring

# Initialize gui window
gui = Tk()
gui.title("vectorGolf")

# Make canvas for turtle
canvas = Canvas(gui, width=1280, height=1080, bg='green')
canvas.pack(side='left')  # Place canvas on the left side

screen = turtle.TurtleScreen(canvas)

# Initialize variables and scoreboard
n = 0
start = 0
end = 0
elapsed = 0
finalScore = 0
scoreboardFile = 'scoreboard.txt'
makeDB = open('scoreboard.txt', 'x')
makeDB.close()


def reset_scores():
    os.remove(scoreboardFile)


def calculate_score():
    global n, start, end, elapsed, finalScore
    multiplier = 1
    if n == 1:
        multiplier = 3
    if n == 2:
        multiplier = 2
    finalScore = (1000 * multiplier) / int(elapsed)
    print(finalScore)


def score():
    global n, elapsed, finalScore
    submit = askstring('Score', 'Enter your name:')
    if submit == '':
        messagebox.showinfo('Error', 'Blank name detected!\nUsing Anon as name...')
    calculate_score()
    if submit is not None:
        with open(scoreboardFile, 'a') as saveScore:
            if submit == '':
                submit = 'Anon'
            saveScore.write(f"\n{submit},{n},{int(elapsed)},{int(finalScore)}")
        messagebox.showinfo('Nice', f'{submit}\'s score submitted!')
        update()
    else:
        messagebox.showinfo('', 'Thank you for playing!')
        exit()


def update():
    scoreboard.delete(*scoreboard.get_children())
    with open(scoreboardFile, 'r') as f:
        for line in f:
            if line.strip():
                data = line.strip().split(',')
                scoreboard.insert('', 'end', values=data)


def make_plane():
    plane = turtle.RawTurtle(screen)
    plane.shape('circle')
    plane.shapesize(0.25)
    plane.speed(0)
    plane.goto(-500, 0)
    plane.stamp()
    plane.write(int(plane.xcor() / 10))
    for i in range(10):
        plane.forward(100)
        plane.stamp()
        plane.write(int(plane.xcor() / 10))

    plane.penup()
    plane.goto(0, 500)
    plane.right(90)
    plane.pendown()
    plane.stamp()
    plane.write(int(plane.ycor() / 10))
    for i in range(10):
        plane.forward(100)
        plane.stamp()
        plane.write(int(plane.ycor() / 10))


def check():
    global n, end, elapsed
    if minHoleX <= golfBall.xcor() <= maxHoleX:
        if minHoleY <= golfBall.ycor() <= maxHoleY:
            if n == 1:
                result = "Hole-in-One"
                plural = ''
            else:
                result = "Par"
                plural = 's'
            end = time.time()
            elapsed = (end - start)
            decision = messagebox.askquestion("You win!", f"{result}! You won in {n} putt{plural}!\n"
                                                          f"Submit score?")

            if decision != 'yes':
                decision2 = messagebox.askquestion("Quit", "Exit game?")
                if decision2 != 'yes':
                    return None
                else:
                    messagebox.showinfo("Thank you", "Thank you for playing vecGolf!")
                    exit()
            else:
                score()


def putt():
    global n
    puttX = puttX_entry.get()
    puttY = puttY_entry.get()

    try:
        float(puttX)
        float(puttY)
    except ValueError:
        messagebox.showinfo("Error", "Input must be a number.")
        return None

    if float(puttX) == 0 and float(puttY) == 0:
        return None
    else:
        finalPuttX = float(golfBall.xcor()) + (float(puttX) * 10)
        finalPuttY = float(golfBall.ycor()) + (float(puttY) * 10)

        golfBall.goto(finalPuttX, finalPuttY)
        n += 1

        check()

        puttX_var.set('0')
        puttY_var.set('0')
    return


def set_hole():
    global minHoleX, maxHoleX, minHoleY, maxHoleY
    minHoleX = golfHole.xcor() - 15
    maxHoleX = golfHole.xcor() + 15
    minHoleY = golfHole.ycor() - 15
    maxHoleY = golfHole.ycor() + 15
    return minHoleX, maxHoleX, minHoleY, maxHoleY


def new_ball():
    global golfBall
    golfBall = turtle.RawTurtle(screen)
    golfBall.turtlesize(1)
    golfBall.color('white')
    golfBall.shape('circle')
    golfBall.speed('slow')


def new_game():
    global golfHole, golfBall, holeX, holeY, n, start
    canvas.delete("all")
    canvas.config(bg='green')

    make_plane()

    golfHole = turtle.RawTurtle(screen)
    golfHole.hideturtle()
    holeX = random.randint(-500, 500)
    holeY = random.randint(-500, 450)
    golfHole.penup()
    golfHole.goto(holeX, holeY)
    golfHole.pendown()

    golfHole.setheading(180)
    golfHole.fillcolor('gray')
    golfHole.begin_fill()
    golfHole.circle(20)
    golfHole.end_fill()
    golfHole.setheading(90)

    golfHole.pensize(2)
    golfHole.pencolor('white')
    golfHole.forward(20)
    golfHole.pencolor('red')
    golfHole.forward(20)
    golfHole.pencolor('white')
    golfHole.forward(20)
    golfHole.pencolor('red')
    golfHole.forward(20)

    golfHole.setheading(0)
    golfHole.fillcolor('red')
    golfHole.begin_fill()

    for flag in range(2):
        golfHole.forward(30)
        golfHole.right(90)
        golfHole.forward(20)
        golfHole.right(90)

    golfHole.end_fill()
    golfHole.penup()
    golfHole.setheading(270)
    golfHole.forward(95)

    set_hole()
    new_ball()
    n = 0

    start = time.time()


def delete():
    selected_item = scoreboard.selection()[0]
    if selected_item:
        decision = messagebox.askquestion('Confirm Deletion', 'Are you sure you want to delete this score?')
        if decision == 'yes':
            item_values = scoreboard.item(selected_item, 'values')
            name = item_values[0]
            with open(scoreboardFile, 'r') as f:
                lines = f.readlines()
            with open(scoreboardFile, 'w') as f:
                for line in lines:
                    if name not in line:
                        f.write(line)
            update()
    else:
        messagebox.showinfo('No Selection', 'Please select an item to delete.')


def exit_game():
    decision = messagebox.askquestion('Confirm', 'Exit game?')

    if decision != 'yes':
        return None
    else:
        gui.destroy()


# Initialize game and ball

canvas.delete("all")
canvas.config(bg='green')

make_plane()

golfHole = turtle.RawTurtle(screen)
golfHole.hideturtle()
holeX = random.randint(-500, 500)
holeY = random.randint(-500, 450)
golfHole.penup()
golfHole.goto(holeX, holeY)
golfHole.pendown()

golfHole.setheading(180)
golfHole.fillcolor('gray')
golfHole.begin_fill()
golfHole.circle(20)
golfHole.end_fill()
golfHole.setheading(90)

golfHole.pensize(2)
golfHole.pencolor('white')
golfHole.forward(20)
golfHole.pencolor('red')
golfHole.forward(20)
golfHole.pencolor('white')
golfHole.forward(20)
golfHole.pencolor('red')
golfHole.forward(20)

golfHole.setheading(0)
golfHole.fillcolor('red')
golfHole.begin_fill()

for newline in range(2):
    golfHole.forward(30)
    golfHole.right(90)
    golfHole.forward(20)
    golfHole.right(90)

golfHole.end_fill()
golfHole.penup()
golfHole.setheading(270)
golfHole.forward(95)

minHoleX = golfHole.xcor() - 15
maxHoleX = golfHole.xcor() + 15
minHoleY = golfHole.ycor() - 15
maxHoleY = golfHole.ycor() + 15

golfBall = turtle.RawTurtle(screen)
golfBall.turtlesize(1)
golfBall.color('white')
golfBall.shape('circle')
golfBall.speed('slow')
n = 0

start = time.time()


# GUI Elements

scoreboardLabel = ttk.Label(gui, text="Scoreboard")
scoreboardLabel.pack(padx=20, pady=10)

scoreboardFrame = Frame(gui)
scoreboardFrame.pack()

scoreboard = ttk.Treeview(scoreboardFrame, selectmode='browse')
scoreboard['columns'] = ('Name', 'Putts', 'Time', 'Score')
scoreboard.column("#0", width=0, stretch=NO)
scoreboard.column("Name", anchor=W, width=100)
scoreboard.heading("Name", text="Name", anchor=W)
scoreboard.column("Putts", anchor=W, width=50)
scoreboard.heading("Putts", text="Putts", anchor=W)
scoreboard.column("Time", anchor=W, width=50)
scoreboard.heading("Time", text="Time", anchor=W)
scoreboard.column("Score", anchor=W, width=75)
scoreboard.heading("Score", text="Score", anchor=W)
scoreboard.pack(side='left', pady=5)

scrollBar = ttk.Scrollbar(scoreboardFrame, orient='vertical', command=scoreboard.yview)
scrollBar.pack(side='left', fill='y', expand=True)
scoreboard.configure(yscrollcommand=scrollBar.set)

puttFrame = Frame(gui)
puttFrame.pack(pady=15)
puttX_var = StringVar()
puttY_var = StringVar()

putt_label = ttk.Label(puttFrame, text="Enter x and y for your putt")
putt_label.pack(side='top')
puttX_entry = ttk.Entry(puttFrame, width=5, textvariable=puttX_var)
puttX_entry.pack(side='left')
puttY_entry = ttk.Entry(puttFrame, width=5, textvariable=puttY_var)
puttY_entry.pack(side='left')
puttButton = ttk.Button(puttFrame, text="Putt!", command=putt)
puttButton.pack(side='left')

buttonFrame = Frame(gui)
buttonFrame.pack(padx=10)

exitButton = ttk.Button(buttonFrame, text="Exit", command=exit_game)
exitButton.pack(side='left')

resetButton = ttk.Button(buttonFrame, text="New Game", command=new_game)
resetButton.pack(side='left')

deleteButton = ttk.Button(buttonFrame, text="Delete", command=delete)
deleteButton.pack(side='left')

update()

# Set entry variable
puttX_var.set('0')
puttY_var.set('0')

# Keep window open
gui.mainloop()
