import csv
from datetime import datetime
import smtplib
import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# variáveis

cpu_vals = []
ram_vals = []
times = []

FILENAME = "log_hardware.csv"


# funções do log


def init_csv():
    """
    Inicializa o arquivo CSV para armazenar os logs de uso.
    """
    try:
        with open(FILENAME, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['hora', 'cpu_porcentagem', 'ram_porcentagem', 'disco_porcentagem'])
    except FileExistsError:
        pass

def log_status():
    """
    Faz a medição do uso de CPU, RAM e Disco e salva no CSV.
    """
    hora = datetime.now()
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage('/').percent

    with open(FILENAME, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([hora.isoformat(), cpu, ram, disco])

   
    return hora, cpu, ram, disco


# funções da interface

def animate(i):
    """
    Chama a animação do Matplotlib para atualizar o gráfico em tempo real.
    """
    hora, cpu, ram, _ = log_status() 
    times.append(hora.strftime("%H:%M:%S"))
    cpu_vals.append(cpu)
    ram_vals.append(ram)

    times_display = times[-20:]
    cpu_display = cpu_vals[-20:]
    ram_display = ram_vals[-20:]

    ax.clear()
    ax.set_facecolor("#1e2a38")
    fig.patch.set_facecolor("#1e2a38")

    ax.plot(times_display, cpu_display, label='CPU %', color="#4fc3f7", linewidth=2)
    ax.plot(times_display, ram_display, label='RAM %', color="#81d4fa", linewidth=2)
    ax.set_ylabel('% Uso', color="#f0f0f0")
    ax.set_xlabel('Hora', color="#f0f0f0")
    ax.set_title('Monitor em Tempo Real', color="#f0f0f0", fontsize=14, weight='bold')
    ax.legend(facecolor="#243447", edgecolor="#243447", labelcolor="#f0f0f0")
    ax.tick_params(axis='x', colors="#f0f0f0", rotation=45)
    ax.tick_params(axis='y', colors="#f0f0f0")
    ax.grid(color="#3a4a5a", linestyle='--', linewidth=0.5)
    plt.tight_layout()

def update_labels():
    """
    Atualiza os valores na interface a cada 5 segundos.
    """
    _, cpu, ram, disco = log_status()  

    label_cpu.config(text=f"CPU: {cpu}%")
    label_ram.config(text=f"RAM: {ram}%")
    label_disk.config(text=f"DISCO: {disco}%")

    if cpu > 90:
        send_alert_email(cpu)

    root.after(5000, update_labels)


#  config da interface no tkinter

root = tk.Tk()
root.title("Monitor de Hardware")
root.geometry("1000x700")
root.configure(bg="#1e2a38")

style = ttk.Style()
style.theme_use('clam')
style.configure("BlueFrame.TFrame", background="#243447", borderwidth=2, relief="raised")
style.configure("InfoLabel.TLabel", font=("Arial", 16, "bold"), background="#243447", foreground="#f0f0f0", padding=10)
style.configure("TitleLabel.TLabel", font=("Arial", 20, "bold"), background="#1e2a38", foreground="#f0f0f0")

# título
title_label = ttk.Label(root, text="Monitor de Desempenho de Hardware", style="TitleLabel.TLabel")
title_label.pack(pady=10)

# indicadores
frame_indicadores = ttk.Frame(root, style="BlueFrame.TFrame", padding=20)
frame_indicadores.pack(fill=tk.X, padx=20, pady=10)

label_cpu = ttk.Label(frame_indicadores, text="CPU: -", style="InfoLabel.TLabel")
label_cpu.pack(side=tk.LEFT, padx=20)

label_ram = ttk.Label(frame_indicadores, text="RAM: -", style="InfoLabel.TLabel")
label_ram.pack(side=tk.LEFT, padx=20)

label_disk = ttk.Label(frame_indicadores, text="DISCO: -", style="InfoLabel.TLabel")
label_disk.pack(side=tk.LEFT, padx=20)

# gráfico
frame_grafico = ttk.Frame(root, style="BlueFrame.TFrame", padding=10)
frame_grafico.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Configs dos gráficos do Matplotlib
fig, ax = plt.subplots(figsize=(10,5))
fig.patch.set_facecolor("#1e2a38")
ax.set_facecolor("#1e2a38")
ax.tick_params(axis='x', colors="#f0f0f0")
ax.tick_params(axis='y', colors="#f0f0f0")
ax.title.set_color("#f0f0f0")

canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


ani = FuncAnimation(fig, animate, interval=5000)

# loop

if __name__ == "__main__":
    init_csv()
    update_labels()
    root.mainloop()
