#!/usr/bin/env python3
import turtle, tkinter, itertools
from random import choice, randrange

UNIT = 20
RAY = 200

main_window = tkinter.Tk()
canvas = turtle.ScrolledCanvas(main_window)
canvas.pack(fill="both",expand=True)
screen = turtle.TurtleScreen(canvas)
screen.tracer(n=600)

"""
Ce script :
- crée une GUI pour turtle (l.6-9)
- crée un labyrinthe aléatoire jusqu'à ce qu'il se referme sur lui-même
"""

left = turtle.RawTurtle(screen)#le mur gauche
right = turtle.RawTurtle(screen)#le mur droit

left.speed(0)#i.e. max
right.speed(0)

left.up()
left.goto((0,UNIT))
left.down()
left.ht()
right.ht()


def middle(x,y) :
        return (sum(x)/len(x),sum(y)/len(y))

def forward(left,right,fork=0):
        created = list()
        if fork%2 :
                new_ll = left.clone()
                new_ll.left(90)
                left.up()
        left.forward( UNIT)
        if fork%2 :
                left.down()
                new_lr = left.clone()
                new_lr.left(90)
                created.append((new_ll,new_lr))

        if fork > 1 :
                new_rr = right.clone()
                new_rr.right(90)
                right.up()
        right.forward( UNIT)
        if fork > 1 :
                right.down()
                new_rl = right.clone()
                new_rl.right(90)
                created.append((new_rl,new_rr))
        return created

def turn_left(left,right,fork=0):
        created = list()
        left.left(90)

        if fork%2 :
                new_ll = right.clone()
                new_ll.right(90)
                right.up()
        right.forward( UNIT)
        if fork%2 :
                right.down()
                new_lr = right.clone()
                new_lr.right(90)
                created.append((new_lr,new_ll))

        if fork > 1 :
                new_rr = right.clone()
                right.up()
        right.left(90)
        right.forward( UNIT)
        if fork > 1 :
                right.down()
                new_rl = right.clone()
                new_rl.right(90)
                created.append((new_rl,new_rr))
        return created

def turn_right(left,right,fork=0):
        created = list()
        right.right(90)
        if fork%2 :
                new_ll = left.clone()
                new_ll.left(90)
                left.up()
        left.forward( UNIT)
        if fork%2 :
                left.down()
                new_lr = left.clone()
                new_lr.left(90)
                created.append((new_ll,new_lr))

        if fork > 1 :
                new_rr = left.clone()
                left.up()
        left.right(90)
        left.forward( UNIT)
        if fork > 1 :
                left.down()
                new_rl = left.clone()
                new_rl.left(90)
                created.append((new_rr,new_rl))
        return created

def ahead(left,right,func=forward):
        fake_left = left.clone()
        fake_right = right.clone()
        fake_left.up()
        fake_right.up()

        func(fake_left,fake_right)
        m = ({left.xcor(),fake_left.xcor(),right.xcor(),fake_right.xcor()},
             {left.ycor(),fake_left.ycor(),right.ycor(),fake_right.ycor()})
        m = [{round(x) for x in string} for string in m]
        return [middle(*m),(fake_left,fake_right)]

def parse_area(x,y):
        """return True if a turtle couple can be reached from (x,y)"""
        gone.add((x,y))
        if (x,y) in pos_turtle.values() :
                return True
        else :
                for (i,j) in [(x-UNIT,y), (x+UNIT,y), (x,y-UNIT), (x,y+UNIT)] :
                        if (i,j) in pos_tracker or (i,j) in gone or abs(i)>=RAY or abs(j)>=RAY :
                                continue
                        if parse_area(i,j) :
                                return True
                return False


forced_move = {
        0:(forward,0),
        1:(forward,0),
        2:(turn_left,0),
        3:(turn_left,2),
        4:(turn_right,0),
        5:(turn_right,2),
        6:(turn_left,1),
        7:(forward,3)}

pos_tracker = set()
pos_turtle = dict()

turtles = [(left,right),]
remove = set()
adding = list()

while len(turtles)  :
        for i,(left,right) in enumerate(turtles):
                m, (fl,fr) = ahead(left,right)
                if m in pos_tracker  or abs(m[0])>RAY or abs(m[1])>RAY  :#déplacement impossible / limites atteintes
                        left.goto(right.pos())
                        del pos_turtle[(left,right)]
                        remove.add(i)
                        continue

                pos_tracker.add(m)

                #le déplacement doit-il être aléatoire ou forcé ?
                reachable = True
                for func in [forward,turn_left,turn_right] :
                        gone = set()
                        if not parse_area(*ahead(*ahead(left,right,func)[1])[0]):
                                reachable = False
                                break

                if reachable :#déplacement aléatoire
                        func = choice([forward,turn_left,turn_right])
                        fork = 0#randrange(4)
                else :#déplacement forcé
                        case = 0
                        for j,func in enumerate([forward,turn_left,turn_right]) :
                                fl,fr = ahead(left,right,func)[1]
                                if ahead(fl,fr)[0] not in pos_tracker :
                                        case += 2**j
                        func,fork = forced_move[case]


                adding.extend(func(left,right,fork=fork))

                m, (fl,fr) = ahead(left,right)
                if m in pos_tracker or abs(m[0])>RAY or abs(m[1])>RAY :#déplacement impossible
                        left.goto(right.pos())
                        del pos_turtle[(left,right)]
                        remove.add(i)


        turtles,remove,adding = [x for i,x in enumerate(turtles) if i not in remove]+adding, set(), list()
        for l,r in turtles :
                pos_turtle[(l,r)] = ahead(l,r)[0]

main_window.mainloop()
