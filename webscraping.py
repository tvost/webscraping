import os
import requests
import tkinter as tk
from tkhtmlview import HTMLLabel
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tkinter import ttk

ua = UserAgent()
headers = {'User-Agent': ua.random}

def extract_and_save_content(url, folder_name):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrair conteúdo HTML
        html_content = soup.prettify()

        # Extrair conteúdo JavaScript
        script_tags = soup.find_all('script')
        js_content = '\n'.join(tag.text for tag in script_tags)

        page_name = url.split('/')[-1].split('.')[0]
        os.makedirs(folder_name, exist_ok=True)

        # Salvar conteúdo HTML
        with open(f'{folder_name}/{page_name}_html.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

        # Salvar conteúdo JavaScript
        with open(f'{folder_name}/{page_name}_js.js', 'w', encoding='utf-8') as file:
            file.write(js_content)

        print(f'Conteúdo da página {url} (HTML e JavaScript) salvo com sucesso.')

    except requests.exceptions.RequestException as e:
        print(f'Erro ao fazer a requisição para {url}: {e}')

# Função chamada quando o botão é pressionado
def on_submit():
    selected_url = url_var.get()
    selected_folder_name = folder_name_var.get()

    extract_and_save_content(selected_url, selected_folder_name)

# Criação da interface gráfica
root = tk.Tk()
root.title("Web Scraping Interface")

# Criação de variáveis para armazenar os dados inseridos pelo usuário
url_var = tk.StringVar()
folder_name_var = tk.StringVar()

# Configuração do estilo
style = ttk.Style()
style.configure('TLabel', font=('Arial', 12), background='black', foreground='white')
style.configure('TButton', font=('Arial', 12), background='black', foreground='white')
style.configure('TEntry', font=('Arial', 12), background='gray', foreground='white')

# Labels e Entradas para cada campo
tk.Label(root, text="URL:").grid(row=0, column=0, sticky="w", pady=10)
url_entry = tk.Entry(root, textvariable=url_var, width=40)
url_entry.grid(row=0, column=1, columnspan=2, pady=10)

tk.Label(root, text="Pasta:").grid(row=1, column=0, sticky="w", pady=10)
folder_name_entry = tk.Entry(root, textvariable=folder_name_var, width=40)
folder_name_entry.grid(row=1, column=1, columnspan=2, pady=10)

# Botão de envio
submit_button = tk.Button(root, text="Extrair e Salvar", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=3, pady=20)

# Adicionando o componente WebView para exibir o conteúdo HTML
html_label = HTMLLabel(root, html='')
html_label.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()