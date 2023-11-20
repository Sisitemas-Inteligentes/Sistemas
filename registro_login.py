import os
import cv2
from matplotlib import pyplot
from tkinter import StringVar, Entry, Button, Label, Toplevel
from tkinter import END
from mtcnn.mtcnn import MTCNN


class RegistroLogin:
    def __init__(self, ventana, app):
        self.pantalla1 = None
        self.pantalla2 = None
        self.ventana = ventana
        self.app = app
        self.usuario = StringVar()
        self.contra = StringVar()
        self.usuario_entrada = None
        self.contra_entrada = None
        self.usuario_entrada2 = None
        self.contra_entrada2 = None
        self.verificacion_usuario = StringVar()
        self.verificacion_contra = StringVar()

    def centrar_ventana(self, ancho, alto):
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla / 2) - (ancho / 2)
        y = (alto_pantalla / 2) - (alto / 2)
        self.ventana.geometry(f'{ancho}x{alto}+{int(x)}+{int(y)}')

    def mostrar_ventana_registro(self):
        self.pantalla1 = Toplevel(self.ventana)
        self.pantalla1.title("Registro")
        self.pantalla1.geometry("500x350")

        Label(self.pantalla1, text="Registro facial: debe asignar un usuario:").pack()
        Label(self.pantalla1, text="Registro tradicional: debe asignar usuario y contraseña:").pack()
        Label(self.pantalla1, text="").pack()
        Label(self.pantalla1, text="Usuario * ").pack()
        self.usuario_entrada = Entry(self.pantalla1, textvariable=self.usuario)
        self.usuario_entrada.pack()
        Label(self.pantalla1, text="Contraseña * ").pack()
        self.contra_entrada = Entry(self.pantalla1, textvariable=self.contra)
        self.contra_entrada.pack()
        Label(self.pantalla1, text="").pack()
        Button(self.pantalla1, text="Registro Tradicional", width=15, height=1, command=self.registrar_usuario).pack()

        Label(self.pantalla1, text="").pack()
        Button(self.pantalla1, text="Registro Facial", width=15, height=1, command=self.registro_facial).pack()

    def mostrar_ventana_login(self):
        self.pantalla2 = Toplevel(self.ventana)
        self.pantalla2.title("Login")
        self.pantalla2.geometry("300x250")
        self.centrar_ventana(300, 250)

        Label(self.pantalla2, text="Login facial: debe asignar un usuario:").pack()
        Label(self.pantalla2, text="Login tradicional: debe asignar usuario y contraseña:").pack()
        Label(self.pantalla2, text="").pack()

        Label(self.pantalla2, text="Usuario * ").pack()
        self.usuario_entrada2 = Entry(self.pantalla2, textvariable=self.verificacion_usuario)
        self.usuario_entrada2.pack()
        Label(self.pantalla2, text="Contraseña * ").pack()
        self.contra_entrada2 = Entry(self.pantalla2, textvariable=self.verificacion_contra, show='*')
        self.contra_entrada2.pack()
        Label(self.pantalla2, text="").pack()
        Button(self.pantalla2, text="Inicio de Sesion Tradicional", width=20, height=1,
               command=self.verificacion_login).pack()

        Label(self.pantalla2, text="").pack()
        Button(self.pantalla2, text="Inicio de Sesion Facial", width=20, height=1, command=self.login_facial).pack()

    def registrar_usuario(self):
        usuario_info = self.usuario.get()
        contra_info = self.contra.get()

        # Verifica si el directorio "db" existe, si no lo crea
        db_dir = "db"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        archivo_path = os.path.join(db_dir, usuario_info)
        with open(archivo_path, "w") as archivo:
            archivo.write(usuario_info + "\n")
            archivo.write(contra_info)

        self.usuario_entrada.delete(0, END)
        self.contra_entrada.delete(0, END)
        Label(self.pantalla1, text="Registro Convencional Exitoso", fg="green", font=("Calibri", 11)).pack()

    def registro_facial(self):
        usuario_info = self.usuario.get()

        # Verifica si el directorio db existe, si no lo crea
        db_dir = "db"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        img_path = os.path.join(db_dir, usuario_info + ".jpg")
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Registro Facial', frame)
            if cv2.waitKey(1) == 27:
                break

        cv2.imwrite(img_path, frame)
        cap.release()
        cv2.destroyAllWindows()

        self.usuario_entrada.delete(0, END)
        self.contra_entrada.delete(0, END)
        Label(self.pantalla1, text="Registro Facial Exitoso", fg="green", font=("Calibri", 11)).pack()

        def reg_rostro(imgagen, lista_resultados):
            data = pyplot.imread(imgagen)
            for i in range(len(lista_resultados)):
                x1, y1, ancho, alto = lista_resultados[i]['box']
                x2, y2 = x1 + ancho, y1 + alto
                pyplot.subplot(1, len(lista_resultados), i + 1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(os.path.join(db_dir, usuario_info + "_cara.jpg"), cara_reg)
                pyplot.imshow(data[y1:y2, x1:x2])
            pyplot.show()

        img = img_path
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)
        reg_rostro(img, caras)

    def verificacion_login(self):
        log_usuario = self.verificacion_usuario.get()
        log_contra = self.verificacion_contra.get()
        self.usuario_entrada2.delete(0, END)
        self.contra_entrada2.delete(0, END)

        db_dir = "db"
        if not os.path.exists(db_dir):
            print("Error: El directorio db no existe")
            return

        archivo_path = os.path.join(db_dir, log_usuario)
        if os.path.exists(archivo_path):
            with open(archivo_path, "r") as archivo:
                verificacion = archivo.read().splitlines()
                if log_contra == verificacion[1]:
                    print("Inicio de sesión exitoso")
                    self.app.cerrar_ventana(self.pantalla2)
                    self.app.mostrar_pagina_principal(log_usuario)
                else:
                    print("Contraseña incorrecta, ingrese de nuevo")
                    Label(self.pantalla2, text="Contraseña Incorrecta", fg="red", font=("Calibri", 11)).pack()
        else:
            print("Usuario no encontrado")
            Label(self.pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()

    def login_facial(self):
        # Iniciar la captura de video desde la cámara
        cap = cv2.VideoCapture(0)

        # Inicializar el detector facial (puedes ajustar los parámetros según sea necesario)
        detector = MTCNN()

        while True:
            # Leer un frame desde la cámara
            ret, frame = cap.read()

            # Mostrar el frame en una ventana
            cv2.imshow('Login Facial', frame)

            # Esperar a que se presione la tecla 'Esc' para salir
            if cv2.waitKey(1) == 27:
                break

        # Guardar la imagen capturada con el nombre del usuario
        usuario_img = self.usuario.get()
        cv2.imwrite(usuario_img + ".jpg", frame)

        # Liberar los recursos de la cámara y cerrar la ventana
        cap.release()
        cv2.destroyAllWindows()

        # Actualizar las entradas de usuario y contraseña
        self.usuario_entrada2.delete(0, END)
        self.contra_entrada2.delete(0, END)

        # Mostrar un mensaje de éxito
        Label(self.pantalla2, text="Inicio de Sesión Facial Exitoso", fg="green", font=("Calibri", 11)).pack()

        # Procesar la imagen para mostrar las caras detectadas
        img = usuario_img + ".jpg"
        pixeles = pyplot.imread(img)
        caras = detector.detect_faces(pixeles)
        self.mostrar_caras_detectadas(img, caras)

    def mostrar_caras_detectadas(self, img, lista_resultados):
        # Cargar la imagen y mostrar las caras detectadas
        data = pyplot.imread(img)

        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto

            # Mostrar la cara en una ventana
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            pyplot.imshow(data[y1:y2, x1:x2])

        # Mostrar la ventana con las caras detectadas
        pyplot.show()


