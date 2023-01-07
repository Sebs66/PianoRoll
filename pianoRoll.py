import tkinter as tk
from pages.newPianoRoll import  NewPianoRoll
from pages.startPage import StartPage
from pages.setImageHeight import GetImagesHeight

#/ class ClassName(herence)
class PianoRollApp(tk.Tk): #/ Tk : Toplevel widget of Tk which represents mostly the main window of an application
    def __init__(self,resolution='1600x900',*args,**kwargs): #/ *args : tupla de argumentos posicionales. *kwarg: dict de keyvalue args.
        self.title = 'PianoRollApp' #/ Definimos una propiedad de titulo para después saber qué estamos usando.
        tk.Tk.__init__(self,*args,**kwargs) #/ iniciamos un tk.Tk
        tk.Tk.iconbitmap(self,default='./images/icon.ico')
        tk.Tk.wm_title(self,self.title) #/ Set the title of this widget.
        tk.Tk.geometry(self,resolution)
        self.container = tk.Frame(self)
        self.container.pack(side='top',fill='both',expand=True)
        #/ fill va a llenar todo el espacio en ese pack, expand va a llenar más allá del espacio si esque hay más disponible.
        self.container.grid_rowconfigure(0,weight=1) #/ 0 es el minimo, weight es prioridad.
        self.container.grid_columnconfigure(0,weight=1)
        self.frames = {} #/ acá tendremos todas las instancias de cada pagina inicial. para poder ir cambiandolos cuando queramos.
        
        for Frame in (StartPage, NewPianoRoll, GetImagesHeight): #/ acá vamos inicializando todas las views y las metemos en el diccionario, para poder mostrarlas luego.
            frame = Frame(self) #/ construimos la instancia de cada clase de view, pasamos el contenedor y la instancia de PianoRollApp.
            print('type(frame)',type(frame))
            self.frames[Frame.name] = frame
            frame.grid(row=0,column=0,sticky='nsew') #sticky nsew es a todas las direcciones.
        
        self.show_frame('StartPage') #/ seteamos que la primera en mostrarse sea StartPage

    def show_frame(self,pageName:str): #/ funcion para mandar el frame del dict adelante.
        frame = self.frames[pageName] #/ Muestra la instancia de esa clase en la ventana.
        print(f'show_frame , {pageName} type(frame) {type(frame)}')
        print('\n')
        print(f'frame.__dict__ {frame.__dict__}')
        print('')
        print(f'Master {frame.master}  {frame.master.__dir__}')
        frame.tkraise() #/ tkraise -> heredado de tk.Tk

    def add_page(self,instance):
        self.frames[instance.name] = instance

