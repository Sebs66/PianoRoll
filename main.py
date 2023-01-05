import tkinter as tk
from tkinter import ttk #/ Styling : ccs for tkinter.
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import pathlib

from utils.openCV_fn import VideoInfo, resize_Image,takeFramesV2, cutImageByHeight, mergeImgs
from utils.various import buildLinkedList, Node, LinkedList

LARGE_FONT = ('Verdana',12)
NORM_FONT = ('Verdana',10)
SMALL_FONT = ('Verdana',8)

resize = (1700, 800) #/ parametro para mostrar imagenes más pequeñas. Debemos recuperar el tamaño normal.
def confirm_position(overlapHeight,Ycoord,GetImagesHeightObject:object):
    '''
    selected_images is a dict with the keys 'coverImg' & 'image0'
    overlapHeight is the overlap height value.
    Ycoord is the heigth of the piano roll per image, to be cropped.
    '''
    videoClass = GetImagesHeightObject.videoClass

    image0 = GetImagesHeightObject.selected_images["image0"]
    print(f'overlap value : {overlapHeight}')
    print(f'Heigth of piano roll per image: {Ycoord}')
    print(f'Cover Image: {GetImagesHeightObject.selected_images["coverImg"]}')
    print(f'Image0: {image0}')
    print(f'Data folder : {GetImagesHeightObject.dataPath}')
 
    #/ Hacer la magia acá.
    #/ Capturar todas las fotos.
    takeFramesV2(videoClass.path,videoClass.intervals)
    mergeImgs(videoClass.path,image0,int(Ycoord),int(overlapHeight))


def release(event,self):
    print('release')
    print('self.img_height',self.img_height)
    Ycoord_adjusted = (self.img_height*event.y)/resize[1]
    self.Ycoord = Ycoord_adjusted
    print('Ycoord Adjusted',self.Ycoord)
    OverlapImgs.buildPage(self.controller.frames[OverlapImgs],self.node,self.Ycoord)

def on_mouse_event(event,text:tk.StringVar):
    text.set(f'Y coord: {event.y}')


# Bind the canvas to the mouse click and motion events
def start_move(event,canvas):
    # Start moving the image when the left mouse button is clicked
    canvas.scan_mark(event.x, event.y)

def move(event,canvas):
    # Move the image as the mouse is moved with the button pressed
    canvas.scan_dragto(event.x, event.y, gain=1)

def update_position(canvas, image_on_canvas, entry, value, OverlapImgsObject:object):
    # Get the value from the input field
    try:
        # Update the label with the new value
        desface = entry.get()
        print('update_position',desface)
        if int(desface) < 100:
            print('Please try a bigger value!')
            OverlapImgsObject.buttonConfirm['state'] = 'disabled'
            return
        OverlapImgsObject.buttonConfirm['state'] = 'normal'
        value[0] = int(desface) #/ Referencia para guardar el valor!
        canvas.coords(image_on_canvas, 0, desface)
        entry.delete(0,'end')
    except Exception as err:
        print('Exception',err)
        return

class PianoRollApp(tk.Tk): #/ Todo lo que está dentro del parentesis es para heredar.
    def __init__(self,*args,**kwargs):
        self.title = 'PianoRollApp'
        tk.Tk.__init__(self,*args,**kwargs) #/ iniciamos un tk.Tk
        tk.Tk.iconbitmap(self,default='./images/icon.ico')
        tk.Tk.wm_title(self,'Piano Roll')
        resolution = '1600x900'
        tk.Tk.geometry(self,resolution)
        container = tk.Frame(self)
        container.pack(side='top',fill='both',expand=True)
        #/ fill va a llenar todo el espacio en ese pack, expand va a llenar más allá del espacio si esque hay más disponible.
        container.grid_rowconfigure(0,weight=1) #/ 0 es el minimo, weight es prioridad.
        container.grid_columnconfigure(0,weight=1)
        self.frames = {} #/ acá tendremos todos los frames o views de nuestra aplicacion. para poder ir cambiandolos cuando queramos.
        for Frame in (StartPage,CreateNewPianoRoll,GalleryPianoRolls,GetImagesHeight,OverlapImgs): #/ acá vamos inicializando todas las views y las metemos en el diccionario, para poder mostrarlas luego.
            frame = Frame(container,self)
            self.frames[Frame] = frame
            frame.grid(row=0,column=0,sticky='nsew') #sticky nsew es a todas las direcciones.
        
        self.show_frame(StartPage) #/ seteamos que la primera en mostrarse sea StartPage

    def show_frame(self,controller): #/ funcion para mandar el frame del dict adelante.
        frame = self.frames[controller]
        frame.tkraise() #/ tkraise -> heredado de tk.Tk

class StartPage(tk.Frame): #/ Nueva página.
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent) #/ parent class!
        label = tk.Label(self,text='Home Page',font=LARGE_FONT) #/ Create label object
        label.pack(pady=10,padx=10) #/ Add to the window.
        button1 = ttk.Button(self,text='Create a Piano Roll',command=lambda : controller.show_frame(CreateNewPianoRoll))
        button1.pack()
        button2 = ttk.Button(self,text='See available Piano Rolls',command=lambda : controller.show_frame(GalleryPianoRolls))
        button2.pack()

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
        video = VideoInfo(path)
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
        

class GalleryPianoRolls(tk.Frame):
    def __init__(self,parent,controller):
        self.title = 'GalleryPianoRolls Page'
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text='PageTwo',font=LARGE_FONT) #/ Create label object
        label.pack(pady=10,padx=10) #/ Add to the window.
        button1 = ttk.Button(self,text='Back to Home',command=lambda : controller.show_frame(StartPage))
        #/ ttk.Button más bonito?
        button1.pack()

class GetImagesHeight(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent
        self.title = 'GetImagesHeight Page'
        self.subFrame = tk.Frame(self)
        self.subFrame.pack()
        self.video_path = None

    def buildPage(self,videoClass):
        #/ path its video path, not data path.
        print(f'buildPage, {self.title}')
        self.videoClass = videoClass
        dataPath = str(pathlib.Path(videoClass.path).parent.joinpath('data'))
        self.dataPath = dataPath
        print(dataPath)
        self.imgLinklist,self.listLen = buildLinkedList('E:\Media\HDPiano\Zoe Wees\data')
        #/ Asignaremos las variables que vamos a ocupar en otros metodos al self. para que sean como variables globales.
        self.selected_images = {}
        self.node = self.imgLinklist.head
        img = Image.open(self.imgLinklist.head.val)
        self.img_height = ImageTk.PhotoImage(img).height()
        my_img = ImageTk.PhotoImage(img.resize(resize))
        my_img.photo_ref = my_img # keep a reference
        self.controller.geometry('1900x900')
        self.text = tk.StringVar()
        self.text.set('Please select the cover image for the long notes image')
        instructions_label = tk.Label(self.subFrame,textvariable=self.text)
        self.my_label = tk.Label(self.subFrame,image=my_img)
        self.current_img = 1
        self.status_text = tk.StringVar() #/ tk inter specific!
        self.status_text.set(f'{self.current_img}/{self.listLen}')
        self.path_text = tk.StringVar() #/ tk inter specific!
        self.path_text.set(self.node.val)
        status_label = tk.Label(self.subFrame,textvariable= self.status_text,bd=1,relief='sunken',anchor=tk.E) #/ se ancla al este (derecha)
        path_label = tk.Label(self.subFrame,textvariable= self.path_text,bd=1,relief='sunken',anchor=tk.W)
        self.button_back = tk.Button(self.subFrame,text='<<',command= self.go_back)
        self.button_forward = tk.Button(self.subFrame,text='>>',command= self.go_forward)
        self.button_select_iterations = 0
        self.button_select = tk.Button(self.subFrame,text='Select Image',command= self.select)
        instructions_label.grid(row=0,column=0,columnspan=3)
        self.my_label.grid(row=1,column=0,columnspan=3)
        self.button_back.grid(row=2,column=0)
        self.button_select.grid(row=2,column=1)
        self.button_forward.grid(row=2,column=2)
        status_label.grid(row=3,column=2,columnspan=1,sticky=tk.W+tk.E) #/ sticky: se amplia de west a east
        path_label.grid(row=3,column=0,columnspan=2,sticky=tk.W+tk.E) #/ sticky: se amplia de west a east
        self.controller.show_frame(GetImagesHeight) #/ Go to page!

    def go_forward(self):
        #print('go_forward()')
        if self.node.next != None:
            self.current_img +=1
            self.status_text.set(f'{self.current_img}/{self.listLen}') #/ Podemos usar listLen ya que no la vamos a alterar y está en el scope parent!
            self.node = self.node.next
            imgPath = self.node.val
            self.path_text.set(imgPath)
            my_img = ImageTk.PhotoImage(Image.open(imgPath).resize(resize))
            my_img.photo_ref = my_img # keep a reference
            self.my_label.grid_forget()
            self.my_label = tk.Label(self.subFrame,image=my_img)
            self.my_label.grid(row=1,column=0,columnspan=3)
        return

    def go_back(self):
        #print('go_back()')
        if self.node.previous != None:
            self.current_img -=1
            self.status_text.set(f'{self.current_img}/{self.listLen}') #/ Podemos usar listLen ya que no la vamos a alterar y está en el scope parent!
            self.node = self.node.previous
            imgPath = self.node.val
            self.path_text.set(imgPath)
            my_img = ImageTk.PhotoImage(Image.open(imgPath).resize(resize))
            my_img.photo_ref = my_img # keep a reference
            self.my_label.grid_forget()
            self.my_label = tk.Label(self.subFrame,image=my_img)
            self.my_label.grid(row=1,column=0,columnspan=3)
        return

    def select(self):
        print('select()')
        if self.button_select_iterations == 0:
            self.selected_images['coverImg'] = self.node.val
            print(f'coverImg: {self.selected_images["coverImg"]}')
            self.text.set('Please select first image with notes on the screen')
            self.button_select_iterations += 1
        elif self.button_select_iterations ==1:
            self.selected_images['image0'] = self.node.val
            print(f'image0: {self.selected_images["image0"]}')
            self.text.set('Please click with the mouse the line separating the top of the piano and the notes carousel')
            print('Please click with the mouse the line separating the top of the piano and the notes carousel')
            self.button_select['state'] = 'disabled'
            self.button_back['state'] = 'disabled'
            self.button_forward['state'] = 'disabled'
            self.Ycoord = 0
            self.my_label.bind('<Motion>',lambda event: on_mouse_event(event,self.status_text))
            self.my_label.bind('<ButtonRelease>',lambda event: release(event,self))
        pass

class OverlapImgs(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.parent = parent
        self.title = 'OverlapImgs Page'
        self.subFrame = tk.Frame(self)
        self.subFrame.pack()

    def buildPage(self,node:Node,Ycoord:int):
        img1Url = node.val
        img2Url = node.next.val
        tempPath1 = pathlib.Path(__file__).parent.joinpath('temp/cut1.jpg')
        tempPath2 = pathlib.Path(__file__).parent.joinpath('temp/cut2.jpg')
        tempPath1 = cutImageByHeight(pathlib.Path(img1Url),Ycoord,tempPath1)
        tempPath2 = cutImageByHeight(pathlib.Path(img2Url),Ycoord,tempPath2)
        print(Ycoord)
        self.controller.show_frame(OverlapImgs)
        print(self.title)
        #/ Cambiamos color de imagen 1 para que haya más contraste.
        img1 = Image.open(tempPath1)
        img1 = img1.convert('RGB')
        enhancer = ImageEnhance.Color(img1)
        img1 = enhancer.enhance(5)
        img2 = Image.open(tempPath2)
        img2.putalpha(128) #/ cambiamos transparencia.
        image1 = ImageTk.PhotoImage(img1)
        image2 = ImageTk.PhotoImage(img2)
        image1.photo_ref = image1 # keep a reference
        image2.photo_ref = image2 # keep a reference
        #self.geometry(f"{image1.width()}x{image1.height()*3}")
        resolution = f"{image1.width()}x1024"
        self.controller.geometry(resolution)
        canvas = tk.Canvas(self.subFrame, width=image1.width(), height=image2.height()*1.2)
        # Create the image on the off-screen buffer using the create_image method
        desface = 150
        image1_on_canvas = canvas.create_image(0, desface, image=image1, anchor=tk.NW)
        image2_on_canvas = canvas.create_image(0, 0, image=image2, anchor=tk.NW)

        canvas.tag_bind(image2_on_canvas,'<Button-1>', lambda event: start_move(event,canvas))
        canvas.tag_bind(image2_on_canvas,'<B1-Motion>', lambda event: move(event,canvas))
        #/ en frame1 tendremos los botones.
        frame1 = tk.LabelFrame(self.subFrame,borderwidth=0,highlightthickness=0)
        label = tk.Label(frame1, text='Enter a value:')
        entry = tk.Entry(frame1)
        value = [0]
        self.buttonConfirm = tk.Button(frame1, text='Confirm', command=lambda: confirm_position(int(value[0]),Ycoord,GetImagesHeightObject))
        self.buttonConfirm['state'] = 'disabled'
        button = tk.Button(frame1, text='Update', command=lambda: update_position(canvas, image1_on_canvas, entry,value, self))
        GetImagesHeightObject = self.controller.frames[GetImagesHeight]
        buttonBack = tk.Button(frame1, text='Back', command=lambda: GetImagesHeight.buildPage(GetImagesHeightObject,GetImagesHeightObject.videoClass))
        frame2 = tk.Frame(self.subFrame,borderwidth=0,highlightthickness=0,pady=20)
        resize = [900,900]
        mini_img2 = ImageTk.PhotoImage(resize_Image(Image.open(tempPath2),resize))
        mini_img1 = ImageTk.PhotoImage(resize_Image(Image.open(tempPath1),resize))
        mini_img1.photo_ref = mini_img1 # keep a reference
        mini_img2.photo_ref = mini_img2 # keep a reference
        label_mini_img1 = tk.Label(frame2,image=mini_img1)
        label_mini_img2 = tk.Label(frame2,image=mini_img2)
        #/ Layout.
        #/ Grid dentro del frame, pack afuera de este.
        label.grid(row=0,column=0,columnspan=1)
        entry.grid(row=0,column=1,columnspan=1)
        button.grid(row=0,column=2,columnspan=1)
        self.buttonConfirm.grid(row=1,column=1,columnspan=1)
        buttonBack.grid(row=1,column=0)
        label_mini_img1.grid(row=0,column=0)
        label_mini_img2.grid(row=0,column=1)
        frame1.pack()
        canvas.pack()
        frame2.pack()
        #/ Bind method.
        entry.bind('<Return>',lambda event: update_position(canvas, image1_on_canvas, entry,value))
        #label.pack()
        # Run the Tkinter event loop

app = PianoRollApp()
app.mainloop()