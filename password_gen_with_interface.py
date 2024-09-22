import random
import string
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import xml.etree.ElementTree as ET
from fpdf import FPDF
import os
import pyperclip  # Biblioteca para copiar texto para a área de transferência

# Função para gerar a senha
def generate_password(length, use_digits, use_uppercase, use_lowercase, use_special):
    alphabet = ''
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_lowercase:
        alphabet += string.ascii_lowercase
    if use_digits:
        alphabet += string.digits
    if use_special:
        alphabet += string.punctuation
    
    if not alphabet:
        messagebox.showwarning("Aviso", "Você precisa selecionar pelo menos uma opção!")
        return None

    password = ''.join(random.choice(alphabet) for _ in range(length))
    return password

# Função para exportar senha para XML
def export_to_xml(password, filename):
    root = ET.Element("password_data")
    ET.SubElement(root, "password").text = password
    
    tree = ET.ElementTree(root)
    with open(filename + ".xml", "wb") as files:
        tree.write(files)

# Função para exportar senha para PDF
def export_to_pdf(password, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Senha Gerada:", ln=True, align='C')
    pdf.cell(200, 10, txt=password, ln=True, align='C')
    
    pdf.output(filename + ".pdf")

# Função para salvar os arquivos
def save_password(password):
    user_filename = filename_entry.get()
    if not user_filename:
        messagebox.showerror("Erro", "Por favor, insira um nome para o arquivo.")
        return
    
    # Corrigir o caminho da pasta Documentos
    documents_path = os.path.join(os.path.expanduser("~"), "Documentos")
    
    # Verificar se a pasta Documentos existe, caso contrário, criar
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)

    # Criar o nome do arquivo com base no nome fornecido pelo usuário
    filename = os.path.join(documents_path, f"senha_{user_filename}")

    # Exportando como XML e PDF
    export_to_xml(password, filename)
    export_to_pdf(password, filename)
    
    messagebox.showinfo("Sucesso", f"Arquivos salvos em: {documents_path}")

# Função principal de gerar senha e exibir
def generate_password_and_display():
    try:
        length = int(characters_entry.get())
        use_digits = digits_var.get()
        use_uppercase = uppercase_var.get()
        use_lowercase = lowercase_var.get()
        use_special = special_var.get()

        password = generate_password(length, use_digits, use_uppercase, use_lowercase, use_special)
        if password:
            # Exibir a senha gerada na interface em um Label
            password_label.config(text=f"Senha Gerada: {password}")
            # Ativar o botão de copiar
            copy_button.config(state=tk.NORMAL)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de caracteres.")

# Função para copiar a senha gerada
def copy_password():
    password = password_label.cget("text").replace("Senha Gerada: ", "")
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Sucesso", "Senha copiada para a área de transferência!")

# Configuração da janela principal
root = tk.Tk()
root.title("Gerador de Senha")
root.geometry("400x400")

# Widgets para a interface
tk.Label(root, text="Quantos caracteres são necessários?").pack(pady=10)
characters_entry = tk.Entry(root)
characters_entry.pack()

digits_var = tk.BooleanVar()
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
special_var = tk.BooleanVar()

tk.Checkbutton(root, text="Incluir Números", variable=digits_var).pack(anchor='w')
tk.Checkbutton(root, text="Incluir Letras Maiúsculas", variable=uppercase_var).pack(anchor='w')
tk.Checkbutton(root, text="Incluir Letras Minúsculas", variable=lowercase_var).pack(anchor='w')
tk.Checkbutton(root, text="Incluir Caracteres Especiais", variable=special_var).pack(anchor='w')

# Botão para gerar a senha
generate_button = tk.Button(root, text="Gerar Senha", command=generate_password_and_display)
generate_button.pack(pady=10)

# Label de exibição da senha gerada
password_label = tk.Label(root, text="Senha Gerada: ", font=('Helvetica', 12), wraplength=300)
password_label.pack(pady=5)

# Botão para copiar a senha gerada
copy_button = tk.Button(root, text="Copiar Senha", command=copy_password, state=tk.DISABLED)
copy_button.pack(pady=5)

# Campo para o nome do arquivo
tk.Label(root, text="Nome do arquivo:").pack(pady=10)
filename_entry = tk.Entry(root)
filename_entry.pack()

# Botão para salvar a senha como XML e PDF
save_button = tk.Button(root, text="Salvar Senha", command=lambda: save_password(password_label.cget("text").replace("Senha Gerada: ", "")))
save_button.pack(pady=20)

# Inicializa a interface
root.mainloop()
