"""
Actividad Formativa 4 - Señales y Sistemas (A)
Implementación y análisis de un sistema de modulación en amplitud (AM)

Autor: Luis Angel Chaires Contreras
Universidad Ciudadana de Nuevo León

Este script implementa un sistema de modulación en amplitud (AM),
analiza la señal en el dominio del tiempo y de la frecuencia, y evalúa
su desempeño bajo distintas condiciones de ruido y atenuación.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os

# Carpeta donde se guardan todas las gráficas generadas
CARPETA_SALIDA = "graficas"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. DEFINICIÓN DE LA SEÑAL DE ENTRADA (MENSAJE)
# ---------------------------------------------------------------------------
# Se define la señal de mensaje (información a transmitir) de baja
# frecuencia, y se establecen los parámetros generales del sistema.

fs = 100000          # Frecuencia de muestreo (Hz) - suficientemente alta
                     # para representar bien la portadora y sus armónicos
duracion = 0.02      # Duración de la simulación en segundos
t = np.arange(0, duracion, 1 / fs)

fm = 300             # Frecuencia de la señal mensaje (Hz)
Am = 1.0             # Amplitud de la señal mensaje
senal_mensaje = Am * np.sin(2 * np.pi * fm * t)

# ---------------------------------------------------------------------------
# 2. DEFINICIÓN DE LA PORTADORA DE ALTA FRECUENCIA
# ---------------------------------------------------------------------------
fc = 5000            # Frecuencia de la portadora (Hz)
Ac = 1.0             # Amplitud de la portadora
senal_portadora = Ac * np.cos(2 * np.pi * fc * t)

# ---------------------------------------------------------------------------
# 3. GRÁFICA DE LA SEÑAL DE ENTRADA (mensaje y portadora en el tiempo)
# ---------------------------------------------------------------------------
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t * 1000, senal_mensaje, color="tab:blue")
plt.title("Señal mensaje (baja frecuencia) - {} Hz".format(fm))
plt.xlabel("Tiempo (ms)")
plt.ylabel("Amplitud")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t * 1000, senal_portadora, color="tab:orange")
plt.title("Señal portadora (alta frecuencia) - {} Hz".format(fc))
plt.xlabel("Tiempo (ms)")
plt.ylabel("Amplitud")
plt.grid(True)

plt.tight_layout()
plt.savefig(f"{CARPETA_SALIDA}/01_senal_mensaje_portadora.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 4. MODULACIÓN EN AMPLITUD (AM)
# ---------------------------------------------------------------------------
# Se aplica la ecuación clásica de modulación AM con índice de modulación m:
#   s(t) = Ac * [1 + m * x(t)] * cos(2*pi*fc*t)
# donde x(t) es la señal mensaje normalizada.

m = 0.8  # Índice de modulación (0 < m <= 1 evita sobremodulación)
senal_modulada = Ac * (1 + m * senal_mensaje) * np.cos(2 * np.pi * fc * t)

plt.figure(figsize=(10, 4))
plt.plot(t * 1000, senal_modulada, color="tab:green", linewidth=0.8)
plt.plot(t * 1000, Ac * (1 + m * senal_mensaje), '--', color="black",
         linewidth=1, label="Envolvente")
plt.plot(t * 1000, -Ac * (1 + m * senal_mensaje), '--', color="black",
         linewidth=1)
plt.title(f"Señal modulada en AM (índice de modulación m = {m})")
plt.xlabel("Tiempo (ms)")
plt.ylabel("Amplitud")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{CARPETA_SALIDA}/02_senal_modulada_tiempo.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 5. ANÁLISIS EN EL DOMINIO DE LA FRECUENCIA (FFT)
# ---------------------------------------------------------------------------
def calcular_espectro(senal, fs):
    """Calcula la magnitud del espectro de una señal usando FFT."""
    n = len(senal)
    yf = fft(senal)
    xf = fftfreq(n, 1 / fs)
    # Solo la mitad positiva del espectro
    mitad = n // 2
    return xf[:mitad], (2.0 / n) * np.abs(yf[:mitad])

freq_mod, mag_mod = calcular_espectro(senal_modulada, fs)

plt.figure(figsize=(10, 4))
plt.plot(freq_mod, mag_mod, color="tab:purple")
plt.title("Espectro de frecuencia de la señal modulada en AM")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.xlim(0, fc + 3 * fm)
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{CARPETA_SALIDA}/03_espectro_senal_modulada.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 6. FUNCIONES AUXILIARES: RUIDO, ATENUACIÓN Y SNR
# ---------------------------------------------------------------------------
def agregar_ruido(senal, snr_db):
    """
    Agrega ruido blanco gaussiano a una señal para lograr
    una relación señal-a-ruido (SNR) objetivo, en dB.
    """
    potencia_senal = np.mean(senal ** 2)
    potencia_ruido = potencia_senal / (10 ** (snr_db / 10))
    ruido = np.random.normal(0, np.sqrt(potencia_ruido), len(senal))
    return senal + ruido

def calcular_snr(senal_original, senal_con_ruido):
    """Calcula la SNR real (dB) comparando señal limpia vs. señal ruidosa."""
    ruido = senal_con_ruido - senal_original
    potencia_senal = np.mean(senal_original ** 2)
    potencia_ruido = np.mean(ruido ** 2)
    if potencia_ruido == 0:
        return np.inf
    return 10 * np.log10(potencia_senal / potencia_ruido)

# ---------------------------------------------------------------------------
# 7. ESCENARIOS DE RUIDO Y ATENUACIÓN
# ---------------------------------------------------------------------------
# Se evalúan distintos escenarios de comunicación:
#   - Escenario 1: canal limpio, poco ruido (SNR alta)
#   - Escenario 2: ruido moderado
#   - Escenario 3: ruido fuerte + atenuación de la señal

escenarios = {
    "Escenario 1: Poco ruido (SNR = 25 dB)": {"snr_db": 25, "atenuacion": 1.0},
    "Escenario 2: Ruido moderado (SNR = 10 dB)": {"snr_db": 10, "atenuacion": 0.8},
    "Escenario 3: Ruido fuerte + atenuación (SNR = 2 dB)": {"snr_db": 2, "atenuacion": 0.4},
}

resultados = {}

fig, axs = plt.subplots(len(escenarios), 1, figsize=(10, 10))

for i, (nombre, params) in enumerate(escenarios.items()):
    # Atenuación: reduce la amplitud de la señal (simula pérdida en el canal)
    senal_atenuada = senal_modulada * params["atenuacion"]
    # Ruido: se agrega ruido gaussiano para simular condiciones del canal
    senal_recibida = agregar_ruido(senal_atenuada, params["snr_db"])
    snr_real = calcular_snr(senal_atenuada, senal_recibida)

    resultados[nombre] = {
        "atenuacion": params["atenuacion"],
        "snr_objetivo_db": params["snr_db"],
        "snr_real_db": snr_real,
    }

    axs[i].plot(t * 1000, senal_recibida, linewidth=0.7)
    axs[i].set_title(f"{nombre} | SNR real ≈ {snr_real:.2f} dB")
    axs[i].set_xlabel("Tiempo (ms)")
    axs[i].set_ylabel("Amplitud")
    axs[i].grid(True)

plt.tight_layout()
plt.savefig(f"{CARPETA_SALIDA}/04_escenarios_ruido_distorsion.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 8. COMPARACIÓN ESPECTRAL: SEÑAL LIMPIA VS. SEÑAL CON RUIDO FUERTE
# ---------------------------------------------------------------------------
peor_escenario = list(escenarios.keys())[-1]
params_peor = escenarios[peor_escenario]
senal_peor = agregar_ruido(senal_modulada * params_peor["atenuacion"],
                            params_peor["snr_db"])

freq_peor, mag_peor = calcular_espectro(senal_peor, fs)

plt.figure(figsize=(10, 4))
plt.plot(freq_mod, mag_mod, label="Señal modulada original", alpha=0.8)
plt.plot(freq_peor, mag_peor, label=f"Señal con ruido/atenuación ({peor_escenario})",
          alpha=0.8)
plt.title("Comparación espectral: señal limpia vs. señal degradada")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud")
plt.xlim(0, fc + 3 * fm)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{CARPETA_SALIDA}/05_comparacion_espectral.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 9. RESUMEN DE RESULTADOS EN CONSOLA
# ---------------------------------------------------------------------------
print("=" * 70)
print("RESUMEN DE RESULTADOS - MODULACIÓN AM")
print("=" * 70)
print(f"Frecuencia de la señal mensaje (fm): {fm} Hz")
print(f"Frecuencia de la portadora (fc):     {fc} Hz")
print(f"Índice de modulación (m):            {m}")
print("-" * 70)
for nombre, datos in resultados.items():
    print(f"{nombre}")
    print(f"   Atenuación aplicada:  {datos['atenuacion']*100:.0f}% de la amplitud original")
    print(f"   SNR objetivo:         {datos['snr_objetivo_db']} dB")
    print(f"   SNR real medida:      {datos['snr_real_db']:.2f} dB")
    print("-" * 70)

print(f"\nTodas las gráficas se guardaron en la carpeta: {CARPETA_SALIDA}/")
