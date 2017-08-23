#!/usr/bin/env python3

import socket
from POO import Laby
from tkinter import Tk
from turtle import ScrolledCanvas, TurtleScreen
import io

co = socket.socket()
co.connect((input("IP : "),1337))
log = bytes()
while True :
        _ = co.recv(1)
        if len(_) == 0 :
                break
        else :
                log += _
log = io.StringIO(log.decode())

main = Tk()
can = ScrolledCanvas(main)
can.pack(fill="both",expand=True)
sc = TurtleScreen(can)
laby = Laby(can,sc,log)

main.mainloop()
