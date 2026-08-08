AF4 - Implementación y Análisis de un Sistema de Modulación en Amplitud (AM)

Universidad Ciudadana de Nuevo León Materia: Señales y Sistemas (A) — Término 2026-2 Autor: Luis Angel Chaires Contreras

Descripción

Este proyecto implementa un sistema de modulación en amplitud (AM) utilizando Python, con el apoyo de las bibliotecas NumPy, SciPy y Matplotlib. El objetivo es analizar cómo cambia una señal modulada bajo distintos escenarios de comunicación, evaluando su desempeño ante condiciones de ruido y atenuación mediante la relación señal a ruido (SNR).

Contenido del proyecto
Definición de una señal mensaje (baja frecuencia) y una señal portadora (alta frecuencia).
Implementación de la modulación en amplitud: s(t) = Ac · [1 + m·x(t)] · cos(2π·fc·t).
Visualización de la señal modulada en el dominio del tiempo y su envolvente.
Análisis espectral mediante la Transformada Rápida de Fourier (FFT), identificando la portadora y las bandas laterales.
Simulación de tres escenarios de comunicación con distintos niveles de ruido gaussiano y atenuación.
Cálculo de la SNR real para cuantificar la degradación de la señal en cada escenario.
Comparación espectral entre la señal original y la señal degradada.
Parámetros utilizados
Parámetro	Valor
Frecuencia de muestreo (fs)	100,000 Hz
Frecuencia de la señal mensaje (fm)	300 Hz
Frecuencia de la portadora (fc)	5,000 Hz
Índice de modulación (m)	0.8
Escenarios evaluados
Escenario	Atenuación	SNR objetivo	SNR real medida
1: Poco ruido	100%	25 dB	25.20 dB
2: Ruido moderado	80%	10 dB	9.70 dB
3: Ruido fuerte + atenuación	40%	2 dB	1.96 dB
Requisitos
bash
pip install numpy scipy matplotlib
Ejecución
bash
python modulacion_am.py

El script genera automáticamente una carpeta graficas/ con las siguientes imágenes:

01_senal_mensaje_portadora.png — Señal mensaje y portadora en el tiempo.
02_senal_modulada_tiempo.png — Señal modulada AM y su envolvente.
03_espectro_senal_modulada.png — Espectro de frecuencia de la señal modulada.
04_escenarios_ruido_distorsion.png — Señal recibida en los tres escenarios simulados.
05_comparacion_espectral.png — Comparación espectral: señal limpia vs. señal degradada.
Estructura del repositorio
├── modulacion_am.py     # Código fuente principal
├── graficas/            # Gráficas generadas por el script
└── README.md            # Este archivo
Conclusión

La implementación permitió comprobar de forma práctica los principios de la modulación en amplitud: la relación entre la envolvente y la señal mensaje, la aparición de bandas laterales en el espectro, y el efecto del ruido y la atenuación del canal sobre la calidad de la señal recibida. A menor SNR y mayor atenuación, la señal se degrada de forma significativa tanto en el dominio del tiempo como en el de la frecuencia.
