import sqlite3
import tkinter as tk
from datetime import datetime

conn = sqlite3.connect('ameacas_ciberneticas.db')
conn.execute("PRAGMA journal_mode = WAL")
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

    c.execute("INSERT INTO ameacas (tipo, descricao, data_deteccao) VALUES (?, ?, ?)",
              (tipo, descricao, data_deteccao))
    conn.commit()

    tipo_entry.delete(0, tk.END)
    descricao_entry.delete(0, tk.END)
    atualizar_listbox()

def editar_ameaca():
    selected = ameacas_listbox.curselection()
    if selected:
        id = selected[0] + 1
        tipo = tipo_entry.get()
        descricao = descricao_entry.get()
        data_deteccao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        c.execute("UPDATE ameacas SET tipo=?, descricao=?, data_deteccao=? WHERE id=?",
                  (tipo, descricao, data_deteccao, id))
        conn.commit()

        tipo_entry.delete(0, tk.END)
        descricao_entry.delete(0, tk.END)
        atualizar_listbox()

def excluir_ameaca():
    selected = ameacas_listbox.curselection()
    if selected:
        id = selected[0] + 1
        c.execute("DELETE FROM ameacas WHERE id=?", (id,))
        conn.commit()
        atualizar_listbox()


def filtrar_ameacas():
    tipo_filtro = tipo_filtro_entry.get()
    descricao_filtro = descricao_filtro_entry.get()
    data_filtro = data_filtro_entry.get()

    query = "SELECT id, tipo, descricao, data_deteccao FROM ameacas"
    params = []

    if tipo_filtro:
        query += " WHERE tipo LIKE ?"
        params.append(f"%{tipo_filtro}%")
    if descricao_filtro:
        if params:
            query += " AND descricao LIKE ?"
        else:
            query += " WHERE descricao LIKE ?"
        params.append(f"%{descricao_filtro}%")
    if data_filtro:
        if params:
            query += " AND data_deteccao LIKE ?"
        else:
            query += " WHERE data_deteccao LIKE ?"
        params.append(f"%{data_filtro}%")

    c.execute(query, params)
    rows = c.fetchall()

    ameacas_listbox.delete(0, tk.END)
    for row in rows:
        ameacas_listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} ({row[3]})")

def atualizar_listbox():
    ameacas_listbox.delete(0, tk.END)
    c.execute("SELECT id, tipo, descricao, data_deteccao FROM ameacas")
    for row in c.fetchall():
        ameacas_listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} ({row[3]})")

root = tk.Tk()
root.title("Sistema de Monitoramento de Ameaças Cibernéticas")

# Labels e Entradas para Adicionar Ameaça
tipo_label = tk.Label(root, text="Tipo de Ameaça:")
tipo_entry = tk.Entry(root)
descricao_label = tk.Label(root, text="Descrição:")
descricao_entry = tk.Entry(root)
adicionar_button = tk.Button(root, text="Adicionar Ameaça", command=adicionar_ameaca)

# Botões para Editar e Excluir Ameaça
editar_button = tk.Button(root, text="Editar Ameaça", command=editar_ameaca)
excluir_button = tk.Button(root, text="Excluir Ameaça", command=excluir_ameaca)

# Labels e Entradas para Filtrar Ameaças
filtro_label = tk.Label(root, text="Filtrar por:")
tipo_filtro_label = tk.Label(root, text="Tipo:")
tipo_filtro_entry = tk.Entry(root)
descricao_filtro_label = tk.Label(root, text="Descrição:")
descricao_filtro_entry = tk.Entry(root)
data_filtro_label = tk.Label(root, text="Data de Detecção:")
data_filtro_entry = tk.Entry(root)
filtrar_button = tk.Button(root, text="Filtrar", command=filtrar_ameacas)

# Label e Listbox para exibir Ameaças
ameacas_label = tk.Label(root, text="Ameaças Detectadas:")
ameacas_listbox = tk.Listbox(root, width=80)

# Grid Layout
tipo_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
tipo_entry.grid(row=0, column=1, padx=10, pady=10)
descricao_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
descricao_entry.grid(row=1, column=1, padx=10, pady=10)
adicionar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

editar_button.grid(row=3, column=0, padx=10, pady=10)
excluir_button.grid(row=3, column=1, padx=10, pady=10)

filtro_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
tipo_filtro_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
tipo_filtro_entry.grid(row=5, column=1, padx=10, pady=10)
descricao_filtro_label.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
descricao_filtro_entry.grid(row=6, column=1, padx=10, pady=10)
data_filtro_label.grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)
data_filtro_entry.grid(row=7, column=1, padx=10, pady=10)
filtrar_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

ameacas_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)
ameacas_listbox.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

filtrar_ameacas()

root.mainloop()

conn.close()
