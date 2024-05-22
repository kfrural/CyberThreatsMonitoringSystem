import sqlite3
import tkinter as tk
from datetime import datetime
import csv
import matplotlib.pyplot as plt

# Conexão com o banco de dados
conn = sqlite3.connect('ameacas_ciberneticas.db')
conn.execute("PRAGMA journal_mode = WAL")
c = conn.cursor()

# Criação das tabelas
c.execute('''CREATE TABLE IF NOT EXISTS ameacas
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              tipo TEXT, 
              descricao TEXT, 
              data_deteccao TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              nome TEXT, 
              username TEXT UNIQUE, 
              password TEXT)''')

# Funções para manipulação de ameaças
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

def fazer_login():
    username = username_login_entry.get()
    password = password_login_entry.get()

    c.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = c.fetchone()

    if usuario:
        print(f"Bem-vindo, {usuario[1]}!")
        login_frame.pack_forget()  # Esconde o frame de login
        registrar_frame.pack()  # Mostra o frame de registro de ameaças
    else:
        print("username ou password incorretos.")

    username_login_entry.delete(0, tk.END)
    password_login_entry.delete(0, tk.END)

def exportar_csv():
    filename = "ameacas.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['ID', 'Tipo', 'Descrição', 'Data de Detecção'])
        
        c.execute("SELECT id, tipo, descricao, data_deteccao FROM ameacas")
        rows = c.fetchall()
        for row in rows:
            csv_writer.writerow(row)
    
    print(f"Dados exportados para {filename} com sucesso.")

def gerar_graficos():
    c.execute("SELECT tipo, COUNT(*) FROM ameacas GROUP BY tipo")
    data = c.fetchall()

    if data:
        tipos, contagens = zip(*data)

        plt.figure(figsize=(10, 6))
        plt.bar(tipos, contagens, color='skyblue')
        plt.xlabel('Tipo de Ameaça')
        plt.ylabel('Quantidade')
        plt.title('Quantidade de Ameaças por Tipo')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("Nenhum dado disponível para gerar gráficos.")

# Interface gráfica
root = tk.Tk()
root.title("Sistema de Monitoramento de Ameaças Cibernéticas")

# Frame de login
login_frame = tk.Frame(root)
login_frame.pack()

username_login_label = tk.Label(login_frame, text="username:")
username_login_label.pack()
username_login_entry = tk.Entry(login_frame)
username_login_entry.pack()

password_login_label = tk.Label(login_frame, text="password:")
password_login_label.pack()
password_login_entry = tk.Entry(login_frame, show="*")
password_login_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=fazer_login)
login_button.pack()

# Frame de registro de ameaças
registrar_frame = tk.Frame(root)

# Widgets para adicionar ameaças
tipo_label = tk.Label(registrar_frame, text="Tipo de Ameaça:")
tipo_entry = tk.Entry(registrar_frame)
descricao_label = tk.Label(registrar_frame, text="Descrição:")
descricao_entry = tk.Entry(registrar_frame)
adicionar_button = tk.Button(registrar_frame, text="Adicionar Ameaça", command=adicionar_ameaca)

# Widgets para editar e excluir ameaças
editar_button = tk.Button(registrar_frame, text="Editar Ameaça", command=editar_ameaca)
excluir_button = tk.Button(registrar_frame, text="Excluir Ameaça", command=excluir_ameaca)

# Widgets para filtrar ameaças
filtro_label = tk.Label(registrar_frame, text="Filtrar por:")
tipo_filtro_label = tk.Label(registrar_frame, text="Tipo:")
tipo_filtro_entry = tk.Entry(registrar_frame)
descricao_filtro_label = tk.Label(registrar_frame, text="Descrição:")
descricao_filtro_entry = tk.Entry(registrar_frame)
data_filtro_label = tk.Label(registrar_frame, text="Data de Detecção:")
data_filtro_entry = tk.Entry(registrar_frame)
filtrar_button = tk.Button(registrar_frame, text="Filtrar", command=filtrar_ameacas)

# Label e Listbox para exibir Ameaças
ameacas_label = tk.Label(registrar_frame, text="Ameaças Detectadas:")
ameacas_listbox = tk.Listbox(registrar_frame, width=80)

# Botão para exportar dados para CSV
exportar_csv_button = tk.Button(registrar_frame, text="Exportar CSV", command=exportar_csv)

# Botão para gerar gráficos
gerar_graficos_button = tk.Button(registrar_frame, text="Gerar Gráficos", command=gerar_graficos)

# Grid Layout para o frame de registro de ameaças
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

exportar_csv_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)
gerar_graficos_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

conn.close()
