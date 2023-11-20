from tkinter import Tk
from ventana_login import VentanaLogin

def main():
    pantalla = Tk()
    pantalla.geometry("600x650")
    pantalla.title("Login Multimodal")

    app = VentanaLogin(pantalla)
    app.pantalla_principal()

    pantalla.mainloop()

if __name__ == "__main__":
    main()
