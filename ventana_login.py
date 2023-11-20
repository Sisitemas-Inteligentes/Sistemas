from tkinter import Tk, Toplevel, StringVar, Entry, Button, Label
from tkinter import END
from registro_login import RegistroLogin

class VentanaLogin:
    def __init__(self, ventana):
        self.ventana = ventana
        self.pantalla1 = None
        self.pantalla2 = None
        self.pagina_principal = None

    def centrar_ventana(self, ancho, alto):
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla / 2) - (ancho / 2)
        y = (alto_pantalla / 2) - (alto / 2)
        self.ventana.geometry(f'{ancho}x{alto}+{int(x)}+{int(y)}')

    def mostrar_pagina_principal(self, usuario):
        self.pagina_principal = Toplevel(self.ventana)
        self.pagina_principal.title("Página Principal")
        self.pagina_principal.geometry("300x250")
        self.centrar_ventana(300, 250)
        Label(self.pagina_principal, text=f"Bienvenido, {usuario}!", font=("Calibri", 14)).pack()
        Button(self.pagina_principal, text="Cerrar Sesión", command=self.cerrar_sesion).pack()

    def cerrar_ventana(self, ventana):
        ventana.destroy()

    def cerrar_sesion(self):
        if self.pagina_principal:
            self.pagina_principal.destroy()
            self.pagina_principal = None

    def pantalla_principal(self):
        self.ventana.geometry("600x650")
        self.ventana.title("Login Multimodal")
        self.centrar_ventana(400, 350)
        Label(text="Login Inteligente", bg="gray", width="300", height="2", font=("Verdana", 13)).pack()
        Label(text="").pack()
        Button(text="Iniciar Sesion", height="2", width="30", command=self.login).pack()
        Label(text="").pack()
        Button(text="Registro", height="2", width="30", command=self.registro).pack()

    def registro(self):
        self.pantalla1 = RegistroLogin(self.ventana, self)
        self.pantalla1.mostrar_ventana_registro()

    def login(self):
        self.pantalla2 = RegistroLogin(self.ventana, self)
        self.pantalla2.mostrar_ventana_login()
