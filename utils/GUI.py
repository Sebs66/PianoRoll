import tkinter as tk
import pathlib
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageEnhance
from functools import partial
import sys
import os
import asyncio
try:
    from utils.openCV_fn import *
except:
    from openCV_fn import *

def release(event,self):
    print('release')
    self.Ycoord = event.y
    print('Ycoord',self.Ycoord)
    

def on_mouse_event(event,text:tk.StringVar):
    text.set(f'Y coord: {event.y}')

def getYcoord(path,Ycoord=[0]):
    '''
    Ycoord=[0] es una lista para que sea una referencia y no se guarde en el stack. Asi no perdemos su valor.'''
    ws = tk.Tk()
    ws.title('Set image height')
    img = Image.open(path)
    img = ImageTk.PhotoImage(img)
    label = tk.Label(ws,image = img).pack()
    ws.bind('<ButtonRelease>',lambda event: release(event,ws,Ycoord))
    ws.mainloop()
    return Ycoord[0]

def getYcoordOnly(root,text,nodes):
    global Ycoord
    root.bind('<ButtonRelease>',lambda event: release(event,nodes,text,root))

def on_drag(event,image_id,canvas):
    # Get the relative mouse position within the canvas
    print('canvas.winfo_rootx()',canvas.winfo_rootx())
    print('canvas.winfo_rooty()',canvas.winfo_rooty())
    x = event.x
    y = event.y
    print(x,y,event.x_root,event.y_root)
    canvas.move(image_id, 1, 1)

# Bind the canvas to the mouse click and motion events
def start_move(event,canvas):
    # Start moving the image when the left mouse button is clicked
    canvas.scan_mark(event.x, event.y)

def move(event,canvas):
    # Move the image as the mouse is moved with the button pressed
    canvas.scan_dragto(event.x, event.y, gain=1)

def update_position(canvas, image_on_canvas, entry,value):
    print('update_position')
    # Get the value from the input field
    try:
        # Update the label with the new value
        desface = entry.get()
        value[0] = desface #/ Referencia para guardar el valor!
        canvas.coords(image_on_canvas, 0, desface)
        entry.delete(0,'end')
    except Exception as err:
        print('Exception',err)
        return

def resize_Image(image, maxsize):
    r1 = image.size[0]/maxsize[0] # width ratio
    r2 = image.size[1]/maxsize[1] # height ratio
    ratio = max(r1, r2)
    newsize = (int(image.size[0]/ratio), int(image.size[1]/ratio)) # keep image aspect ratio
    image = image.resize(newsize, Image.ANTIALIAS)
    return image

def confirm_position(value):
    print(int(value[0]))
    #/ Hacer la magia acá.

def overlapImg(img1Url,img2Url):
    root = tk.Tk()
    #/ Cambiamos color de imagen 1 para que haya más contraste.
    img1 = Image.open(img1Url)
    img1 = img1.convert('RGB')
    enhancer = ImageEnhance.Color(img1)
    img1 = enhancer.enhance(5)
    img2 = Image.open(img2Url)
    img2.putalpha(128) #/ cambiamos transparencia.
    image1 = ImageTk.PhotoImage(img1)
    image2 = ImageTk.PhotoImage(img2)
    image1.photo_ref = image1 # keep a reference
    image2.photo_ref = image2 # keep a reference
    root.geometry(f"{image1.width()}x{image1.height()*3}")
    canvas = tk.Canvas(root, width=image1.width(), height=image2.height()*1.5)
    # Create the image on the off-screen buffer using the create_image method
    desface = 150
    image1_on_canvas = canvas.create_image(0, desface, image=image1, anchor=tk.NW)
    image2_on_canvas = canvas.create_image(0, 0, image=image2, anchor=tk.NW)

    canvas.tag_bind(image2_on_canvas,'<Button-1>', lambda event: start_move(event,canvas))
    canvas.tag_bind(image2_on_canvas,'<B1-Motion>', lambda event: move(event,canvas))
    #/ en frame1 tendremos los botones.
    frame1 = tk.LabelFrame(root,borderwidth=0,highlightthickness=0)
    label = tk.Label(frame1, text='Enter a value:')
    entry = tk.Entry(frame1)
    value = [0]
    button = tk.Button(frame1, text='Update', command=lambda: update_position(canvas, image1_on_canvas, entry,value))
    buttonConfirm = tk.Button(frame1, text='Confirm', command=lambda: confirm_position(value))
    frame2 = tk.Frame(root,borderwidth=0,highlightthickness=0,pady=100)
    resize = [900,900]
    mini_img1 = ImageTk.PhotoImage(resize_Image(Image.open(img1Url),resize))
    mini_img2 = ImageTk.PhotoImage(resize_Image(Image.open(img2Url),resize))
    label_mini_img1 = tk.Label(frame2,image=mini_img1)
    label_mini_img2 = tk.Label(frame2,image=mini_img2)
    #/ Layout.
    #/ Grid dentro del frame, pack afuera de este.
    label.grid(row=0,column=0,columnspan=1)
    entry.grid(row=0,column=1,columnspan=1)
    button.grid(row=0,column=2,columnspan=1)
    buttonConfirm.grid(row=1,column=1,columnspan=1)
    label_mini_img2.grid(row=0,column=0)
    label_mini_img1.grid(row=0,column=1)
    frame1.pack()
    canvas.pack()
    frame2.pack()
    #/ Bind method.
    entry.bind('<Return>',lambda event: update_position(canvas, image1_on_canvas, entry,value))
    #label.pack()
    # Run the Tkinter event loop
    root.mainloop()

def home():
    root = tk.Tk()
    root.geometry(f"1920x1080")
    root.mainloop()


if __name__ == '__main__':
    #path = pathlib.Path(r'E:\Media\HDPiano\Zoe Wees NOT FINISHED\data\7__frame559.jpg')
    #y = getYcoord(path)
    #print('Ycoord',y)
    # from various import sorted_alphanumeric
    # folderPath = pathlib.Path(r'E:\Media\HDPiano\Zoe Wees NOT FINISHED')
    # imgList = os.listdir('E:\Media\HDPiano\Zoe Wees NOT FINISHED\data')
    # sorted = sorted_alphanumeric(imgList)
    path1 = 'D:\Documents\Coder\HDPiano\codigo\cut1.jpg'
    path2 = 'D:\Documents\Coder\HDPiano\codigo\cut2.jpg'
    overlapImg(path1,path2)
    home()