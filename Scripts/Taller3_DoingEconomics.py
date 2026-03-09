# -*- coding: utf-8 -*-
"""
================================================================================
  Taller 3 - Haciendo Economía: Midiendo la temperatura de la Tierra y el CO₂
  Realizado por: Jessica Gil y Esteban Mora
================================================================================

  Estructura:
    Parte 1.1 — Anomalías de temperatura (gráficos mensual, estacional, anual)
    Parte 1.2 — Distribución de temperaturas por períodos históricos
    Parte 1.3 — CO₂ y su relación con la temperatura

  Fuentes de datos:
    - NASA GISS: temperature_anomalies_northernh.csv
    - NOAA Mauna Loa: co2_mauna_loa.xlsx
================================================================================
"""

# ============================================================
#  0. IMPORTACIÓN DE LIBRERÍAS
# ============================================================
# pip install openpyxl  ← ejecutar en terminal si no está instalado

import openpyxl                      # Lectura de archivos Excel
import pandas as pd                  # Manipulación de datos
import numpy as np                   # Cálculos numéricos
import matplotlib.pyplot as plt      # Visualización
from pathlib import Path             # Manejo de rutas de archivos
import pingouin as pg                # Estadística (disponible para uso futuro)
from lets_plot import *              # Gráficos alternativos (disponible para uso futuro)

LetsPlot.setup_html(no_js=True)


# ============================================================
#  DEFINICIÓN DE RUTAS
# ============================================================

BASE_DIR     = Path(r"C:\Users\jessi\OneDrive\Documents\GitHub\DoingEconomics-Taller3")
RAW_PATH     = BASE_DIR / "RawData"     # Carpeta con datos crudos
RESULTS_PATH = BASE_DIR / "Results"     # Carpeta donde se guardan los gráficos

print("Directorio base:", BASE_DIR)


# ============================================================
#  PARTE 1.1 — ANOMALÍAS DE TEMPERATURA
# ============================================================

# ------------------------------------------------------------
#  1.1.1. Carga de datos de temperatura
# ------------------------------------------------------------
# Datos: NASA GISS - Northern Hemisphere mean monthly,
#        seasonal, and annual temperature anomalies (1880–presente)
# Referencia: promedio del período 1951–1980 = 0°C

file_path = RAW_PATH / "temperature_anomalies_northernh.csv"

df = pd.read_csv(
    file_path,
    skiprows=1,        # La primera fila es un encabezado descriptivo
    na_values="***"    # "***" indica dato faltante en este dataset
)

# Verificación inicial de la estructura del dataset
print(df.head())
print(df.info())

# El año se usa como índice para facilitar el plotting por tiempo
df = df.set_index("Year")


# ------------------------------------------------------------
#  1.1.2. Gráfico 1: Anomalía mensual (mes elegido)
# ------------------------------------------------------------
# Se grafican dos meses para comparar comportamientos distintos:
# Diciembre (invierno) y Abril (primavera)

# --- Diciembre ---
month = "Dec"
fig, ax = plt.subplots()
ax.axhline(0, color="orange")   # Línea de referencia: promedio 1951–1980
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(f"Average temperature anomaly in {month}\nin the northern hemisphere (1880—{df.index.max()})")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_xlabel("Year")
plt.savefig(RESULTS_PATH / "anomalia_dec.png", dpi=150, bbox_inches="tight")
plt.show()

# --- Abril ---
month = "Apr"
fig, ax = plt.subplots()
ax.axhline(0, color="orange")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(f"Average temperature anomaly in {month}\nin the northern hemisphere (1880—{df.index.max()})")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_xlabel("Year")
plt.savefig(RESULTS_PATH / "anomalia_apr.png", dpi=150, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
#  1.1.3. Gráfico 2: Anomalía estacional (DJF, MAM, JJA, SON)
# ------------------------------------------------------------
# Cada estación es el promedio de 3 meses:
#   DJF = Diciembre, Enero, Febrero  (Invierno)
#   MAM = Marzo, Abril, Mayo         (Primavera)
#   JJA = Junio, Julio, Agosto       (Verano)
#   SON = Septiembre, Octubre, Nov.  (Otoño)

seasons = ["DJF", "MAM", "JJA", "SON"]

# --- Gráfico combinado: las 4 estaciones en un solo panel ---
fig, ax = plt.subplots()
for season in seasons:
    df[season].plot(ax=ax, label=season)
ax.axhline(0, color="black", linestyle="--", linewidth=0.8)
ax.set_title(f"Average seasonal temperature anomaly\nin the northern hemisphere (1880–{df.index.max()})")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_xlabel("Year")
ax.legend(title="Season")
plt.savefig(RESULTS_PATH / "anomalia_season.png", dpi=150, bbox_inches="tight")
plt.show()

# --- Gráfico separado: panel 2x2 con una estación por subgráfico ---
season_names = {
    "DJF": "Winter (Dec-Jan-Feb)",
    "MAM": "Spring (Mar-Apr-May)",
    "JJA": "Summer (Jun-Jul-Aug)",
    "SON": "Autumn (Sep-Oct-Nov)"
}

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), sharex=True, sharey=True)
axes = axes.flatten()  # Convierte la matriz 2x2 en lista de 4 ejes

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
plt.savefig(RESULTS_PATH / "anomalia_seasonv2.png", dpi=150, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
#  1.1.4. Gráfico 3: Anomalía anual promedio (columna J-D)
# ------------------------------------------------------------
# J-D = promedio anual de enero a diciembre
# Es el indicador más sintético del calentamiento global anual

month = "J-D"
fig, ax = plt.subplots()
ax.axhline(0, color="orange")
ax.annotate("1951—1980 average", xy=(0.68, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(f"Average annual temperature anomaly\nin the northern hemisphere (1880—{df.index.max()})")
ax.set_ylabel("Temperature anomaly (°C)")
ax.set_xlabel("Year")
plt.savefig(RESULTS_PATH / "anomalia_annual.png", dpi=150, bbox_inches="tight")
plt.show()


# ============================================================
#  PARTE 1.2 — DISTRIBUCIÓN DE TEMPERATURAS POR PERÍODO
# ============================================================

# ------------------------------------------------------------
#  1.2.1. Tablas de frecuencia: 1951–1980 y 1981–2010
# ------------------------------------------------------------
# Se crean períodos históricos para comparar la distribución
# de anomalías antes y después del calentamiento acelerado

df["Period"] = pd.cut(
    df.index,
    bins=[1920, 1950, 1980, 2010],   # Límite inferior en 1920 para incluir 1921
    labels=["1921—1950", "1951—1980", "1981—2010"],
    ordered=True,
)

# Verificación de la columna creada
print(df["Period"].value_counts().sort_index())
print("Columnas del dataframe:", df.columns.tolist())

col = "J-D"  # Se usa la anomalía anual para comparar períodos completos

# Separar datos por período
df_1951_1980 = df[df["Period"] == "1951—1980"][col].dropna()
df_1981_2010 = df[df["Period"] == "1981—2010"][col].dropna()

# Bins fijos para que ambas tablas sean directamente comparables
bins   = [-0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
labels = [f"{bins[i]:.1f} to {bins[i+1]:.1f}" for i in range(len(bins) - 1)]

def make_freq_table(series, bins, labels):
    """Construye una tabla de frecuencias absolutas y relativas."""
    counts = pd.cut(series, bins=bins, labels=labels,
                    include_lowest=True).value_counts().sort_index()
    freq_table = pd.DataFrame({
        "Intervalo":     counts.index,
        "Frecuencia":    counts.values,
        "Porcentaje (%)": (counts.values / counts.sum() * 100).round(1)
    })
    return freq_table

table_1951 = make_freq_table(df_1951_1980, bins, labels)
table_1981 = make_freq_table(df_1981_2010, bins, labels)

print("\nTabla de frecuencias — 1951–1980:")
print(table_1951.to_string(index=False))
print("\nTabla de frecuencias — 1981–2010:")
print(table_1981.to_string(index=False))


# ------------------------------------------------------------
#  1.2.2. Histogramas: distribución de anomalías por período
# ------------------------------------------------------------
# Permite comparar visualmente si la distribución se desplazó
# hacia temperaturas más altas en el período reciente

periods = ["1951—1980", "1981—2010"]
colors  = ["steelblue", "tomato"]

fig, axes = plt.subplots(ncols=2, figsize=(12, 5), sharex=True, sharey=True)

for ax, period, color in zip(axes, periods, colors):
    data = df.loc[df["Period"] == period, "J-D"].dropna()

    ax.hist(data, bins=10, color=color, edgecolor="white", alpha=0.85)

    # Línea vertical en la media del período
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
plt.savefig(RESULTS_PATH / "histogramas_periodos.png", dpi=150, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
#  1.2.3. Deciles 3 y 7 del período de referencia 1951–1980
# ------------------------------------------------------------
# El NYT clasifica:
#   - Frío:     anomalías por debajo del decil 3
#   - Caliente: anomalías por encima del decil 7

data_ref = df.loc[df["Period"] == "1951—1980", "J-D"].dropna()

decil_3 = np.quantile(data_ref, 0.3)   # Umbral inferior (frío)
decil_7 = np.quantile(data_ref, 0.7)   # Umbral superior (caliente)

print(f"\nDecil 3 — umbral 'frío':     {decil_3:.4f}°C")
print(f"Decil 7 — umbral 'caliente': {decil_7:.4f}°C")


# ------------------------------------------------------------
#  1.2.4. Proporción de años "calientes" en 1981–2010
# ------------------------------------------------------------
# Se aplican los umbrales de 1951–1980 al período 1981–2010
# para evaluar si las temperaturas altas se volvieron más frecuentes

data_1981 = df.loc[df["Period"] == "1981—2010", "J-D"].dropna()

calientes  = (data_1981 > decil_7).sum()
porcentaje = (calientes / len(data_1981)) * 100

print(f"\nTotal de años en 1981–2010:        {len(data_1981)}")
print(f"Años considerados 'calientes':     {calientes}")
print(f"Porcentaje de años 'calientes':    {porcentaje:.1f}%")


# ------------------------------------------------------------
#  1.2.5. Media y varianza estacional por período
# ------------------------------------------------------------
# Compara si las temperaturas se volvieron más variables
# (mayor varianza) en los períodos más recientes

seasons = ["DJF", "MAM", "JJA", "SON"]
periods = ["1921—1950", "1951—1980", "1981—2010"]

results = []
for period in periods:
    subset = df[df["Period"] == period]
    for season in seasons:
        data = subset[season].dropna()
        results.append({
            "Período":   period,
            "Estación":  season,
            "Media":     round(data.mean(), 4),
            "Varianza":  round(data.var(),  4)
        })

df_stats = pd.DataFrame(results)
print("\nMedia y varianza por estación y período:")
print(df_stats.to_string(index=False))


# ============================================================
#  PARTE 1.3 — CO₂ Y SU RELACIÓN CON LA TEMPERATURA
# ============================================================

# ------------------------------------------------------------
#  Carga de datos de CO₂ — Observatorio Mauna Loa, Hawái
# ------------------------------------------------------------
# Fuente: NOAA Global Monitoring Laboratory
# Serie histórica desde 1958 hasta 2018
# Variables principales:
#   - monthly_average: promedio mensual directo del instrumento
#   - interpolated:    incluye estimaciones para meses faltantes
#   - trend:           versión suavizada sin variación estacional

file_path2 = RAW_PATH / "co2_mauna_loa.xlsx"
co2 = pd.read_excel(file_path2)

co2 = co2.rename(columns={
    "Year":            "year",
    "Month":           "month",
    "Monthly average": "monthly_average",
    "Interpolated":    "interpolated",
    "Trend":           "trend"
})

print(co2.head())

# Limpieza: el valor -99.99 indica dato faltante
# Se reemplaza por NaN para que no afecte los análisis
co2["monthly_average"] = co2["monthly_average"].replace(-99.99, np.nan)
print(f"Valores faltantes en monthly_average: {co2['monthly_average'].isna().sum()}")

print(co2.info())

# Crear columna de fecha para facilitar el plotting temporal
co2["date"]   = pd.to_datetime(dict(year=co2["year"], month=co2["month"], day=1))
co2_1960      = co2[co2["date"] >= "1960-01-01"].copy()   # Filtrar desde 1960


# ------------------------------------------------------------
#  1.3.3. Gráfico: niveles de CO₂ (interpolated y trend)
# ------------------------------------------------------------
# interpolated (azul): muestra ciclos estacionales
# trend (rojo):        muestra la tendencia de largo plazo suavizada

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(co2_1960["date"], co2_1960["interpolated"],
        label="Interpolated", color="steelblue", linewidth=1, alpha=0.8)
ax.plot(co2_1960["date"], co2_1960["trend"],
        label="Trend", color="tomato", linewidth=1.8)

ax.set_title("Niveles de concentración de CO₂ atmosférico\nObservatorio Mauna Loa (1960–2018)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Año", fontsize=11)
ax.set_ylabel("Concentración de CO₂ (ppm)", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.text(0.99, 0.01, "Fuente: NOAA Global Monitoring Laboratory",
        transform=ax.transAxes, ha="right", fontsize=9, color="gray")

plt.tight_layout()
plt.savefig(RESULTS_PATH / "co2_trend_interpolated.png", dpi=150, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------
#  1.3.4. Diagrama de dispersión: temperatura vs CO₂
# ------------------------------------------------------------
# Se usa enero como mes de referencia para ambas series
# CO₂: variable trend (sin estacionalidad) para capturar tendencia pura

# Cargar temperatura nuevamente con nombres originales de columnas
file_path = RAW_PATH / "temperature_anomalies_northernh.csv"
temp = pd.read_csv(file_path, skiprows=1, na_values="***")
temp.columns = [c.strip() for c in temp.columns]

# Seleccionar enero desde 1960
temp_jan = temp[["Year", "Jan"]].rename(columns={"Jan": "temp_anomaly"})
temp_jan = temp_jan[temp_jan["Year"] >= 1960]

# Seleccionar CO₂ trend de enero desde 1960
co2_jan = co2[co2["month"] == 1][["year", "trend"]].rename(columns={"year": "Year"})
co2_jan = co2_jan[co2_jan["Year"] >= 1960]

# Unir ambas series por año y eliminar filas con datos faltantes
base_final = pd.merge(temp_jan, co2_jan, on="Year").dropna()
print("\nPrimeras filas del dataset combinado (temperatura + CO₂):")
print(base_final.head())

# Coeficiente de correlación de Pearson
# Mide la fuerza y dirección de la relación lineal entre ambas variables
corr = base_final["temp_anomaly"].corr(base_final["trend"])
print(f"\nCoeficiente de correlación de Pearson (r): {corr:.4f}")

# Línea de tendencia lineal por mínimos cuadrados
m, b = np.polyfit(base_final["temp_anomaly"], base_final["trend"], 1)

fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(base_final["temp_anomaly"], base_final["trend"],
           color="steelblue", alpha=0.7, edgecolors="white", s=60,
           label="Observaciones")
ax.plot(base_final["temp_anomaly"],
        m * base_final["temp_anomaly"] + b,
        color="tomato", linewidth=1.8, label="Tendencia lineal")

ax.set_xlabel("Anomalía de temperatura (°C)", fontsize=11)
ax.set_ylabel("Concentración de CO₂ — Trend (ppm)", fontsize=11)
ax.set_title(f"Relación entre anomalía de temperatura y CO₂\nEnero 1960–2018  |  r = {corr:.3f}",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(RESULTS_PATH / "dispersion_temp_co2.png", dpi=150, bbox_inches="tight")
plt.show()