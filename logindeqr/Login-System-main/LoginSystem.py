import tkinter as tk
from tkinter import *
import os
import qrcode
import mysql.connector
import credenciales
def conectar():
    conexion = mysql.connector.connect(**credenciales.get_credenciales())
    cursor = conexion.cursor()
    return conexion, cursor

def cerrar(conexion, cursor):
    conexion.commit()
    cursor.close()
    conexion.close()
def register_user():
    username_info = username.get()
    password_info = password.get()

    conexion, cursor = conectar()

    if not os.path.exists(USERS_DIRECTORY):
        os.makedirs(USERS_DIRECTORY)

    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    user_data = (username_info, password_info)
    cursor.execute(insert_query, user_data)

    cerrar(conexion, cursor)

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registro Exitoso", fg="green").pack()

    # Genera y muestra el código QR
    qr_file_path = generate_qr_code(username_info)
    qr_label = Label(register_screen, text="Código QR:")
    qr_label.pack()
    qr_image = PhotoImage(file=qr_file_path)
    qr_label.config(image=qr_image)
    qr_label.image = qr_image

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    conexion, cursor = conectar()

    # Verifica si el usuario y la contraseña coinciden en la base de datos
    select_query = "SELECT * FROM estudiantes WHERE username = %s AND password = %s"
    user_data = (username1, password1)
    cursor.execute(select_query, user_data)
    result = cursor.fetchone()

    cerrar(conexion, cursor)

    if result:
        login_success(username1)
    else:
        password_not_recognised()
register_screen = None

def main_acc():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x260")
    main_screen.title("Main")
    Label(text="Inicia sesion o registrate", bg="#b1abf1", fg="white",
          width="300", height="2", font=("Calibri", 13)).pack(padx=20, pady=23)
    Button(text="Iniciar Sesion", height="2", width="15", fg="#c0ecc0", command=login).pack(padx=1, pady=20)
    Button(text="Registrarse", height="2", width="15", fg="#D8BFD8", command=register).pack(padx=1, pady=5)
    main_screen.mainloop()

# Directorios donde se guardarán los usuarios y los códigos QR
USERS_DIRECTORY = "users"
QR_DIRECTORY = "usersqr"


def get_user_file_path(username):
    # Construye la ruta completa del archivo del usuario
    return os.path.join(USERS_DIRECTORY, f"{username}.txt")

def get_qr_file_path(username):
    # Construye la ruta completa del archivo del código QR
    return os.path.join(QR_DIRECTORY, f"{username}_qr.png")

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("320x350")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Ingrese sus datos", bg="#D8BFD8", fg="black",
          width="300", height="2", font=("Calibri", 13)).pack(padx=20, pady=23)
    Label(register_screen, text="").pack()

    unLabel = Label(register_screen, text="Nombre", fg="black", bg="#D8BFD8")
    unLabel.pack(pady=5)

    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()

    passLabel = Label(register_screen, text="Contraseña", fg="black", bg="#D8BFD8")
    passLabel.pack(pady=5)

    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()

    Label(register_screen, text="").pack()
    Button(register_screen, text="Registrarse", width=10, height=1, fg="black", command=register_user).pack()

def generate_qr_code(username):
    # Genera un código QR con el nombre de usuario
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(username)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Verifica si el directorio de códigos QR existe, si no, lo crea
    if not os.path.exists(QR_DIRECTORY):
        os.makedirs(QR_DIRECTORY)

    # Guarda el código QR en un archivo de imagen
    qr_file_path = get_qr_file_path(username)
    img.save(qr_file_path)
    return qr_file_path

def register_user():
    username_info = username.get()
    password_info = password.get()

    conexion, cursor = conectar()

    # Verifica si el directorio de usuarios existe, si no, lo crea
    if not os.path.exists(USERS_DIRECTORY):
        os.makedirs(USERS_DIRECTORY)

    # Inserta el nuevo usuario en la base de datos
    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    user_data = (username_info, password_info)
    cursor.execute(insert_query, user_data)

    cerrar(conexion, cursor)

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registro Exitoso", fg="green").pack()

    # Genera y muestra el código QR
    qr_file_path = generate_qr_code(username_info)
    qr_label = Label(register_screen, text="Código QR:")
    qr_label.pack()
    qr_image = PhotoImage(file=qr_file_path)
    qr_label.config(image=qr_image)
    qr_label.image = qr_image
def user_dashboard(username):
    global dashboard_screen
    dashboard_screen = Toplevel(main_screen)
    dashboard_screen.title(f"{username}'s Dashboard")
    dashboard_screen.geometry("300x300")

    Label(dashboard_screen, text=f"¡Bienvenido, {username}!", font=("Calibri", 14)).pack(pady=20)

    # Muestra el código QR del usuario
    qr_file_path = get_qr_file_path(username)
    qr_label = Label(dashboard_screen, text="Tu Código QR:")
    qr_label.pack()
    qr_image = PhotoImage(file=qr_file_path)
    qr_label.config(image=qr_image)
    qr_label.image = qr_image

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("320x350")
    Label(login_screen, text="Ingrese sus datos", bg="#c0ecc0", fg="black",
          width="300", height="2", font=("Calibri", 13)).pack(padx=20, pady=23)
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Nombre", fg="black", bg="#c0ecc0").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack(pady=5)

    Label(login_screen, text="").pack()
    Label(login_screen, text="Contraseña", fg="black", bg="#c0ecc0").pack(pady=5)

    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()

    Label(login_screen, text="").pack()
    Button(login_screen, text="Iniciar Sesion", width=10, fg="black", height=1, command=login_verify).pack()

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    conexion, cursor = conectar()

    # Verifica si el usuario y la contraseña coinciden en la base de datos
    select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
    user_data = (username1, password1)
    cursor.execute(select_query, user_data)
    result = cursor.fetchone()

    cerrar(conexion, cursor)

    if result:
        login_success(username1)
    else:
        password_not_recognised()


def login_success(username):
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Acceso Existoso").pack()
    Button(login_success_screen, text="OK", command=lambda: user_dashboard(username)).pack()

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("ERROR")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Contraseña Inválida").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("ERROR")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, fg="red", text="Usuario No Encontrado").pack(pady=20)
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

def delete_login_success():
    login_success_screen.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

if __name__ == "__main__":
    main_acc()

