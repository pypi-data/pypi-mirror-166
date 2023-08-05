import tkinter as tk
import time
win = tk.Tk()
title = 'easy-game\'s GUI'
height = 800
width = 600
c = tk.Canvas(win,height=1080,width=1920)
c.pack()
looplist = list()
def clear():
    global c
    c.delete("all")

class Role:
    def __init__(self,img,x=0,y=0):
        global c
        self.x = x
        self.y = y
        self.img = tk.PhotoImage(file=img)
    def draw(self):
        global c
        image = c.create_image(self.x,self.y,image=self.img)

    def meet(self,ob):
        return (self.x,self.y) == (ob.x,ob.y)
    def update(self):
        self.img = tk.PhotoImage(file=img)

def setloop(func:type(lambda:None)):
    win.after(100,func)
    
def logonloop(name:str):
    exec('win.after(100,{})'.format(name))

def onMouseClick(func: type(lambda:None)):
    win.bind('<Button>', func)

def onKeyClick(func: type(lambda:None)):
    win.bind('<KeyPress>', func)

def setheight(num:int):
    global height
    height = num

def setwidth(num:int):
    global width
    width = num

def settitle(titlestr:str):
    global title
    title = titlestr

def go():
    global title
    global height
    global width
    global c
    global looplist
    c.pack()
    win.title(title)
    win.geometry(str(width) + 'x' + str(height))
    win.mainloop()