#!/usr/bin/env python
import os 
from ping3 import  ping, verbose_ping 
from PIL import Image, ImageTk
import time
import tkinter as tk
import socket 
import sys 
import threading 
import json 
# ventana de configuracion 


from preferenciasConfiguracion import Config as conf


# [+] Funciones del programa 
# def __init__(self, parent, datosConfig, *args, **kwargs):
# def carpetasEspeciales(self, titulo, imagen, ruta , ancho = 20, alto = 20): 	
# def entrar_A_Carpeta(self,event, titulo, ruta, label1):
# def opcionesCarpetasEspeciales(self, event, titulo, label):
# def resizeImagen(self,ruta,nuevaImagen, ancho = 50, alto = 50): # funcion de resize imagenes 
# def ping(self, serverIp, *ports):
# def ordenes(self, orden):
# def interpreteJson(self, data):
# def labeles(self, frameElementos, columna,fila, archivo, imagenRuta):
# def clicleoLabeles(self, event, nombre, label):
# def anticlickeadoLabeles(self, event, nombre):
# def reinicio(self):
# def on_canvas_configure(self,event):
# def cancelar(self):
# def home (self):
# def limpiar(self):

def configuraciones ():
	with open("configuraciones.json", "r") as file:
		data = json.load(file)	
	return data



class Main(tk.Frame):
	def __init__(self, parent, datosConfig, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
	# [+] Variables de root del programa 
		self.datosConfig = datosConfig
		self.parent = parent
		self.ancho = datosConfig["ancho"]
		self.alto = datosConfig["alto"]

	# [+] Variables para las conexiones
		self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # definimos la coneccion
		self.servidor = datosConfig["servidorIp"] # aqui se va a obtener el ip del servidor 
		self.puerto1 = int(datosConfig["puerto"]) # puerto1 principal para el servidor
		self.puerto2 = int(datosConfig["puerto2"]) # puerto2 (secundario) para el servidor 
		self.rutaElementosServidor = "" # Esta es la variable donde vamos a obtener las respuestas de
					# los elementos que nos envie el servidor
		self.x_ = 0
		self.y_ = 0		
		self.n = 0
		self.labels = []
		self.imagenes = []  # Lista para almacenar las imágenes
		self.dataJson = None

		self.puertoVisor1 = int(datosConfig["puerto3"]) # puerto1 para el visor
		self.puertoVisor2 = int(datosConfig["puerto4"]) # puerto2 (secundario) para el visor
	# [+] Configuracion del programa 
		self.parent.geometry(f"{self.ancho}x{self.alto}+150+10") # geometrya de la ventana 
		self.parent.update() 
		self.ventana_ancho_info = self.parent.winfo_height() 
		self.ventana_alto_info = self.parent.winfo_width()
		self.parent.title(" Ventana cliente :D ")

	# [+] Variables otras:  
		self.labelSeleccionado = None # {-} sirve para mantener el control de los objetos que se clickean
		self.archivoPeticion = "" # {-} sirve para almacenar el nombre del archivo para pedir a descargar 


	
	# [+] Frames de contenedores [NEGRO]
		self.controles = tk.Frame(self.parent)
		self.anchoControles = int((self.ancho-10) * 0.2)
		self.controles.config(
			width = self.anchoControles,
			height = self.alto, 
			bg = datosConfig["backgroundControles"],
			relief = "solid"
			)
		#self.controles.resizable(width=0,height=0)

		self.controles.pack(fill = "both", expand = 0, side = datosConfig["posicionControles"])
		# [-] controles

		self.contenedor = tk.Frame(self.parent)
		self.scrollbar = tk.Scrollbar(self.parent, orient = "vertical", bg = datosConfig["colorScrollbar"])
		self.scrollbar2 = tk.Scrollbar(self.parent, orient = "horizontal", bg = datosConfig["colorScrollbar"])
		self.scrollbar2.pack(fill = "x", side = "bottom")
		self.scrollbar.pack(side = "right", fill = "y") # scrollbar

		self.anchoFrameElementos = int((self.ancho + 10) * 0.8)
		self.canvas = tk.Canvas(self.parent, 
			yscrollcommand = self.scrollbar.set, 
			xscrollcommand = self.scrollbar2.set, 
			bg = datosConfig["backgroundColor"], 
			width = self.ancho
		)
		self.canvas.pack(side="left", fill = "both", expand = True) 
		self.contenedor.pack(side="left", fill = "both", expand = True)
		self.scrollbar.config(command = self.canvas.yview)
		self.scrollbar2.config(command = self.canvas.xview)

		self.frameElementos = tk.Frame(self.canvas, bg = datosConfig["backgroundColor"])
		self.canvas.create_window((0,0),window= self.frameElementos, anchor = "nw")

		#for i in range(65):
		#	tk.Label(self.frameElementos, text = f"Elemento{i+1}").grid(row = i, column = 0)

		self.canvas.bind("<Configure>", self.on_canvas_configure)


	# {!} Declaracion de la barra de opciones
		# [+] Declaracion de la barra
		self.Menu = tk.Menu(self.parent)

		# [¡] Opciones_de_menu de ventana 
		self.opciones_de_menu = tk.Menu(self.Menu, tearoff = 0)
		self.opciones_de_menu.add_command(label = "Agregar")
		self.opciones_de_menu.add_separator()
		self.opciones_de_menu.add_command(label = "Salir", command = parent.quit)


		# [¡] opciones_de_menu de escaner 
		self.escaner = tk.Menu(self.Menu, tearoff = 0)
		self.escaner.add_command( label = "Reiniciar",command = self.reinicio)
		self.escaner.add_command(label = "Ver Lan")


		# [¡] Opciones para el programa, no para la ventana
		self.preferencias = tk.Menu(self.Menu, tearoff = 0)
		self.preferencias.add_command(label = "Configuraciones", command = self.prefConfig)

		# [¡] agregamos las opciones_de_menu a la barra 
		self.Menu.add_cascade(label = "Archivo ", menu = self.opciones_de_menu)
		self.Menu.add_cascade(label = "Lan", menu = self.escaner) 
		self.Menu.add_cascade(label = "Preferencias", menu = self.preferencias) 

		# [¡] asignamos la barra a la raiz de la ventana 
		self.parent.config(menu = self.Menu)
	# {-} Fin de declaracion de la barra de opciones

	# {-} Fin de declaracion de opciones de anticlick

	# [...] Ping al servidor si esta activo(solo si el host esta prendido) // 
	# falta mejorar este es solo la version 1.0
		pingThread = threading.Thread(target = self.ping, args = (self.servidor,
			self.puerto1, self.puerto2))
		pingThread.daemon = True
		pingThread.start()
		

	# {@} Conexion al servidor que nos dara la data o informacion con la que vamos a mostrar el contenido
		self.listado1 = self.ordenes("{'comando': 'ls'}") 

		self.interpreteJson(self.listado1) # lo que retorne lo pasamos al interprete 



	# {+!} CONTROLES PARA EL SERVIDOR
		# [+] Label de los botones
		self.botones = tk.Label(self.controles)
		self.botones.grid(sticky="nw")

		# [-] Botones del panel
		self.atrasImagen = self.resizeImagen(self.frameElementos,"atras.png", 30,30)
		self.atrasBoton = tk.Button(self.botones, image = self.atrasImagen, command = self.atras)
		self.atrasBoton.grid(row = 0, column = 1)

		self.homeImage = self.resizeImagen(self.frameElementos,"home.png", 30,30)

		self.homeBoton = tk.Button(self.botones, image = self.homeImage, command = self.home)
		self.homeBoton.grid(row = 0, column = 2)

		self.adelanteImagen = self.resizeImagen(self.frameElementos,"adelante.png", 30,30)
		self.adelanteBoton = tk.Button(self.botones, image = self.adelanteImagen, command = lambda: print("asas", self.x_, self.y_))
		self.adelanteBoton.grid(row = 0, column = 3)

	# [+] LUGARES FIJOS como el: Escritorio, Documentos, etc
		self.lugares = tk.Label(self.controles, text = datosConfig["tipoDirectorios"],
			font = datosConfig["fuenteLabelDirectorios"]) 
		self.lugares.grid(sticky="")

		self.directorios = tk.Label(self.controles)
		self.directorios.grid(sticky="")
		
		self.imagenesEspeciales = []
		dirs = datosConfig["rutasFijas"]
		for dirs_ in dirs:
			# aqui envio el nombre de la carpeta y el icono de la carpeta
			self.carpetasEspeciales(dirs[dirs_]["titulo"], dirs[dirs_]["icono"], dirs[dirs_]["ruta"])

	# [+] Funcion que hace un retroceso 
	def atras(self):
		self.entrar_A_Carpeta(None, "..",None, None)


	# {+} Estas 3 funciones son de los labeles Especiales o Carpetas Especiales
	# este es solo una funcion de declaracion de los labeles
	def carpetasEspeciales(self, titulo, imagen, ruta , ancho = 20, alto = 20):
		ruta = ruta 
		imagenEspecial = Image.open(imagen)
		imagenEspecial = imagenEspecial.resize((ancho, alto), Image.LANCZOS)
		imagenEspecial = ImageTk.PhotoImage(imagenEspecial)
		self.imagenesEspeciales.append(imagenEspecial)  # Almacena la imagen en la lista
		self.labelCarpeta = tk.Label(self.directorios, text=titulo, image=imagenEspecial, compound = self.datosConfig["ladoCarpetas"], anchor = "e")
		self.labelCarpeta.grid()
		
		# cuando se hace anticlick
		self.labelCarpeta.bind("<Button-3>", lambda event: self.opcionesCarpetasEspeciales(event, titulo, self.labelCarpeta))
		# cuando se hace click
		self.labelCarpeta.bind("<Button-1>", lambda event: self.entrar_A_Carpeta(event,titulo, ruta, self.labelCarpeta))

	# [+] Funcion encargada de la comunicacion entre el cliente y el servidor 
	def entrar_A_Carpeta(self,event, titulo, ruta, label1):
		event = event
		print(titulo, ruta)
		# aqui sigue la funcion donde se debera de enviar la orden al server
		orden = "{{'comando':'entrar', 'directorio': '{titulo}'}}".format(titulo=titulo)
		
		self.x = 1
		self.y = 1
		print("\n \n\n___________________________ \n", orden, "\n", ruta)
		listado = self.ordenes(orden)
		self.interpreteJson(listado)


		
	# [+] en esta funcion hara que se aparezcan las diferente opciones para los botones de las
	#  carpetasEspeciales 
	def opcionesCarpetasEspeciales(self, event, titulo, label):
		# abajo la funcion para que aparezcan las opciones
		print("presionado")
		pass 


	# [+] Funcion encargada de las imagenes en los labeles en el frame de los elementos
	def resizeImagen(self,ruta,nuevaImagen, ancho = 50, alto = 50): # funcion de resize imagenes 
		botonImagen = Image.open(rf"{nuevaImagen}")
		botonImagen = botonImagen.resize((ancho, alto), Image.Resampling.LANCZOS)
		botonImagen = ImageTk.PhotoImage(botonImagen)
		
		tk.Label(self.frameElementos, image = botonImagen)
		return botonImagen
	
	# [+] Funcion encargada de hacer un ping si el host esta activo
	# // solo hace ping al equipo si existe no si el puerto tambien esta activo
	def ping(self, serverIp, *ports): 
		"""
		while True:
			time.sleep(4)
			respuesta = ping(serverIp)
			if respuesta is not None:
				#print("respuesta de ping ", respuesta, end = "")
				pass
			else:
				print("no se recivio respuesta, reiniciare")
				self.reinicio() # invoca la funcion de reinicio<
		"""


	# [+] Esta funcion se encargara de enviar los comandos al servidor 
	def ordenes(self, orden):
		cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		SERVIDOR = self.servidor
		puerto1 = self.puertoVisor1
		puerto2 = self.puertoVisor2	
		
		try:
			cliente.connect((SERVIDOR, puerto1))
		except:
			cliente.connect((SERVIDOR, puerto2))

		orden = orden
		cliente.send(orden.encode())
		
		print("Esperando data.. ")

		data = cliente.recv(1024)
		try:
			mensaje = data.decode("utf-8")
		except: 
			return data

		#print(mensaje)
		cliente.close()
		return mensaje


	# [+] Esta funcion es el inicio de todo, esta recive la data en formato json y entonces lo interpreta 
	def interpreteJson(self, data):
		frameElementos = self.frameElementos # root de donde alojare y mostrare la informacion
		print("\n \n la data esta abajo")
		dataJson = json.loads(data) # convierto la data recivida del servidor en formato Json
		self.dataJson = dataJson
		self.limpiar()		
		# determinare el rango o numero de columnas que deberan de ir 
		if self.n == 0: # si el self.n == 0, entonces que haga la operacion de abajo
			self.rango = int(self.anchoFrameElementos/(self.datosConfig["dimensionIcon"] + self.datosConfig["espacioMargen"])) 
			self.n = self.rango 
		# NOTA: nose muy bien porque puse esta funcion, pero funciona, hacer que el self.rango se mantenga en el mismo numero,
		# asi puedo evitar errores al momento que hacer una actualizacion de por ejemplo entrar a una carpeta, entonces
		# el numero de las columnas no se reduce, ya que nose muy bien porque se reduce en 1 


		# este print indica la cantidad de columnas disponibles a crear tomando en cuenta la variable self.rango
		print(self.rango)

		# aqui asigno estas variables a una variable publica para que se mantenga en 0 despues de hacer las operaciones 
		# que viene a continuacion
		self.x = self.x_ 
		self.y = self.y_

		# Esta funcion hace recorrido por los datos recividos, en donde primero creara los labeles para las
		# carpetas
		for directorios in dataJson["directorios"]:
			if self.datosConfig["archivosOcultos"] is False and directorios.startswith("."):
				continue
			print("directorio: ", directorios)
			# lo siguiente es un control para poder calcular las posiciones x,y 
			if self.rango > self.x:
				self.x += 1

			elif self.x == self.rango:
				self.y += 1
				self.x = 1
			# llamado a la creacion de los labeles
			if directorios == "Escritorio" : # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{directorios}", self.datosConfig["iconos"]["dirEscritorio"])
			elif directorios == "Documentos" : # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{directorios}", self.datosConfig["iconos"]["dirDocumentos"])
			elif directorios == "Imágenes" : # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{directorios}", self.datosConfig["iconos"]["dirImagenes"])
			elif directorios == "Descargas" : # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{directorios}", self.datosConfig["iconos"]["dirDescargas"])
			else:
				self.labeles(frameElementos, self.x, self.y, f"{directorios}", self.datosConfig["iconos"]["Carpeta"])

		# en este for es lo mismo pero ahora, solo hara las operaciones con los archivos
		for archivo in dataJson["archivos"]:
			if self.datosConfig["archivosOcultos"] is False and archivo.startswith("."):
				continue
			print("archivo :", archivo)
			if self.rango > self.x:
				self.x += 1

			elif self.x == self.rango:
				self.y += 1
				self.x = 1


			# las condicionales indicaran que tipo de archivo es cada archivo recivido en la data
			if archivo.endswith(".d"): # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Dlang"])
			elif archivo.endswith(".py"): # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Python"])
			elif archivo.endswith(".c"): # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["C"])
			elif archivo.endswith(".cpp"): # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Cpp"])
			elif archivo.endswith(".json"): # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Json"])
			elif archivo.endswith(".exe"): # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Exe"])
			elif archivo.endswith(".gif" and ".png" or ".jpg" and "jpeg"): # determinacion si es .d Dlang <3
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Imagen"])
			elif archivo.endswith(".mp4"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Video"])
			elif archivo.endswith(".o"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Dll"])
			elif archivo.endswith(".so"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Dll"])
			elif archivo.endswith(".dll"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Dll"])
			elif archivo.endswith(".lib"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Dll"])
			elif archivo.endswith(".a"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Exe"])
			elif archivo.endswith(".exe"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Exe"])
			elif archivo.endswith(".out"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Exe"])
			elif archivo.endswith(".pdf"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Pdf"])
			elif archivo.endswith(".java"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["Java"])
			elif archivo.endswith(".class"):
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["JavaClass"])

			else: # si hay algun archivo que no se ha reconocido por su extencion entonces le dare un icono de no definido
				self.labeles(frameElementos, self.x, self.y, f"{archivo}", self.datosConfig["iconos"]["NoDefinido"])

	# [+] Esta funcion se encarga de la creacion de los elementos clickeables 
	def labeles(self, frameElementos, columna,fila, archivo, imagenRuta):
		self.labelSeleccionado = None # control: hace que cuando los labeles se actualizan, sus labeles se puedan reutilizar 

		# Esta funcion se encarga de definir el tamaño de las imagenes
		self.imagen = self.resizeImagen(self.frameElementos,imagenRuta, 
			self.datosConfig["dimensionIcon"], 
			self.datosConfig["dimensionIcon"]
			)
		# hace que las imagenes sean accesibles depues de haber hecho una actualizacion al frame principal
		self.imagenes.append(self.imagen)  # Agregar la imagen a la lista


		# Mostrar la imagen en una etiqueta
		label = tk.Label(frameElementos, 
			image=self.imagen, 
			bg = self.datosConfig["backgroundColor"], 
			height=110, 
			compound = tk.TOP, 
			width = self.datosConfig["dimensionIcon"] + self.datosConfig["espacioMargen"]
		)
		# este hace los labeles se agreguen a una lista que despues se podra usar, no me acuerdo bien para que 
		# era esta funcion pero se encarga del control de los labeles despues de las actualizaciones
		self.labels.append(label)
		
		# esta funcion detecta si se hizo un click sobre el label
		label.bind("<Button-1>", lambda event, lbl = label: self.clicleoLabeles(event,archivo, lbl))

		# abajo configuraciones del los labeles
		label.config(anchor=tk.N)
		label.grid(row = fila, column = columna)
		
		labelX = label.grid_info()
		labelX = labelX["ipadx"]
		labelY = label.grid_info()
		labelY = labelY["ipady"]
		
		# la condicion determinara si se le pondra un salto de linea al nombre del archivo
		# cuando aparezca abajo de la imagen del archivo
		if len(archivo) > 14: #
			parte1 = archivo[:14]
			parte2 = archivo[14:]
			archivo = parte1 + "\n" + parte2
		clabele = tk.Label(label, text = archivo, justify = "center", bg = "white",
			font = tuple(self.datosConfig["fuenteNombres"]),
			fg = self.datosConfig["colorNombres"])
		clabele.place(rely = 0.65) 
	

	# [+] Esta funcion se encarga de lo que es la funcion de lectura de los clickeos, 
	# ojo solo de los clickeos, no de los anticlicks 
	def clicleoLabeles(self, event, nombre, label):
		print("label", label)
		if "\n" in nombre: # esta condicion es solo para que se pueda ver el nombre del archivo  sin 
			nombre = nombre.replace("\n", "") #      	saltos de linea

		# condicion que hace que se pueda seleccionar los elementos
		if self.labelSeleccionado is not None:
			self.labelSeleccionado.config(bg = self.datosConfig["backgroundColor"])
			self.labelSeleccionado = None # este de aca hace que entonces solo se seleccione solo un elementos

		# color de cuando se selecciona un elemento, que es el ROJO
		label.config(bg = self.datosConfig["colorClickeo"]) 
 
		self.labelSeleccionado = label # no me acuerdo para que era pero era mas que todo para el control de los 
		# elementos clickeados

		print("Objeto clickeado : ", nombre)
		# una ves clickeado detecta si hay anticlick 
		label.bind("<Button-3>", lambda event: self.anticlickeadoLabeles(event,nombre))



	# [+] Funcion que se encarga de mostrar las opciones del elementos, Descargar, etc, en la 
	# 	misma posicion del mouse
	def anticlickeadoLabeles(self, event, nombre):
		# [+] Declaracion del anticlick y las opciones
		self.archivoPeticion = nombre
		self.opciones = tk.Menu(self.parent, tearoff = False)	
		self.opciones.add_command(label = "Descargar", 	command = lambda: self.descargar(self.archivoPeticion))


		# si es directorio entonces que aparezca la opcion de entrar
		if nombre in self.dataJson["directorios"]:
			self.opciones.add_command(label = "Entrar", command = lambda: self.entrar_A_Carpeta(None, self.archivoPeticion, None, None))
			
		self.opciones.tk_popup(event.x_root, event.y_root)

	# [+] Funcion encargada de descargar los archivos o directorios que quiera
	def descargar(self, elemento): 
		orden = "{{'comando':'descargar', 'elemento': '{nombre}'}}".format(nombre=elemento)
		print("Mensaje al servidor:", orden)

		cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		SERVIDOR = self.servidor
		puerto1 = self.puertoVisor1
		puerto2 = self.puertoVisor2
		
		try:
			cliente.connect((SERVIDOR, puerto1))
		except:
			cliente.connect((SERVIDOR, puerto2))

		orden = orden
		cliente.send(orden.encode())
		
		print("Esperando data.. ")
		
		descarga = b""
		while True:
			data = cliente.recv(1024)
			if not data:
				break
			descarga += data

		cliente.close()

		ruta = os.path.expanduser(os.path.join(self.datosConfig["rutaDescarga"], elemento))
		try:
			with open(ruta, "wb") as file:
				file.write(descarga)
			return "Archivo descargado y guardado en: " + ruta
		except Exception as e:
			return "Error al guardar el archivo: " + str(e)
		"""
		"""

	# {+} Funcion que reinicia el programa desde cero
	def reinicio(self):
		python = sys.executable # declaro de una instancia 
		os.execl(python, python, *sys.argv) # funcion de systema que reinicia el programa



	def on_canvas_configure(self,event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		#print("evento",event.width)
		#print("anchoframe" ,self.anchoFrameElementos)
		self.anchoFrameElementos = event.width
		#print("n anchoFrameElementos", self.anchoFrameElementos)
		self.parent.update()

	def cancelar(self):
		pass

	def home (self):
		home = self.ordenes("{'comando' : 'home'}")
		self.ordenes(home)

	# [+] No tocar esta funcion que se encarga de limpiar el frameElementos de todos los 
	# 		widgets
	def limpiar(self):
		for label in self.labels:
			label.grid_forget()
		self.labels = []

	def prefConfig(self):
		conf(self.parent)
			

def __callback(event):
	sys.exit()

def reinicio(event):
	print("actualizando... ")
	python = sys.executable # declaro de una instancia 
	os.execl(python, python, *sys.argv) # funcion de systema que reinicia el programa

if __name__ == '__main__':
	data = configuraciones()
	root = tk.Tk()
	# al ultimo poner un inicio como en mojang con la imagen daniLogo.jpg
	Main(root, data).pack()
	root.bind("<Escape>", __callback)
	root.bind("<F5>",reinicio)
	root.bind("<Configure>")
	root.mainloop()





