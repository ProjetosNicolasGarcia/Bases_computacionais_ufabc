import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variáveis
cpu_vals, ram_vals, disk_vals = [], [], []
upload_vals, download_vals = [], []
times = []

FILENAME = "log_hardware.csv"

# Inicializa CSV
def init_csv():
    try:
        with open(FILENAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "CPU (%)", "RAM (%)", "Disco (%)", "Upload (KB/s)", "Download (KB/s)"])
    except FileExistsError:
        pass

init_csv()

# Inicia valores de rede
prev_net = psutil.net_io_counters()
prev_bytes_sent = prev_net.bytes_sent
prev_bytes_recv = prev_net.bytes_recv

# Atualiza dados e gráficos
def update_data(frame):
    global prev_bytes_sent, prev_bytes_recv

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    net = psutil.net_io_counters()
    upload = (net.bytes_sent - prev_bytes_sent) / 1024
    download = (net.bytes_recv - prev_bytes_recv) / 1024
    prev_bytes_sent = net.bytes_sent
    prev_bytes_recv = net.bytes_recv

    timestamp = datetime.now().strftime("%H:%M:%S")
    times.append(timestamp)
    cpu_vals.append(cpu)
    ram_vals.append(ram)
    disk_vals.append(disk)
    upload_vals.append(upload)
    download_vals.append(download)

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu, ram, disk, upload, download])

    max_len = 30
    if len(times) > max_len:
        times.pop(0)
        cpu_vals.pop(0)
        ram_vals.pop(0)
        disk_vals.pop(0)
        upload_vals.pop(0)
        download_vals.pop(0)

    fig.patch.set_facecolor("#1e2a38")
    plt.subplots_adjust(hspace=1)  

    # Limpa e configura os gráficos
    ylabels = ["CPU (%)", "RAM (%)", "Disco (%)", "Rede (KB/s)"]
    for i, ax in enumerate(axes):
        ax.clear()
        ax.set_facecolor("#1e2a38")
        ax.grid(color="#3a4a5a", linestyle='--', linewidth=0.5)
        ax.tick_params(axis='x', colors="#f0f0f0", rotation=45, labelsize=7 )
        ax.tick_params(axis='y', colors="#f0f0f0")
        ax.set_xlabel("Tempo", color="#f0f0f0")
        ax.set_ylabel(ylabels[i], color="#f0f0f0")

    # Plota os dados
    axes[0].plot(times, cpu_vals, label="CPU (%)", color="cyan", linewidth=2)
    axes[1].plot(times, ram_vals, label="RAM (%)", color="magenta", linewidth=2)
    axes[2].plot(times, disk_vals, label="Disco (%)", color="yellow", linewidth=2)
    axes[3].plot(times, upload_vals, label="Upload (KB/s)", color="orange", linewidth=2)
    axes[3].plot(times, download_vals, label="Download (KB/s)", color="green", linewidth=2)

    for ax in axes:
        ax.legend(facecolor="#243447", edgecolor="#243447", labelcolor="#f0f0f0")


# Atualiza rótulos superiores
def update_labels():
    global prev_bytes_sent, prev_bytes_recv

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    net = psutil.net_io_counters()
    upload = (net.bytes_sent - prev_bytes_sent) // 1024
    download = (net.bytes_recv - prev_bytes_recv) // 1024
    prev_bytes_sent = net.bytes_sent
    prev_bytes_recv = net.bytes_recv

    label_cpu.config(text=f"CPU: {cpu}%")
    label_ram.config(text=f"RAM: {ram}%")
    label_disk.config(text=f"Disco: {disk}%")
    label_network.config(text=f"Rede - Enviado: {upload} KB | Recebido: {download} KB")

    root.after(5000, update_labels)

# Interface
root = tk.Tk()
root.title("Monitor de Hardware")
root.geometry("1000x750")
root.configure(bg="#1e2a38")

# Estilos
style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background="#1e2a38", borderwidth=0)
style.configure("TNotebook.Tab", font=('Arial', 12, 'bold'), background="#243447", foreground="#f0f0f0", padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "#4fc3f7")], foreground=[("selected", "#000000")])
style.configure("BlueFrame.TFrame", background="#243447", borderwidth=2, relief="raised")
style.configure("InfoLabel.TLabel", font=("Arial", 16, "bold"), background="#243447", foreground="#f0f0f0", padding=10)
style.configure("TitleLabel.TLabel", font=("Arial", 20, "bold"), background="#1e2a38", foreground="#f0f0f0")

# Notebook com abas
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# Aba de monitoramento
aba_monitoramento = ttk.Frame(notebook, style="BlueFrame.TFrame")
notebook.add(aba_monitoramento, text="Monitoramento")

# Título
title_label = ttk.Label(aba_monitoramento, text="Monitor de Desempenho de Hardware", style="TitleLabel.TLabel")
title_label.pack(pady=10)

# Indicadores
frame_indicadores = ttk.Frame(aba_monitoramento, style="BlueFrame.TFrame", padding=20)
frame_indicadores.pack(fill=tk.X, padx=20, pady=10)

label_cpu = ttk.Label(frame_indicadores, text="CPU: -", style="InfoLabel.TLabel")
label_cpu.pack(side=tk.LEFT, padx=20)

label_ram = ttk.Label(frame_indicadores, text="RAM: -", style="InfoLabel.TLabel")
label_ram.pack(side=tk.LEFT, padx=20)

label_disk = ttk.Label(frame_indicadores, text="Disco: -", style="InfoLabel.TLabel")
label_disk.pack(side=tk.LEFT, padx=20)

label_network = ttk.Label(frame_indicadores, text="Rede: -", style="InfoLabel.TLabel")
label_network.pack(side=tk.LEFT, padx=20)

# Gráfico
frame_grafico = ttk.Frame(aba_monitoramento, style="BlueFrame.TFrame", padding=10)
frame_grafico.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

fig, axes = plt.subplots(4, 1, figsize=(10, 8))
canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

ani = FuncAnimation(fig, update_data, interval=1000)

# Aba de ajuda
frame_ajuda = ttk.Frame(notebook, style="BlueFrame.TFrame", padding=20)
notebook.add(frame_ajuda, text="Ajuda")

ajuda_text = """
CPU (Unidade Central de Processamento):
Considerada o cérebro do computador, é responsável por executar instruções e processar dados. Sua velocidade influencia diretamente o desempenho dos programas e do sistema como um todo.

RAM (Memória de Acesso Aleatório):
Armazena temporariamente as informações utilizadas pelos programas em execução. Quanto maior a capacidade de RAM, melhor o desempenho em multitarefas e na execução de aplicativos simultâneos.

Disco:
Responsável pelo armazenamento permanente de arquivos e programas. Um disco cheio ou com baixa velocidade de leitura e gravação pode impactar negativamente o desempenho do sistema.

Rede:
Indica o tráfego de dados enviados e recebidos pela máquina. É útil para identificar picos de uso da internet, o que pode ajudar a diagnosticar lentidão ou atividades em segundo plano.
"""

scrollbar = tk.Scrollbar(frame_ajuda)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_ajuda = tk.Text(frame_ajuda, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                     bg="#243447", fg="#f0f0f0", font=("Arial", 14, "bold"),
                     padx=20, pady=20, relief="flat", borderwidth=0)
text_ajuda.insert(tk.END, ajuda_text)
text_ajuda.config(state=tk.DISABLED)
text_ajuda.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=text_ajuda.yview)

# Execução
if __name__ == "__main__":
    update_labels()
    root.mainloop()
