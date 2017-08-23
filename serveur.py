#!/usr/bin/env python3
import socket
from POO import Laby
from tkinter import Tk
from turtle import ScrolledCanvas, TurtleScreen
import sys
import io

sys.stdout = io.StringIO()

main = Tk()
can = ScrolledCanvas(main)
can.pack(fill="both",expand=True)
sc = TurtleScreen(can)
laby = Laby(can,sc)

sys.stdout, log = sys.__stdout__, sys.stdout.getvalue().encode()

co = socket.socket()
co.bind(("",1337))
co.listen(5)

while True :
        client = co.accept()[0]
        client.send(log)
        client.close()
