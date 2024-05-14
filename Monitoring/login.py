import sqlite3
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

conn = sqlite3.connect('ameacas_ciberneticas.db')
conn.execute("PRAGMA journal_mode = WAL")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT UNIQUE, 
              password TEXT)''')


class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Login - Sistema de Monitoramento de Ameaças Cibernéticas")
        self.parent = parent

        self.username_label = tk.Label(self, text="Nome de Usuário:")
        self.username_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Senha:")
        self.password_entry = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Login", command=self.login)

        self.username_label.pack()
        self.username_entry.pack()
        self.password_label.pack()
        self.password_entry.pack()
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        c.execute("SELECT id FROM usuarios WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        if user:
            self.destroy()
            self.parent.open_main_window(user[0])
            self.parent.deiconify()  # Exibe a janela principal
        else:
            messagebox.showerror("Erro de Login", "Nome de usuário ou senha inválidos.")

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Monitoramento de Ameaças Cibernéticas")
        self.withdraw()  # Oculta a janela principal

    def open_main_window(self, user_id):
        user_label = tk.Label(self, text="Usuário Logado: {}".format(user_id))
        user_label.pack()

        # Chama o script gerenciador.py após o login bem-sucedido
        subprocess.Popen(["python", "gerenciador.py"])

        self.deiconify()  # Exibe a janela principal

if __name__ == "__main__":
    root = MainWindow()
    login_window = LoginWindow(root)
    root.mainloop()

    conn.close()
