#===============================================================================
# MechaMule graphical user interface main file.
# Name(s): Johnson Le
# Date: January 15, 2019
#===============================================================================
# IMPORTS
#===============================================================================
from tkinter import *
import tkinter.font
# import RPi.GPIO #comment when not on pi

#===============================================================================
# Main GUI window setup
# Will start in fullscreen. f2 to toggle_fullscreen. f1 to close.
#===============================================================================
window = Tk()
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
window.geometry('%dx%d' % (screen_w, screen_h))
window.title("Beta GUI")

window.attributes('-fullscreen', True) #will start in fullscreen.
def toggle_fullscreen(event):
    window.attributes('-fullscreen', not window.attributes('-fullscreen'))

def close(event):
    # RPi.GPIO.cleanup()    #comment when not on pi
    window.destroy()

window.bind('<F2>', toggle_fullscreen)
window.bind('<F1>', close)

#===============================================================================
# loop till forever.
#===============================================================================
window.mainloop()
