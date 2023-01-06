import tkinter as tk

LARGE_FONT = ('Verdana',12)

class StartPage(tk.Frame): #/ Nueva página.
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent) #/ parent class!
        label = tk.Label(self,text='Home Page',font=LARGE_FONT) #/ Create label object
        label.pack(pady=10,padx=10) #/ Add to the window.
        button1 = ttk.Button(self,text='Create a Piano Roll',command=lambda : controller.show_frame(CreateNewPianoRoll))
        button1.pack()
        button2 = ttk.Button(self,text='See available Piano Rolls',command=lambda : controller.show_frame(GalleryPianoRolls))
        button2.pack()