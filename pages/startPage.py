import tkinter as tk
from tkinter import ttk #/ Styling : ccs for tkinter.
#/ Need to import the class just to access to the instance in the dict for show_frame

LARGE_FONT = ('Verdana',12)

class StartPage(tk.Frame): #/ Nueva página.
    name = 'StartPage'
    def __init__(self,pianoRollInstance):
        parent = pianoRollInstance.container
        tk.Frame.__init__(self,parent) #/ parent frame
        label = tk.Label(self,text='Home Page',font=LARGE_FONT) #/ Create label object
        label.pack(pady=10,padx=10) #/ Add to the window.
        button1 = ttk.Button(self,text='Create a Piano Roll',command=lambda : pianoRollInstance.show_frame('NewPianoRoll'))
        button1.pack()
        button2 = ttk.Button(self,text='See available Piano Rolls') #,command=lambda : controller.show_frame(GalleryPianoRolls))
        button2.pack()
        print('Start Page pianoRollInstance.__dir__',pianoRollInstance.__dir__)