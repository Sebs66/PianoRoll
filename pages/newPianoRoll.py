import tkinter as tk
from utils.openCV_fn import VideoClass, resize_Image,takeFramesV2, cutImageByHeight, mergeImgs
from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog

from pages.setImageHeight import SetImagesHeight


LARGE_FONT = ('Verdana',12)

class NewPianoRoll(tk.Frame): #/ Select File Page.
    name = 'NewPianoRoll'
    '''
    This class represents the view to create a new piano roll image.
    The constructor takes the container in which the page/view will be created and the instance of the main app class: PianoRollApp
    '''
    def __init__(self,pianoRollInstance):
        #/ parent es el contenedor en el que estará contenida esta página.
        #/ pianoRollInstance -> instancia de la clase PianoRollApp.
        self.title = 'CreateNewPianoRoll Page'

        self.parent = pianoRollInstance.container
        self.pianoRollInstance = pianoRollInstance
        tk.Frame.__init__(self,self.parent)
        label = tk.Label(self,text='Create a new Piano Roll',font=LARGE_FONT) #/ Create label object
        label.pack(pady=10,padx=10) #/ Add to the window.
        subFrame = tk.Frame(self)
        button1 = tk.Button(subFrame,text='Back to Home',command=lambda : pianoRollInstance.show_frame('StartPage')) #/ instance
        button1.grid(row=1,column=0,sticky='nw')
        button2 = tk.Button(subFrame,text='Choose Video File',command= lambda : self.selectFile(pianoRollInstance))
        button2.grid(row=1,column=1,sticky='nw')
        self.subFrame_videoInfo = tk.Label(self,background='green')
        subFrame.pack()
        self.subFrame_videoInfo.pack(pady = 100,side=tk.TOP,fill=tk.BOTH,expand=True) #/ canvas with the video info.
    
    def selectFile(self,pianoRollInstance):
        print('selectFile')
        path = filedialog.askopenfilename(initialdir='E:/Media',title='Select video file',filetypes=(('.mkv','*.mkv'),('all files','*.*')))
        if path == '': return
        self.showFile(path)

    def showFile(self,path:str):
        for widget in self.subFrame_videoInfo.winfo_children():
            widget.destroy()
        print(path)
        video = VideoClass(path) #/ Creating an instance of VideoClass.
        minutes = int(video.duration/60)
        seconds = int(video.duration%60)
        cover = video.get_first_img() #/ Path of the cover img.
        resize = [600,600]
        cover_img = ImageTk.PhotoImage(resize_Image(Image.open(cover),resize))
        cover_img.photo_ref = cover_img
        text = f'Filename: {video.filename}\nPath: {video.path}\nVideo length: {minutes}:{seconds}\nfps: {video.fps}\nTotal frames: {video.frame_count}'
        label0 = tk.Label(self.subFrame_videoInfo,text='Selected File',font=LARGE_FONT,justify=tk.LEFT)
        label1 = tk.Label(self.subFrame_videoInfo,text=text,justify=tk.LEFT)
        frame_btns = tk.Frame(self.subFrame_videoInfo)
        label0.pack()
        label1.pack() #/ posicionar en el subFrame video info.
        frame_btns.pack()
        textlabel = tk.Label(frame_btns,text='Define frame interval:')
        entry_intervals = tk.Entry(frame_btns)
        self.take_pictures_button = tk.Button(frame_btns,text='Process Video',command=lambda: self.processVideo(video,20,entry_intervals.get()))
        self.take_pictures_button['state'] = 'active'
        textlabel.grid(row=0,column=0)
        entry_intervals.grid(row=0,column=1)
        self.take_pictures_button.grid(row=0,column=2)
    
    def processVideo(self,videoClass:VideoClass,pictureLimit,interval):
        if interval == '':
            print('Try another interval value!')
            return
        interval = int(interval)
        videoClass.intervals = interval
        self.take_pictures_button['state'] = 'disabled'
        print('processVideo')
        print(videoClass.frame_count/interval)
        #takeFramesV2(videoClass.path,interval,pictureLimit)
        print(f'Tomamos las {pictureLimit} imágenes.')
        #/ pianoRollInstance es la app
        #/ Creamos una nueva ventana y la mostramos!.
        instance =  SetImagesHeight(self.pianoRollInstance,videoClass)
        self.pianoRollInstance.add_page(instance)
        self.pianoRollInstance.show_frame('SetImagesHeight')

        