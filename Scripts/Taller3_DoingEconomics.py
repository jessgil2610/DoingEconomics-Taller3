# -*- coding: utf-8 -*-
"""
* Taller 3 - Haciendo Economía
* Realizado por: Jessica Gil y
"""

# ========================
#  0. Importe de librerias
# ========================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pingouin as pg
from lets_plot import *

LetsPlot.setup_html(no_js=True)

# =====================
# Definición de rutas
# =====================

BASE_DIR = Path(r"C:\Users\jessi\OneDrive\Documents\GitHub\DoingEconomics-Taller3")

RAW_PATH = BASE_DIR / "RawData"
RESULTS_PATH = BASE_DIR / "Results"

print("Base:", BASE_DIR)

# 1.1.1. Importar base de datos y guardar en la carpeta RawData

file_path = RAW_PATH / "temperature_anomalies_northernh.csv"

df = pd.read_csv(
    file_path,
    skiprows=1,
    na_values="***"
)

# Verificación de la base cargada
print(df.head())
print(df.info())
df = df.set_index("Year")
df.head()


# 1.1.2. Gráfico 1:
''' Elige un mes y construye un gráfico de línea con la anomalía 
    de temperatura promedio en el eje vertical y el tiempo (desde 1880 
    hasta el último año disponible) en el eje horizontal '''

month = "Dec"
fig, ax = plt.subplots()
ax.axhline(0, color="orange")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(
    f"Average temperature anomaly in {month} \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");

month = "Apr"
fig, ax = plt.subplots()
ax.axhline(0, color="orange")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(
    f"Average temperature anomaly in {month} \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");

# 1.1.3. Gráfico 2:
''' Ahora, otro gráfico pero con los promedios de cada estación 
    (una línea por estación).  Las columnas DJF, MAM, JJA, SON 
    contienen dicha información. Por ejemplo, MAM es el promedio 
    de los meses Marzo, Abril y Mayo. '''

seasons = ["DJF", "MAM", "JJA", "SON"]

fig, ax = plt.subplots()

for season in seasons:
    df[season].plot(ax=ax, label=season)

ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
ax.set_title(f"Average seasonal temperature anomaly\nin the northern hemisphere (1880–{df.index.max()})")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_xlabel("Year")
ax.legend(title="Season")
plt.show()


# 1.1.4. Gráfico 3:
''' Ahora hagamos una gráfica con los promedios de las anomalías 
    anuales. Esta información está en las columnas J-D '''

month = "J-D"
fig, ax = plt.subplots()
ax.axhline(0, color="orange")
ax.annotate("1951—1980 average", xy=(0.68, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(
    f"Average annual temperature anomaly in \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");


seasons = ["DJF", "MAM", "JJA", "SON"]
season_names = {
    "DJF": "Winter (Dec-Jan-Feb)",
    "MAM": "Spring (Mar-Apr-May)",
    "JJA": "Summer (Jun-Jul-Aug)",
    "SON": "Autumn (Sep-Oct-Nov)"
}

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), sharex=True, sharey=True)
axes = axes.flatten()  # convierte la matriz 2x2 en una lista de 4 ejes

for i, season in enumerate(seasons):
    ax = axes[i]
    df[season].plot(ax=ax)
    ax.axhline(0, color="orange", linestyle="--", linewidth=1)
    ax.set_title(season_names[season])
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature anomaly (°C)")

fig.suptitle(f"Average seasonal temperature anomaly\nin the northern hemisphere (1880–{df.index.max()})",
             fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

# 1.2.1 Creación de tablas de frecuencias para los años 1951-1980 y 1981-2010

# Crear columna Period 
df["Period"] = pd.cut(
    df.index,
    bins=[1920, 1950, 1980, 2010],  # 1920 en vez de 1921 para incluir 1921
    labels=["1921—1950", "1951—1980", "1981—2010"],
    ordered=True,
)

# Verificar que se creó bien
print(df["Period"].value_counts().sort_index())
print(df.columns.tolist())  # confirmar que 'Period' aparece

col = "J-D"

# Filtrar períodos
df_1951_1980 = df[df["Period"] == "1951—1980"][col].dropna()
df_1981_2010 = df[df["Period"] == "1981—2010"][col].dropna()

# Definir bins fijos para que ambas tablas sean comparables
bins = [-0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
labels = [f"{bins[i]:.1f} to {bins[i+1]:.1f}" for i in range(len(bins)-1)]

# Crear frecuencias
def make_freq_table(series, bins, labels):
    counts = pd.cut(series, bins=bins, labels=labels, include_lowest=True).value_counts().sort_index()
    freq_table = pd.DataFrame({
        "Intervalo": counts.index,
        "Frecuencia": counts.values,
        "Porcentaje (%)": (counts.values / counts.sum() * 100).round(1)
    })
    return freq_table

table_1951 = make_freq_table(df_1951_1980, bins, labels)
table_1981 = make_freq_table(df_1981_2010, bins, labels)

print("\nTabla 1951–1980:")
print(table_1951.to_string(index=False))
print("\nTabla 1981–2010:")
print(table_1981.to_string(index=False))


# 1.2.2 Histogramas 1951–1980 y 1981–2010
periods = ["1951—1980", "1981—2010"]
colors  = ["steelblue", "tomato"]

fig, axes = plt.subplots(ncols=2, figsize=(12, 5), sharex=True, sharey=True)

for ax, period, color in zip(axes, periods, colors):
    data = df.loc[df["Period"] == period, "J-D"].dropna()

    ax.hist(data, bins=10, color=color, edgecolor="white", alpha=0.85)

    # Línea de media
    mean_val = data.mean()
    ax.axvline(mean_val, color="black", linestyle="--", linewidth=1.2,
               label=f"Media: {mean_val:.2f}°C")

    ax.set_title(period, fontsize=12, fontweight="bold")
    ax.set_xlabel("Anomalía de temperatura (°C)", fontsize=10)
    ax.set_ylabel("Frecuencia", fontsize=10)
    ax.legend(fontsize=9)

fig.suptitle(
    "Distribución de anomalías anuales de temperatura (J-D)\nHemisferio Norte",
    fontsize=13, fontweight="bold"
)
plt.tight_layout()
plt.show()


# 1.2.3 Deciles 3 y 7 usando datos de 1951–1980
data_ref = df.loc[df["Period"] == "1951—1980", "J-D"].dropna()

decil_3 = np.quantile(data_ref, 0.3)
decil_7 = np.quantile(data_ref, 0.7)

print(f"Decil 3 (umbral 'frío'):    {decil_3:.4f}°C")
print(f"Decil 7 (umbral 'caliente'): {decil_7:.4f}°C")

# 1.2.4 Anomalías "calientes" en 1981–2010
data_1981 = df.loc[df["Period"] == "1981—2010", "J-D"].dropna()

calientes = (data_1981 > decil_7).sum()
porcentaje = (calientes / len(data_1981)) * 100

print(f"Total años en 1981–2010:         {len(data_1981)}")
print(f"Años considerados 'calientes':   {calientes}")
print(f"Porcentaje 'caliente':           {porcentaje:.1f}%")

# 1.2.5 Media y varianza por estación y período
seasons = ["DJF", "MAM", "JJA", "SON"]
periods = ["1921—1950", "1951—1980", "1981—2010"]

results = []
for period in periods:
    subset = df[df["Period"] == period]
    for season in seasons:
        data = subset[season].dropna()
        results.append({
            "Período":  period,
            "Estación": season,
            "Media":    round(data.mean(), 4),
            "Varianza": round(data.var(), 4)
        })

df_stats = pd.DataFrame(results)
print(df_stats.to_string(index=False))

















