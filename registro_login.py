import os
import cv2
import shutil
from matplotlib import pyplot
from tkinter import StringVar, Entry, Button, Label, Toplevel, filedialog
from tkinter import END
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace

from comparacion_audio import comparar_audios


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
        self.centrar_ventana(500, 300)

        Label(self.pantalla1, text="Registro Iteligente: debe asignar un usuario:").pack()
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
        Button(self.pantalla1, text="Registro Inteligente", width=15, height=1, command=self.registro_facial).pack()

    def mostrar_ventana_login(self):
        self.pantalla2 = Toplevel(self.ventana)
        self.pantalla2.title("Login")
        self.pantalla2.geometry("300x250")
        self.centrar_ventana(300, 250)

        Label(self.pantalla2, text="Login Inteligente: debe asignar un usuario:").pack()
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
        Button(self.pantalla2, text="Inicio de Sesion Inteligente", width=20, height=1, command=self.login_facial).pack()

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

        # Guardar el archivo de audio en la carpeta "db" con el nombre del usuario
        audio_path = filedialog.askopenfilename(title=f"Seleccione el archivo de audio para {usuario_info}",
                                                filetypes=[("Archivos WAV", "*.wav")])

        if audio_path:
            nuevo_audio_path = os.path.join(db_dir, f"{usuario_info}.wav")
            shutil.copy(audio_path, nuevo_audio_path)

            Label(self.pantalla1, text="Registro Convencional Exitoso", fg="green", font=("Calibri", 11)).pack()
        else:
            Label(self.pantalla1, text="Error: No se seleccionó un archivo de audio", fg="red",
                  font=("Calibri", 11)).pack()

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
            cv2.imshow('Registro Inteligente', frame)
            if cv2.waitKey(1) == 27:
                break

        cv2.imwrite(img_path, frame)
        cap.release()
        cv2.destroyAllWindows()

        self.usuario_entrada.delete(0, END)
        self.contra_entrada.delete(0, END)
        self.guardar_primer_audio(usuario_info)
        Label(self.pantalla1, text="Registro Inteligente Exitoso", fg="green", font=("Calibri", 11)).pack()

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
            # pyplot.show()

        img = img_path
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)
        reg_rostro(img, caras)

    def guardar_primer_audio(self, usuario_info):
        # Obtener la ruta del archivo de audio seleccionado
        audio_path = filedialog.askopenfilename(title=f"Seleccione el archivo de audio para {usuario_info}",
                                                filetypes=[("Archivos WAV", "*.wav")])

        # Verificar si se seleccionó un archivo
        if audio_path:
            # Crear la carpeta "db" si no existe
            db_dir = "db"
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)

            # Construir la ruta de destino para guardar el archivo de audio
            nuevo_audio_path = os.path.join(db_dir, f"{usuario_info}.wav")

            # Copiar el archivo de audio seleccionado a la carpeta "db"
            shutil.copy(audio_path, nuevo_audio_path)

            # Informar sobre el éxito
            Label(self.pantalla1, text="Archivo de audio guardado exitosamente", fg="green",
                  font=("Calibri", 11)).pack()
        else:
            # Informar si no se seleccionó ningún archivo
            Label(self.pantalla1, text="Error: No se seleccionó un archivo de audio", fg="red",
                  font=("Calibri", 11)).pack()

        # Limpiar las entradas de usuario y contraseña
        self.usuario_entrada.delete(0, END)
        self.contra_entrada.delete(0, END)

    def verificacion_login(self):
        log_usuario = self.verificacion_usuario.get()
        print(log_usuario)
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

    def login_retina(self):
        usuario_info = self.usuario.get()

        # Verifica si el directorio "db" existe, si no lo crea
        db_dir = "db"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        img_path_retina = os.path.join(db_dir, usuario_info + "_retina.jpg")
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Registro de Retina', frame)
            if cv2.waitKey(1) == 27:
                break

        cv2.imwrite(img_path_retina, frame)
        cap.release()
        cv2.destroyAllWindows()

        # Verificar la similitud usando DeepFace
        img_path_facial = os.path.join(db_dir, usuario_info + "_facial.jpg")
        result = DeepFace.verify(img_path_facial, img_path_retina, model_name="VGG-Face",
                                 distance_metric='euclidean_l2')

        if result["verified"]:
            print("Inicio de Sesión con Retina Exitoso")
            self.app.cerrar_ventana(self.pantalla2)
            self.app.mostrar_pagina_principal(usuario_info)
        else:
            print("Inicio de Sesión con Retina Fallido")
            Label(self.pantalla2, text="Inicio de Sesión con Retina Fallido", fg="red", font=("Calibri", 11)).pack()

    def login_facial(self,):
        # Iniciar la captura de video desde la cámara
        cap = cv2.VideoCapture(0)

        # Inicializar el detector facial (puedes ajustar los parámetros según sea necesario)
        detector = MTCNN()

        # Obtener el nombre de usuario desde la entrada
        nombre_usuario = self.usuario.get()

        # Verificar si el directorio "db" existe, si no lo crea
        db_dir = "db"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        while True:
            # Leer un frame desde la cámara
            ret, frame = cap.read()

            # Mostrar el frame en una ventana
            cv2.imshow('Login Inteligente', frame)

            # Esperar a que se presione la tecla 'Esc' para salir
            if cv2.waitKey(1) == 27:
                break

        # Guardar la imagen capturada con el nombre del usuario
        img_path_db = os.path.join(db_dir, f"{nombre_usuario}_facial.jpg")
        cv2.imwrite(img_path_db, frame)

        # Liberar los recursos de la cámara y cerrar la ventana
        cap.release()
        cv2.destroyAllWindows()

        # Actualizar las entradas de usuario y contraseña
        self.usuario_entrada2.delete(0, END)
        self.contra_entrada2.delete(0, END)

        # Pedir al usuario que seleccione el segundo archivo de audio
        audio_path2 = filedialog.askopenfilename(title="Seleccione el segundo archivo de audio",
                                                    filetypes=[("Archivos WAV", "*.wav")])

        # Comparar el audio capturado con el segundo archivo de audio seleccionado
        if audio_path2:
            # Obtener el primer archivo de audio capturado
          
            nombre_usuario = self.usuario.get()
            
            primer_audio_path = os.path.join(db_dir, f"{nombre_usuario}.wav")
            

            # Comparar los archivos de audio
            comparar_audios(primer_audio_path, audio_path2)

            # Mostrar un mensaje de éxito
            Label(self.pantalla2, text="Comparación de Audio Exitosa", fg="green", font=("Calibri", 11)).pack()

        else:
            Label(self.pantalla2, text="Error: No se seleccionó el segundo archivo de audio", fg="red",
                    font=("Calibri", 11)).pack()

        # Mostrar un mensaje de éxito
        Label(self.pantalla2, text="Inicio de Sesión Inteligente Exitoso", fg="green", font=("Calibri", 11)).pack()

        # Procesar la imagen para mostrar las caras detectadas
        pixeles = pyplot.imread(img_path_db)
        caras = detector.detect_faces(pixeles)
        self.mostrar_caras_detectadas(img_path_db, caras)

    def mostrar_caras_detectadas(self, img, lista_resultados):
        # Cargar la imagen y mostrar las caras detectadas
        # data = pyplot.imread(img)

        # for i in range(len(lista_resultados)):
        # x1, y1, ancho, alto = lista_resultados[i]['box']
        # x2, y2 = x1 + ancho, y1 + alto

        # Mostrar la cara en una ventana
        # pyplot.subplot(1, len(lista_resultados), i + 1)
        # pyplot.axis('off')
        # pyplot.imshow(data[y1:y2, x1:x2])

        # Mostrar la ventana con las caras detectadas
        # pyplot.show()

        # Cerrar la ventana de inicio de sesión
        self.app.cerrar_ventana(self.pantalla2)

        # Mostrar la página principal
        self.app.mostrar_pagina_principal(self.usuario.get())