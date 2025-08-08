import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shutil
import matplotlib.dates as mdates

# Configuração de estilo
plt.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "legend.fontsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 300
})

#  Leitura dos dados 
df = pd.read_csv("log_hardware.csv", parse_dates=["Timestamp"])

# Gráfico: Variação de CPU e RAM
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Timestamp"], df["CPU (%)"], label="CPU (%)", color="#1f77b4", linewidth=2)
ax.plot(df["Timestamp"], df["RAM (%)"], label="RAM (%)", color="#2ca02c", linewidth=2)
ax.set_xlabel("Horário")
ax.set_ylabel("Uso (%)")
ax.set_title("Variação de CPU e RAM com a execução de programas")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig("grafico_cpu_ram.png", dpi=300)
plt.close()

# Gráfico: Disco e Rede 
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Timestamp"], df["Disco (%)"], label="Disco (%)", color="#9467bd", linewidth=2)
ax.plot(df["Timestamp"], df["Upload (KB/s)"], label="Upload (KB/s)", color="#ff7f0e", linewidth=2)
ax.plot(df["Timestamp"], df["Download (KB/s)"], label="Download (KB/s)", color="#d62728", linewidth=2)
ax.set_xlabel("Horário")
ax.set_ylabel("Atividade")
ax.set_title("Atividade de Disco e Rede durante execução de tarefas")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
fig.autofmt_xdate()
plt.tight_layout()
plt.savefig("grafico_disco_rede.png", dpi=300)
plt.close()

# Verificação do uso de disco
total, used, free = shutil.disk_usage("/")
percent_manual = (used / total) * 100
print(f"Uso de disco (calculado manualmente): {percent_manual:.2f}%")
print(f"Uso de disco (monitoramento): {df['Disco (%)'].iloc[-1]:.2f}%")

#  Mapa de calor das correlações
correlacoes = df.corr(numeric_only=True)

plt.figure(figsize=(8, 6))
sns.heatmap(correlacoes, annot=True, cmap="coolwarm", fmt=".2f", cbar_kws={"label": "Correlação"})
plt.title("Mapa de Correlação entre Indicadores de Desempenho")
plt.tight_layout()
plt.savefig("grafico_correlacao.png", dpi=300)
plt.close()

# Estatísticas descritivas 
estatisticas = df.describe().round(2)
print("\nEstatísticas descritivas:")
print(estatisticas)

# Salva em CSV
estatisticas.to_csv("estatisticas_descritivas.csv")
