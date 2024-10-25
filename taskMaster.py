import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('task_manager.db')
cursor = conn.cursor()

# Criação da tabela de tarefas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        due_date TEXT,
        priority TEXT
    )
''')
conn.commit()
conn.close()

import tkinter as tk
from tkinter import messagebox
import sqlite3

# Funções de interação com o banco de dados
def add_task():
    description = entry_description.get()
    due_date = entry_due_date.get()

    if description:
        conn = sqlite3.connect('task_manager.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (description, due_date, priority) VALUES (?, ?, ?)', (description, due_date, ''))
        conn.commit()
        conn.close()
        display_tasks()
        entry_description.delete(0, tk.END)
        entry_due_date.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "A descrição da tarefa não pode estar vazia")

def display_tasks():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    rows = cursor.fetchall()
    conn.close()

    listbox_tasks.delete(0, tk.END)
    for row in rows:
        listbox_tasks.insert(tk.END, f"{row[1]} - {row[2]} - {row[3]}")

# Configuração da interface gráfica
window = tk.Tk()
window.title("Gerenciador de Tarefas Inteligente")

label_description = tk.Label(window, text="Descrição da Tarefa")
label_description.pack()
entry_description = tk.Entry(window, width=50)
entry_description.pack()

label_due_date = tk.Label(window, text="Data de Vencimento")
label_due_date.pack()
entry_due_date = tk.Entry(window, width=50)
entry_due_date.pack()

button_add = tk.Button(window, text="Adicionar Tarefa", command=add_task)
button_add.pack()

listbox_tasks = tk.Listbox(window, width=80, height=10)
listbox_tasks.pack()

display_tasks()
window.mainloop()

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# Dados de exemplo para treinamento (simulados)
data = [
    ('Pagar contas', 'Alta'),
    ('Estudar para a prova', 'Alta'),
    ('Comprar mantimentos', 'Média'),
    ('Limpar a casa', 'Baixa'),
    ('Enviar e-mails', 'Média')
]
descriptions, priorities = zip(*data)

# Transformação dos textos em vetores numéricos
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(descriptions)
y = priorities

# Treinamento do modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = MultinomialNB()
model.fit(X_train, y_train)

# Função para classificar uma nova tarefa
def classify_task(description):
    X_new = vectorizer.transform([description])
    predicted_priority = model.predict(X_new)
    return predicted_priority[0]

# Exemplo de uso
task_description = "Terminar o relatório"
print(f"Prioridade sugerida: {classify_task(task_description)}")
