from tkinter import Tk,Button

import ttkbootstrap as ttkbootstrap
from ttkbootstrap import PRIMARY, SUCCESS, DANGER, WARNING, DARK, LIGHT

currentColor = 0
allColors = [PRIMARY, SUCCESS, DANGER, WARNING, DARK, LIGHT]


class ColorfulButtons(Button):
    def __init__(self, master, **kwargs):
        bootstyle = self.getColor()
        print(bootstyle)
        ttkbootstrap.Button.__init__(self,master,bootstyle=bootstyle)


        self.config(**kwargs)
        #


    def getColor(self):
        global currentColor
        currentColor += 1
        print(currentColor)
        currentColor %= allColors.__len__()
        return allColors[currentColor]


if __name__ == "__main__":
    w = Tk()
    a = ColorfulButtons(w, text="1")
    a.pack()
    b = ColorfulButtons(w, text="2")
    b.pack()
    c = ColorfulButtons(w, text="2")
    c.pack()
    w.mainloop()
