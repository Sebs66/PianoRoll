import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
import pathlib

from utils.various import buildLinkedList

class SetImagesHeight(tk.Frame):
    name = 'SetImagesHeight'
    def __init__(self,pianoRollInstance,videoClass):
        self.parent = pianoRollInstance.container
        print(f'SetImagesHeight parent: {self.parent.__dir__}')
        self.resize = pianoRollInstance.resize
        tk.Frame.__init__(self,self.parent)
        self.title = 'SetImagesHeight Page'
        #self.subFrame = tk.Frame(self)
        #self.subFrame.pack()
        self.video_path = None
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
        my_img = ImageTk.PhotoImage(img.resize(self.resize))
        my_img.photo_ref = my_img # keep a reference
        #self.pianoRollInstance.geometry('1900x900')
        self.text = tk.StringVar()
        self.text.set('Please select the cover image for the long notes image')
        instructions_label = tk.Label(self,textvariable=self.text)
        self.my_label = tk.Label(self,image=my_img)
        self.current_img = 1
        self.status_text = tk.StringVar() #/ tk inter specific!
        self.status_text.set(f'{self.current_img}/{self.listLen}')
        self.path_text = tk.StringVar() #/ tk inter specific!
        self.path_text.set(self.node.val)
        status_label = tk.Label(self,textvariable= self.status_text,bd=1,relief='sunken',anchor=tk.E) #/ se ancla al este (derecha)
        path_label = tk.Label(self,textvariable= self.path_text,bd=1,relief='sunken',anchor=tk.W)
        self.button_back = tk.Button(self,text='<<',command= self.go_back)
        self.button_forward = tk.Button(self,text='>>',command= self.go_forward)
        self.button_select_iterations = 0
        self.button_select = tk.Button(self,text='Select Image',command= self.select)
        instructions_label.grid(row=0,column=0,columnspan=3)
        self.my_label.grid(row=1,column=0,columnspan=3)
        self.button_back.grid(row=2,column=0)
        self.button_select.grid(row=2,column=1)
        self.button_forward.grid(row=2,column=2)
        status_label.grid(row=3,column=2,columnspan=1,sticky=tk.W+tk.E) #/ sticky: se amplia de west a east
        path_label.grid(row=3,column=0,columnspan=2,sticky=tk.W+tk.E) #/ sticky: se amplia de west a east

    def go_forward(self):
        #print('go_forward()')
        if self.node.next != None:
            self.current_img +=1
            self.status_text.set(f'{self.current_img}/{self.listLen}') #/ Podemos usar listLen ya que no la vamos a alterar y está en el scope parent!
            self.node = self.node.next
            imgPath = self.node.val
            self.path_text.set(imgPath)
            my_img = ImageTk.PhotoImage(Image.open(imgPath).resize(self.resize))
            my_img.photo_ref = my_img # keep a reference
            self.my_label.grid_forget()
            self.my_label = tk.Label(self,image=my_img)
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
            my_img = ImageTk.PhotoImage(Image.open(imgPath).resize(self.resize))
            my_img.photo_ref = my_img # keep a reference
            self.my_label.grid_forget()
            self.my_label = tk.Label(self,image=my_img)
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

class GetImagesHeight(tk.Frame):
    name = 'GetImagesHeight'
    def __init__(self,pianoRollInstance):
        parent = pianoRollInstance.container
        tk.Frame.__init__(self,parent)
        self.parent = pianoRollInstance.container
        self.title = 'GetImagesHeight Page'
        self.subFrame = tk.Frame(self)
        self.subFrame.pack()
        self.video_path = None

    def buildPage(self,pianoRollInstance,videoClass):
        #/ path its video path, not data path.
        print(f'buildPage, {self.title}')
        self.videoClass = videoClass
        self.resize = pianoRollInstance.resize
        dataPath = str(pathlib.Path(videoClass.path).parent.joinpath('data'))
        self.dataPath = dataPath
        print(dataPath)
        self.imgLinklist,self.listLen = buildLinkedList('E:\Media\HDPiano\Zoe Wees\data')
        #/ Asignaremos las variables que vamos a ocupar en otros metodos al self. para que sean como variables globales.
        self.selected_images = {}
        self.node = self.imgLinklist.head
        img = Image.open(self.imgLinklist.head.val)
        self.img_height = ImageTk.PhotoImage(img).height()
        my_img = ImageTk.PhotoImage(img.resize(self.resize))
        my_img.photo_ref = my_img # keep a reference
        pianoRollInstance.geometry('1900x900')
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
            my_img = ImageTk.PhotoImage(Image.open(imgPath).resize(self.resize))
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
            my_img = ImageTk.PhotoImage(Image.open(imgPath).resize(self.resize))
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

def release(event,self):
    print('release')
    print('self.img_height',self.img_height)
    Ycoord_adjusted = (self.img_height*event.y)/self.resize[1]
    self.Ycoord = Ycoord_adjusted
    print('Ycoord Adjusted',self.Ycoord)
    #OverlapImgs.buildPage(self.controller.frames[OverlapImgs],self.node,self.Ycoord)

def on_mouse_event(event,text:tk.StringVar):
    text.set(f'Y coord: {event.y}')