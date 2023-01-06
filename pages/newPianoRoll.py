import tkinter as tk
from utils.openCV_fn import VideoClass, resize_Image,takeFramesV2, cutImageByHeight, mergeImgs
from PIL import Image, ImageTk, ImageEnhance

LARGE_FONT = ('Verdana',12)

class CreateNewPianoRoll(tk.Frame): #/ Select File Page.
    def __init__(self,parent,controller):
        self.title = 'CreateNewPianoRoll Page'
        self.parent = parent
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text='Create a new Piano Roll',font=LARGE_FONT) #/ Create label object
        label.pack(pady=10,padx=10) #/ Add to the window.
        subFrame = tk.Frame(self)
        button1 = tk.Button(subFrame,text='Back to Home',command=lambda : controller.show_frame(StartPage))
        button1.grid(row=1,column=0,sticky='nw')
        button2 = tk.Button(subFrame,text='Choose Video File',command= lambda : self.selectFile(controller))
        button2.grid(row=1,column=1,sticky='nw')
        self.subFrame_videoInfo = tk.Label(self,background='green')
        subFrame.pack()
        self.subFrame_videoInfo.pack(pady = 100,side=tk.TOP,fill=tk.BOTH,expand=True) #/ canvas with the video info.
    
    def selectFile(self,controller):
        print('selectFile')
        path = filedialog.askopenfilename(initialdir='E:/Media',title='Select video file',filetypes=(('.mkv','*.mkv'),('all files','*.*')))
        if path == '': return
        self.getFile(path,controller)

    def getFile(self,path:str,controller):
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
        take_pictures_button = tk.Button(frame_btns,text='Process Video',command=lambda: self.processVideo(video,20,int(entry_intervals.get()),controller))
        textlabel.grid(row=0,column=0)
        entry_intervals.grid(row=0,column=1)
        take_pictures_button.grid(row=0,column=2)
    
    def processVideo(self,videoClass:VideoInfo,pictureLimit,interval,controller):
        if interval == '':
            print('Try another interval value!')
            return
        videoClass.intervals = interval
        print('processVideo')
        print(videoClass.frame_count/interval)
        takeFramesV2(videoClass.path,interval,pictureLimit)
        print(f'Tomamos las {pictureLimit} imágenes.')
        #/ controller es la app
        #/ Construimos la pagina con la info que sacamos. La pagina ya existe como referencia, pero es una pagina vacía.    
        GetImagesHeightObject = controller.frames[GetImagesHeight]    
        GetImagesHeight.buildPage(GetImagesHeightObject,videoClass) #/ Builds the page and shows it!
        