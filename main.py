from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN


# Funciones
def centrar_ventana(ventana, ancho, alto):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla / 2) - (ancho / 2)
    y = (alto_pantalla / 2) - (alto / 2)
    ventana.geometry(f'{ancho}x{alto}+{int(x)}+{int(y)}')

def mostrar_pagina_principal(usuario):
    global pagina_principal
    if pagina_principal:
        # Enfoca la ventana existente si ya está abierta
        pagina_principal.focus()
    else:
        # Crea la nueva ventana de la página principal
        pagina_principal = Toplevel(pantalla)
        pagina_principal.title("Página Principal")
        pagina_principal.geometry("300x250")
        centrar_ventana(pagina_principal, 300, 250)
        Label(pagina_principal, text=f"Bienvenido, {usuario}!", font=("Calibri", 14)).pack()
        Button(pagina_principal, text="Cerrar Sesión", command=cerrar_sesion).pack()


def cerrar_ventana(ventana):
    ventana.destroy()


def registrar_usuario():
    usuario_info = usuario.get()
    contra_info = contra.get()
    archivo = open(usuario_info, "w")
    archivo.write(usuario_info + "\n")
    archivo.write(contra_info)
    archivo.close()
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Registro Convencional Exitoso", fg="green", font=("Calibri", 11)).pack()

def registro():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1


    pantalla1 = Toplevel(pantalla)
    pantalla1.title("Registro")
    pantalla1.geometry("300x250")

    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text="Registro facial: debe asignar un usuario:").pack()
    Label(pantalla1, text="Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text="").pack()
    Label(pantalla1, text="Usuario * ").pack()
    usuario_entrada = Entry(pantalla1, textvariable=usuario)
    usuario_entrada.pack()
    Label(pantalla1, text="Contraseña * ").pack()
    contra_entrada = Entry(pantalla1, textvariable=contra)
    contra_entrada.pack()
    Label(pantalla1, text="").pack()
    Button(pantalla1, text="Registro Tradicional", width=15, height=1, command=registrar_usuario).pack()

    Label(pantalla1, text="").pack()
    Button(pantalla1, text="Registro Facial", width=15, height=1, command=registro_facial).pack()

def login():
    global pantalla2
    global verificacion_usuario
    global verificacion_contra
    global usuario_entrada2
    global contra_entrada2

    pantalla2 = Toplevel(pantalla)
    pantalla2.title("Login")
    pantalla2.geometry("300x250")
    centrar_ventana(pantalla2, 300, 250)

    Label(pantalla2, text="Login facial: debe asignar un usuario:").pack()
    Label(pantalla2, text="Login tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla2, text="").pack()

    verificacion_usuario = StringVar()
    verificacion_contra = StringVar()

    Label(pantalla2, text="Usuario * ").pack()
    usuario_entrada2 = Entry(pantalla2, textvariable=verificacion_usuario)
    usuario_entrada2.pack()
    Label(pantalla2, text="Contraseña * ").pack()
    contra_entrada2 = Entry(pantalla2, textvariable=verificacion_contra, show='*')  # Agregado el atributo show
    contra_entrada2.pack()
    Label(pantalla2, text="").pack()
    Button(pantalla2, text="Inicio de Sesion Tradicional", width=20, height=1, command=verificacion_login).pack()

    Label(pantalla2, text="").pack()
    Button(pantalla2, text="Inicio de Sesion Facial", width=20, height=1, command=login_facial).pack()

def registro_facial():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Registro Facial', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_img = usuario.get()
    cv2.imwrite(usuario_img + ".jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Registro Facial Exitoso", fg="green", font=("Calibri", 11)).pack()

    def reg_rostro(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(usuario_img + ".jpg", cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = usuario_img + ".jpg"
    pixeles = pyplot.imread(img)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    reg_rostro(img, caras)


def mostrar_pagina_principal(usuario):
    pagina_principal = Toplevel(pantalla)
    pagina_principal.title("Página Principal")
    pagina_principal.geometry("300x250")
    centrar_ventana(pagina_principal, 300, 250)
    Label(pagina_principal, text=f"Bienvenido, {usuario}!", font=("Calibri", 14)).pack()
    Button(pagina_principal, text="Cerrar Sesión", command=lambda: cerrar_ventana(pagina_principal)).pack()


def cerrar_sesion():
    global pagina_principal
    if pagina_principal:
        # Destruye la ventana de la página principal
        pagina_principal.destroy()
        pagina_principal = None


def verificacion_login():
    log_usuario = verificacion_usuario.get()
    log_contra = verificacion_contra.get()
    usuario_entrada2.delete(0, END)
    contra_entrada2.delete(0, END)
    lista_archivos = os.listdir()
    if log_usuario in lista_archivos:
        archivo2 = open(log_usuario, "r")
        verificacion = archivo2.read().splitlines()
        if log_contra in verificacion:
            print("Inicio de sesion exitoso")
            cerrar_ventana(pantalla2)
            mostrar_pagina_principal(log_usuario)
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(pantalla2, text="Contraseña Incorrecta", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()


def login_facial():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Login Facial', frame)
        if cv2.waitKey(1) == 27:
            break
    usuario_login = verificacion_usuario.get()
    cv2.imwrite(usuario_login + "LOG.jpg", frame)
    cap.release()
    cv2.destroyAllWindows()

    usuario_entrada2.delete(0, END)

    def log_rostro(imagen, lista_resultados):
        data = pyplot.imread(imagen)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(usuario_login + "LOG.jpg", cara_reg)
            return pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img_nombre = usuario_login + "LOG.jpg"
    pixeles = pyplot.imread(img_nombre)
    detector = MTCNN()
    caras = detector.detect_faces(pixeles)
    log_rostro(img_nombre, caras)

    def orb_sim(img1, img2):
        orb = cv2.ORB_create()
        kpa, descr_a = orb.detectAndCompute(img1, None)
        kpb, descr_b = orb.detectAndCompute(img2, None)
        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = comp.match(descr_a, descr_b)
        regiones_similares = [i for i in matches if i.distance < 70]
        if len(matches) == 0:
            return 0
        return len(regiones_similares) / len(matches)

    im_archivos = os.listdir()
    if usuario_login + ".jpg" in im_archivos:
        rostro_reg = cv2.imread(usuario_login + ".jpg", 0)
        rostro_log = cv2.imread(usuario_login + "LOG.jpg", 0)
        similitud = orb_sim(rostro_reg, rostro_log)
        if similitud >= 0.98:
            cerrar_ventana(pantalla2)
            mostrar_pagina_principal(usuario_login)
            print("Bienvenido al sistema usuario: ", usuario_login)
            print("Compatibilidad con la foto del registro: ", similitud)
        else:
            print("Rostro incorrecto, Cerifique su usuario")
            print("Compatibilidad con la foto del registro: ", similitud)
            Label(pantalla2, text="Incompatibilidad de rostros", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(pantalla2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()


def pantalla_principal():
    global pantalla
    pantalla = Tk()
    pantalla.geometry("600x650")
    pantalla.title("Login Multimodal")
    centrar_ventana(pantalla, 400, 350)
    Label(text="Login Inteligente", bg="gray", width="300", height="2",
          font=("Verdana", 13)).pack()
    Label(text="").pack()
    Button(text="Iniciar Sesion", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Registro", height="2", width="30", command=registro).pack()
    pantalla.mainloop()


# Código principal
pantalla_principal()
