import turtle
import string
import random


positions = []
colors = ["Lavender", "Misty Rose", "Dark Slate Gray", "Midnight Blue", "Cornflower Blue",
          "Deep Sky Blue", "Dark Turquoise", "Forest Green", "Medium Sea Green", "Yellow",
          "Indian Red", "Sandy Brown", "Firebrick"]


def drawStickLeaf(L):
    L = drawStick(L)
    L = drawLeaf(L)
    return L


def drawLeaf(L):
    turtle.circle(1)
    return L


def rand_color():
    return random.choice(colors)


def drawStick(L):
    turtle.forward(3)
    return L


def pushPos(L):
    pos = turtle.position()
    ang = turtle.heading()
    L.append((pos, ang))
    turtle.left(45)
    return L


def popPos(L):
    pos, ang = L.pop()
    turtle.penup()
    turtle.setpos(pos)
    turtle.setheading(ang)
    turtle.pendown()
    turtle.right(45)
    return L


start = 's'
symbols = '01[]'
rules = {'0': '1[0]0', '1': '11', '[': '[', ']': ']'}
actions = {'0': drawStickLeaf, '1': drawStick, '[':pushPos,']': popPos}


def applyRules(cur, rules):
    newstring = ''
    newlist = [rules[s] for s in cur if s in rules]
    newstring = ''.join(newlist)
    return newstring


def runString(instring, actions):
    turtle.resetscreen()
    turtle.clearscreen()
    turtle.color(rand_color())
    turtle.speed(100)
    turtle.left(90)
    turtle.penup()
    turtle.back(400)
    turtle.pendown()
    states = []
    for l in instring:
        if l in actions:
            a = actions[l]
            states = a(states)


def runGrammar(initial, rules, iters=10):
    #turtle.color(rand_color())
    st = initial
    for _ in range(iters):
        st = applyRules(st, rules)
        runString(st, actions)


runGrammar('0', rules, 10)
