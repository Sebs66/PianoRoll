from pianoRoll import PianoRollApp

app = PianoRollApp()
print('app.__dir__',app.__dir__)
app.resize = (1700, 800) #/ parametro para mostrar imagenes más pequeñas. Debemos recuperar el tamaño normal.
app.mainloop()