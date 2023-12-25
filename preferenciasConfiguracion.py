#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
import json
import sys
import os
from ping3 import ping
from PIL import Image, ImageTk

def configuraciones():
	with open("configuraciones.json", "r") as file:
		data = json.load(file)
	return data

class Config(tk.Frame, tk.Toplevel):
	def __init__(self, parent, datosconfig, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.parent = parent
		self.parent.title("Configuraciones Preferencias")
		self.parent.geometry("500x400+150+10")
		self.parent.resizable(width=0, height=0)
		self.parent.protocol("WM_DELETE_WINDOW", self.volver)
		self.datosconfig = datosconfig
		self.create_tabs()

	def create_tab(self, tabControl, title):
		tab = tk.Frame(tabControl)
		tabControl.add(tab, text=title)

		if title == "Red":
			self.redTab(tab)  # NO ES DE COLOR SINO LA CONFIGURACION DE LA RED
		elif title == "Personalizacion":
			self.personalizacionTab(tab)
		elif title == "Sistema":
			self.sistemaTab(tab)

	def create_tabs(self):
		tabControl = ttk.Notebook(self.parent)

		tab_titles = ["Red", "Personalizacion", "Sistema"]

		for title in tab_titles:
			self.create_tab(tabControl, title)

		tabControl.pack(expand=1, fill="both")

	def volver(self):
		self.parent.deiconify()
		self.destroy()







	# [+] Cofiguracion de la red
	def redTab(self, parentTab): # NO ES DE COLOR SINO LA CONFIGURACION DE LA RED
		# Crear la etiqueta 1
		etiqueta1 = tk.Label(parentTab, text="Dirección de Servidor")
		etiqueta1.grid(row=0, column=0, padx=10, pady=10)
	
		direccion_var = tk.StringVar()
		direccion_var.set(self.datosconfig["servidorIp"])  # Valor inicial
		caja_texto = tk.Entry(parentTab, textvariable=direccion_var)
		caja_texto.grid(row=0, column=1, padx=10, pady=10)
	
		cuadricula_interna = tk.Frame(parentTab)
		cuadricula_interna.grid(row=1, column=0, padx=10, pady=10)
		
		# Agregar el mensaje "Puertos de visor" en la cuadrícula interna
		mensaje_interno = tk.Label(cuadricula_interna, text="Puertos de visor")
		mensaje_interno.grid(row=0, column=0, padx=5, pady=5)
		
		# Agregar etiquetas y cajas de texto para los puertos en la cuadrícula interna
		etiqueta_puerto1 = tk.Label(cuadricula_interna, text="Puerto1")
		etiqueta_puerto1.grid(row=1, column=0, padx=5, pady=5)
		caja_puerto1 = tk.Entry(cuadricula_interna)
		caja_puerto1.grid(row=1, column=1, padx=5, pady=5)
		caja_puerto1.insert(0, "9090")  # Valor inicial
		
		etiqueta_puerto2 = tk.Label(cuadricula_interna, text="Puerto2")
		etiqueta_puerto2.grid(row=2, column=0, padx=5, pady=5)
		caja_puerto2 = tk.Entry(cuadricula_interna)
		caja_puerto2.grid(row=2, column=1, padx=5, pady=5)
		caja_puerto2.insert(0, "9090")  # Valor inicial
		


		cuadricula_interna2 = tk.Frame(parentTab)
		cuadricula_interna2.grid(row=2, column=0, padx=10, pady=10)
		
		# Agregar el mensaje "Puertos de visor" en la cuadrícula interna
		mensaje_interno2 = tk.Label(cuadricula_interna2, text="Puertos de envio")
		mensaje_interno2.grid(row=0, column=0, padx=5, pady=5)
		
		# Agregar etiquetas y cajas de texto para los puertos en la cuadrícula interna
		etiqueta_puerto12 = tk.Label(cuadricula_interna2, text="Puerto1")
		etiqueta_puerto12.grid(row=1, column=0, padx=5, pady=5)
		caja_puerto12 = tk.Entry(cuadricula_interna2)
		caja_puerto12.grid(row=1, column=1, padx=5, pady=5)
		caja_puerto12.insert(0, "9090")  # Valor inicial
		
		etiqueta_puerto22 = tk.Label(cuadricula_interna2, text="Puerto2")
		etiqueta_puerto22.grid(row=2, column=0, padx=5, pady=5)
		caja_puerto22 = tk.Entry(cuadricula_interna2)
		caja_puerto22.grid(row=2, column=1, padx=5, pady=5)
		caja_puerto22.insert(0, "9090")  # Valor inicial


	# [+] funcion de configuracion de sistema de la ventana
	def sistemaTab(self, parentTab):
		rutaDescarga = tk.Label(parentTab, text="Dirección de Servidor")
		rutaDescarga.grid(row=0, column=0, padx=10, pady=10)
		
		rutaPredeterminada = tk.StringVar()
		rutaPredeterminada.set("~/Descarga")  # Valor inicial
		cajaRuta = tk.Entry(parentTab, textvariable=rutaPredeterminada)
		cajaRuta.grid(row=0, column=1, padx=10, pady=10)        


		# boton para las rutas del panel de las carpetas
		botonPanelCarpetas = tk.Button(parentTab, text="Ver Rutas Especiales", command=lambda: self.abrir_ventana(parentTab))
		botonPanelCarpetas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

	def abrir_ventana(self, parentTab):
		ventana_nueva = Toplevel(parentTab)
		ventana_nueva.title("Ventana Nueva")
		etiqueta = tk.Label(ventana_nueva, text="¡Esta es una nueva ventana!")
		etiqueta.pack(padx=20, pady=20)
		
		for carpeta in self.datosconfig["rutasFijas"]:
			tk.Button(ventana_nueva, text=carpeta, command=lambda carp=carpeta: self.modificacion(carp, ventana_nueva)).pack(pady=5)

	def modificacion(self, carpeta, parentTab):
		ventana_nueva = Toplevel(parentTab)
		ventana_nueva.title("Ventana Nueva")
		etiqueta = tk.Label(ventana_nueva, text="¡Esta es una nueva ventana!")
		etiqueta.pack(padx=20, pady=20)

		detalles = self.datosconfig["rutasFijas"][carpeta]
		
		cuadricula = tk.Label(ventana_nueva)
		cuadricula.pack()

		tk.Label(cuadricula, text="Titulo").grid(row=0, column=0, sticky="w")
		cajaTitulo = tk.StringVar()
		cajaTitulo.set(detalles["titulo"])  # Valor inicial
		caja_texto = tk.Entry(cuadricula, textvariable=cajaTitulo)
		caja_texto.grid(row=0, column=1)


		tk.Label(cuadricula, text="Icono").grid(row=1, column=0, sticky="w")
		cajaIcono = tk.StringVar()
		cajaIcono.set(detalles["icono"])  # Valor inicial
		caja_texto = tk.Entry(cuadricula, textvariable=cajaIcono)
		caja_texto.grid(row=1, column=1)

		tk.Label(cuadricula, text="Ruta").grid(row=2, column=0, sticky="w")
		cajaRuta = tk.StringVar()
		cajaRuta.set(detalles["ruta"])  # Valor inicial
		caja_texto = tk.Entry(cuadricula, textvariable=cajaRuta)
		caja_texto.grid(row=2, column=1)

	


	def personalizacionTab(self, parentTab):
		posicionPanel = tk.Label(parentTab, text="Posicion del Panel")
		posicionPanel.grid(row=0, column=0, padx=10, pady=10)
	
		valorPosicionPanel = tk.StringVar()
		valorPosicionPanel.set(self.datosconfig["posicionControles"])  # Valor inicial
		caja_posicionPanel = tk.Entry(parentTab, textvariable=valorPosicionPanel)
		caja_posicionPanel.grid(row=0, column=1)
			

		colorFondo = tk.Label(parentTab, text="Color de fondo")
		colorFondo.grid(row=2, column=0, padx=10, pady=10)
	
		valorColorFondo = tk.StringVar()
		valorColorFondo.set(self.datosconfig["backgroundColor"])  # Valor inicial
		cajaColorFondo = tk.Entry(parentTab, textvariable=valorColorFondo)
		cajaColorFondo.grid(row=2, column=1)

		

		dimesionIconosElementos = tk.Label(parentTab, text="Dimencion de los iconos de los elementos")
		dimesionIconosElementos.grid(row=3, column=0, padx=10, pady=10)
	
		valorDimensionElementos = tk.StringVar()
		valorDimensionElementos.set(self.datosconfig["dimensionIcon"])  # Valor inicial
		cajaDimensionElementos = tk.Entry(parentTab, textvariable=valorDimensionElementos)
		cajaDimensionElementos.grid(row=3, column=1)		
		


		margenLabelElementos = tk.Label(parentTab, text="Margen del label en los elementos")
		margenLabelElementos.grid(row=4, column=0, padx=10, pady=10)
	
		valorMargenElementos = tk.StringVar()
		valorMargenElementos.set(self.datosconfig["espacioMargen"])  # Valor inicial
		cajaMargenElementos = tk.Entry(parentTab, textvariable=valorMargenElementos)
		cajaMargenElementos.grid(row=4, column=1)		



		backgroundPanel = tk.Label(parentTab, text="Color de fondo de el panel")
		backgroundPanel.grid(row=5, column=0, padx=10, pady=10)
	
		valorBargroundPanel = tk.StringVar()
		valorBargroundPanel.set(self.datosconfig["backgroundControles"])  # Valor inicial
		cajaBackgroundPanel = tk.Entry(parentTab, textvariable=valorBargroundPanel)
		cajaBackgroundPanel.grid(row=5, column=1)		
		

		backgroundPanel = tk.Label(parentTab, text="Color del scrollbar")
		backgroundPanel.grid(row=6, column=0, padx=10, pady=10)
	
		valorBargroundPanel = tk.StringVar()
		valorBargroundPanel.set(self.datosconfig["colorScrollbar"])  # Valor inicial
		cajaBackgroundPanel = tk.Entry(parentTab, textvariable=valorBargroundPanel)
		cajaBackgroundPanel.grid(row=6, column=1)		


		backgroundPanel = tk.Label(parentTab, text="Color de seleccion")
		backgroundPanel.grid(row=7, column=0, padx=10, pady=10)
	
		valorBargroundPanel = tk.StringVar()
		valorBargroundPanel.set(self.datosconfig["colorClickeo"])  # Valor inicial
		cajaBackgroundPanel = tk.Entry(parentTab, textvariable=valorBargroundPanel)
		cajaBackgroundPanel.grid(row=7, column=1)		
		pass





def callback(event):
	sys.exit()

def reinicio(event):
	print("actualizando...")
	python = sys.executable
	os.execl(python, python, *sys.argv)

if __name__ == '__main__':
	data = configuraciones()
	root = tk.Tk()
	Config(root, data).pack()
	root.bind("<Escape>", callback)
	root.bind("<F5>", reinicio)
	root.mainloop()
