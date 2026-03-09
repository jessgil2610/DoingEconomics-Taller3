# 🌡️ Taller 3 — Haciendo Economía
## Midiendo la temperatura de la Tierra y el CO₂

**Materia:** Haciendo Economía  
**Integrantes:** Jessica Gil y Esteban Mora  
**Herramienta:** Python 3 (Anaconda — Spyder)  

---

## 📋 Descripción

Este repositorio contiene el desarrollo del Taller 3 de la materia *Haciendo Economía*, en el cual se analizan datos climáticos históricos para estudiar patrones de cambio de temperatura global y su relación con los niveles de CO₂ atmosférico.

El análisis se divide en tres partes:

- **Parte 1.1** — Anomalías de temperatura del hemisferio norte (NASA GISS)
- **Parte 1.2** — Distribución y variabilidad de temperaturas por períodos históricos
- **Parte 1.3** — Concentración de CO₂ en Mauna Loa y su relación con la temperatura

---

## 🗂️ Estructura del repositorio

```
DoingEconomics-Taller3/
│
├── RawData/
│   ├── temperature_anomalies_northernh.csv   # Anomalías de temperatura NASA GISS
│   └── co2_mauna_loa.xlsx                    # Concentración de CO₂ NOAA Mauna Loa
│
├── Results/
│   ├── anomalia_dec.png                      # Gráfico anomalía mensual — Diciembre
│   ├── anomalia_apr.png                      # Gráfico anomalía mensual — Abril
│   ├── anomalia_season.png                   # Gráfico estacional combinado
│   ├── anomalia_seasonv2.png                 # Gráfico estacional panel 2x2
│   ├── anomalia_annual.png                   # Gráfico anomalía anual (J-D)
│   ├── histogramas_periodos.png              # Histogramas 1951–1980 vs 1981–2010
│   ├── co2_trend_interpolated.png            # Gráfico CO₂ interpolated vs trend
│   └── dispersion_temp_co2.png              # Dispersión temperatura vs CO₂
│
├── Scripts/
│   └── taller3_doingeconomics.py             # Script principal del análisis
│
└── README.md
```

---

## 📦 Fuentes de datos

| Dataset | Fuente | Descripción |
|---|---|---|
| `temperature_anomalies_northernh.csv` | [NASA GISS](https://data.giss.nasa.gov/gistemp/) | Anomalías mensuales, estacionales y anuales de temperatura del hemisferio norte (1880–presente). Referencia: promedio 1951–1980. |
| `co2_mauna_loa.xlsx` | [NOAA GML](https://tinyco.re/3763425) | Concentración mensual de CO₂ atmosférico registrada en el Observatorio Mauna Loa, Hawái (1958–2018). |





