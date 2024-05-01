import sqlite3
import tkinter as tk
from datetime import datetime

conn = sqlite3.connect('ameacas_ciberneticas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS ameacas
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              tipo TEXT, 
              descricao TEXT, 
              data_deteccao TEXT)''')

def adicionar_ameaca():
    tipo = tipo_entry.get()
    descricao = descricao_entry.get()
    data_deteccao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute("INSERT INTO ameacas (tipo, descricao, data_deteccao) VALUES (?, ?, ?)", (tipo, descricao, data_deteccao))
    conn.commit()
    
    tipo_entry.delete(0, tk.END)
    descricao_entry.delete(0, tk.END)
    atualizar_listbox()

def atualizar_listbox():
    ameacas_listbox.delete(0, tk.END)
    c.execute("SELECT tipo, descricao, data_deteccao FROM ameacas")
    for row in c.fetchall():
        ameacas_listbox.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]})")

root = tk.Tk()
root.title("Sistema de Monitoramento de Ameaças Cibernéticas")

tipo_label = tk.Label(root, text="Tipo de Ameaça:")
tipo_entry = tk.Entry(root)
descricao_label = tk.Label(root, text="Descrição:")
descricao_entry = tk.Entry(root)
adicionar_button = tk.Button(root, text="Adicionar Ameaça", command=adicionar_ameaca)
ameacas_label = tk.Label(root, text="Ameaças Detectadas:")
ameacas_listbox = tk.Listbox(root, width=80)

tipo_label.grid(row=0, column=0, padx=10, pady=10)
tipo_entry.grid(row=0, column=1, padx=10, pady=10)
descricao_label.grid(row=1, column=0, padx=10, pady=10)
descricao_entry.grid(row=1, column=1, padx=10, pady=10)
adicionar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
ameacas_label.grid(row=3, column=0, padx=10, pady=10)
ameacas_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

atualizar_listbox()

root.mainloop()

conn.close()
