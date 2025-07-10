import pyautogui
import threading
import time
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os
import winsound
import subprocess

# Tempo entre movimentos (em segundos)
INTERVALO_MIN = 270  # 4.5 minutos
INTERVALO_MAX = 360  # 6 minutos

# Controle do bot
ativo = False
sons_ativos = True

# Funções novas para animações
def animar_botao(botao, cor_animada, cor_original):
    botao.config(bg=cor_animada, fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
    botao.update()
    root.after(150, lambda: botao.config(bg=cor_original, fg="white", relief="flat", font=("Segoe UI", 10, "bold")))

def mexer_mouse():
    while True:
        if ativo:
            x_move = random.choice([-2, -1, 1, 2])
            y_move = random.choice([-2, -1, 1, 2])
            pyautogui.move(x_move, y_move, duration=0.1)

            intervalo = random.randint(INTERVALO_MIN, INTERVALO_MAX)
            tempo_passado = 0
            while tempo_passado < intervalo:
                if not ativo:
                    break
                time.sleep(0.1)
                tempo_passado += 0.1
        else:
            time.sleep(0.5)

def escrever_produtivo():
    while True:
        if ativo:
            pyautogui.typewrite("produtivo ", interval=0.2)
            time.sleep(3)
        else:
            time.sleep(0.5)

def iniciar_bot():
    global ativo
    ativo = True
    status_var.set("Status: ATIVADO")
    if sons_ativos:
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
    animar_botao(start_button, "#6fe36f", "#4CAF50")
    subprocess.Popen("notepad.exe")
    time.sleep(2.5)
    pyautogui.hotkey('win', 'up')  # Maximiza a janela
    time.sleep(0.5)
    pyautogui.click(x=600, y=400)  # Clica no centro da janela do Bloco de Notas (ajuste se necessário)

def parar_bot():
    global ativo
    ativo = False
    status_var.set("Status: DESATIVADO")
    if sons_ativos:
        winsound.MessageBeep(winsound.MB_ICONHAND)
    animar_botao(stop_button, "#ff8a65", "#F44336")

def sair():
    if messagebox.askokcancel("Sair", "Tem certeza que quer sair?"):
        root.destroy()

def abrir_tela_loading():
    loading = tk.Toplevel()
    loading.title("Procastinator™ - Iniciando...")
    loading.geometry("300x150")
    loading.configure(bg="#2b2b2b")
    loading.resizable(False, False)
    label = tk.Label(loading, text="Carregando o poder da preguiça...", font=("Segoe UI", 10), bg="#2b2b2b", fg="white")
    label.pack(pady=10)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Horizontal.TProgressbar", troughcolor='#3c3f41', background='#4CAF50')

    progress = ttk.Progressbar(loading, orient=tk.HORIZONTAL, length=200, mode='determinate', style="Horizontal.TProgressbar")
    progress.pack(pady=10)

    loading.update()
    for i in range(0, 101, 5):
        progress['value'] = i
        loading.update_idletasks()
        time.sleep(0.1)

    loading.destroy()

def abrir_tela_configuracoes():
    config = tk.Toplevel()
    config.title("Configurações")
    config.geometry("300x250")
    config.configure(bg="#2b2b2b")

    global INTERVALO_MIN, INTERVALO_MAX, sons_ativos

    tk.Label(config, text="Tempo Mínimo (s):", bg="#2b2b2b", fg="white").pack(pady=(10,0))
    min_entry = tk.Entry(config)
    min_entry.insert(0, str(INTERVALO_MIN))
    min_entry.pack(pady=5)

    tk.Label(config, text="Tempo Máximo (s):", bg="#2b2b2b", fg="white").pack(pady=(10,0))
    max_entry = tk.Entry(config)
    max_entry.insert(0, str(INTERVALO_MAX))
    max_entry.pack(pady=5)

    sons_var = tk.IntVar(value=1 if sons_ativos else 0)
    sons_check = tk.Checkbutton(config, text="Ativar sons", variable=sons_var, bg="#2b2b2b", fg="white", selectcolor="#2b2b2b")
    sons_check.pack(pady=10)

    def salvar_config():
        global INTERVALO_MIN, INTERVALO_MAX, sons_ativos
        try:
            INTERVALO_MIN = int(min_entry.get())
            INTERVALO_MAX = int(max_entry.get())
            sons_ativos = bool(sons_var.get())
            messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
            config.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Insira apenas números inteiros para os tempos.")

    salvar_button = tk.Button(config, text="Salvar", command=salvar_config, width=15, bg="#4CAF50", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
    salvar_button.pack(pady=10)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def abrir_tela_boas_vindas():
    tela_bv = tk.Toplevel()
    tela_bv.title("Procastinator™ - Bem-vindo")
    tela_bv.geometry("400x300")
    tela_bv.configure(bg="#2b2b2b")
    tela_bv.resizable(False, False)

    texto = (
        "Bem-vindo ao Procastinator™!\n\n"
        "Produto da GnomaLabs™\n\n"
        "Este software é recreativo e o usuário é responsável pelo uso."
    )
    label = tk.Label(
        tela_bv, text=texto, font=("Segoe UI", 10),
        bg="#2b2b2b", fg="white", justify="center", wraplength=360
    )
    label.pack(pady=20, padx=20)

    def continuar():
        tela_bv.destroy()

    botao_continuar = tk.Button(
        tela_bv, text="Continuar", command=continuar,
        width=15, bg="#4CAF50", fg="white",
        relief="flat", font=("Segoe UI", 10, "bold")
    )
    botao_continuar.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal durante o loading

    abrir_tela_loading()

    root.deiconify()  # Mostra a janela principal depois do loading
    root.title("Procastinator™")
    root.geometry("400x450")
    root.configure(bg="#2b2b2b")
    root.resizable(False, False)

    abrir_tela_boas_vindas()

    titulo_label = tk.Label(root, text="Procastinator™ – Controle de Presença", font=("Segoe UI", 16, "bold"), bg="#2b2b2b", fg="white")
    titulo_label.pack(pady=(10, 5))

    # Adiciona logo no topo
    try:
        logo_path = resource_path("logo.png")
        imagem = Image.open(logo_path)
        imagem = imagem.resize((80, 80))
        logo = ImageTk.PhotoImage(imagem)
        logo_label = tk.Label(root, image=logo, bg="#2b2b2b")
        logo_label.image = logo  # mantém uma referência
        logo_label.pack(pady=5)
    except Exception as e:
        print("Logo não carregado:", e)

    status_var = tk.StringVar()
    status_var.set("Status: DESATIVADO")

    status_label = tk.Label(root, textvariable=status_var, font=("Segoe UI", 14, "bold"), bg="#2b2b2b", fg="white")
    status_label.pack(pady=10)

    botoes_frame = tk.Frame(root, bg="#2b2b2b")
    botoes_frame.pack(pady=10)

    start_button = tk.Button(botoes_frame, text="Iniciar", command=iniciar_bot, width=15, bg="#4CAF50", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
    start_button.pack(pady=5)

    stop_button = tk.Button(botoes_frame, text="Parar", command=parar_bot, width=15, bg="#F44336", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
    stop_button.pack(pady=5)

    config_button = tk.Button(botoes_frame, text="Configurações", command=abrir_tela_configuracoes, width=15, bg="#FFA726", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
    config_button.pack(pady=5)

    sair_button = tk.Button(botoes_frame, text="Sair", command=sair, width=15, bg="#607d8b", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
    sair_button.pack(pady=5)

    threading.Thread(target=mexer_mouse, daemon=True).start()
    threading.Thread(target=escrever_produtivo, daemon=True).start()

    root.protocol("WM_DELETE_WINDOW", sair)
    root.mainloop()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  