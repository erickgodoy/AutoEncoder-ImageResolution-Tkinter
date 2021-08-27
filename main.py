import cv2
import tensorflow as tf
import os
import tkinter as tk
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import random

from keras.preprocessing import image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tensorflow import keras


BG_GRAY = "#7d5ba6"
BG_COLOR = "#fffcf9"
BG_BUTTON = "#55d6be"


#Text Color
TEXT_COLOR = "#36413e"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

#Cargar Modelo
autoencoder =  keras.models.load_model("model_rn.h5")
autoencoder.compile(optimizer='adam', loss='mse', metrics=['accuracy'])


class Application:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Proyecto 2da Unidad")
        self.window.resizable(width=False, height=False)        #Fijar Tamaño
        self.window.configure(width=1080, height=450, bg=BG_COLOR)   #Dimensiones de ventana
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Mejora de Resolución de Imagenes usando AutoEncoder", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
                
        #Buttons
        upload_button = Button(bottom_label, text="Subir Imagen", font = FONT_BOLD, width=15, bg=BG_BUTTON, command=lambda: self._upload_image())
        upload_button.place(relx=0.10, rely=0.008, relheight=0.04, relwidth=0.20)

        transform_button = Button(bottom_label, text="Transformar", font = FONT_BOLD, width=15, bg=BG_BUTTON, command=lambda: self._transform_image())
        transform_button.place(relx=0.30, rely=0.008, relheight=0.04, relwidth=0.20)

        download_button = Button(bottom_label, text="Descargar Imagen", font = FONT_BOLD, width=15, bg=BG_BUTTON, command=lambda: self._download_image())
        download_button.place(relx=0.50, rely=0.008, relheight=0.04, relwidth=0.20)

        exit_button = Button(bottom_label, text="Salir", font = FONT_BOLD, width=15, bg=BG_BUTTON, command=lambda:exit())
        exit_button.place(relx=0.70, rely=0.008, relheight=0.04, relwidth=0.20)

    
    #Functions
    def pixalate_image(self, image, scale_percent = 40):
        self.width = int(image.shape[1] * scale_percent / 100)
        self.height = int(image.shape[0] * scale_percent / 100)
        self.dim = (self.width, self.height)
        self.small_image = cv2.resize(image, self.dim, interpolation = cv2.INTER_AREA)
            
        #Escalar tamaño original
        self.width = int(self.small_image.shape[1] * 100 / scale_percent)
        self.height = int(self.small_image.shape[0] * 100 / scale_percent)
        self.dim = (self.width, self.height)
        self.low_res_image = cv2.resize(self.small_image, self.dim, interpolation =  cv2.INTER_AREA)
        return self.low_res_image


    def _download_image(self):
        id = random.random()
        path = 'descarga/img' + str(id) + '.png'
        self.f2.savefig(str(path), bbox_inches='tight')

    
    def _transform_image(self):
        self.img = image.load_img(str(self.fln), target_size=(80,80,3))
        self.img = image.img_to_array(self.img)
        self.img = self.img/255

        self.img = self.pixalate_image(self.img)
        
        self.input_array = np.array([self.img])

        self.predict = autoencoder.predict(self.input_array)

        self.f2 = Figure()
        self.a2 = self.f2.add_subplot(111)
        self.a2.imshow(self.predict[0])

        self.canvas2 = FigureCanvasTkAgg(self.f2, master=self.window)
        self.canvas2.get_tk_widget().place(relx=0.4, rely=0.085, relheight=0.7, relwidth=0.7)
        
    def _upload_image(self):
        self.fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Seleccionar Imagen", filetypes=(("JPG File", "*.jpg"),("PNG file","*.png")))
        self.img = image.load_img(str(self.fln), target_size=(80,80,3))
        self.img = image.img_to_array(self.img)
        self.img = self.img/255
        
        DIR_IMG = str(self.fln)

        self.img = self.pixalate_image(self.img)
            
        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.a.imshow(self.img)

        self.canvas = FigureCanvasTkAgg(self.f, master=self.window)
        self.canvas.get_tk_widget().place(relx=-0.1, rely=0.085, relheight=0.7, relwidth=0.7)
        
        
if __name__ == "__main__":
    app = Application()
    app.run()
