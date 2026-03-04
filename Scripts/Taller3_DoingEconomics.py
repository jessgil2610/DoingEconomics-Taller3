# -*- coding: utf-8 -*-
"""
* Taller 3 - Haciendo Economía
* Realizado por: Jessica Gil y
"""

# =====================
# IMPORTS
# =====================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pingouin as pg
from lets_plot import *

LetsPlot.setup_html(no_js=True)

# =====================
# DEFINIR RUTA BASE (TU REPO)
# =====================

BASE_DIR = Path(r"C:\Users\jessi\OneDrive\Documents\GitHub\DoingEconomics-Taller3")

RAW_PATH = BASE_DIR / "RawData"
RESULTS_PATH = BASE_DIR / "Results"

print("Base:", BASE_DIR)

# =====================
# CARGAR DATOS
# =====================

file_path = RAW_PATH / "temperature_anomalies_northernh.csv"

df = pd.read_csv(
    file_path,
    skiprows=1,
    na_values="***"
)

print(df.head())
print(df.info())


df = df.set_index("Year")
df.head()


month = "J-D"
fig, ax = plt.subplots()
ax.axhline(0, color="orange")
ax.annotate("1951—1980 average", xy=(0.68, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(
    f"Average annual temperature anomaly in \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");



df["Period"] = pd.cut(
    df.index,
    bins=[1921, 1950, 1980, 2010],
    labels=["1921—1950", "1951—1980", "1981—2010"],
    ordered=True,
)

df["Period"].tail(20)
list_of_months = ["Jun", "Jul", "Aug"]
df[list_of_months].stack().head()


fig, axes = plt.subplots(ncols=3, figsize=(9, 4), sharex=True, sharey=True)
for ax, period in zip(axes, df["Period"].dropna().unique()):
    df.loc[df["Period"] == period, list_of_months].stack().hist(ax=ax)
    ax.set_title(period)
plt.suptitle("Histogram of temperature anomalies")
axes[1].set_xlabel("Summer temperature distribution")
plt.tight_layout();


# Create a variable that has years 1951 to 1980, and months Jan to Dec (inclusive)
temp_all_months = df.loc[(df.index >= 1951) & (df.index <= 1980), "Jan":"Dec"]
# Put all the data in stacked format and give the new columns sensible names
temp_all_months = (
    temp_all_months.stack()
    .reset_index()
    .rename(columns={"level_1": "month", 0: "values"})
)
# Take a look at this data:
temp_all_months

quantiles = [0.3, 0.7]
list_of_percentiles = np.quantile(temp_all_months["values"], q=quantiles)

print(f"The cold threshold of {quantiles[0]*100}% is {list_of_percentiles[0]}")
print(f"The hot threshold of {quantiles[1]*100}% is {list_of_percentiles[1]}")


# Create a variable that has years 1981 to 2010, and months Jan to Dec (inclusive)
temp_all_months = df.loc[(df.index >= 1981) & (df.index <= 2010), "Jan":"Dec"]
# Put all the data in stacked format and give the new columns sensible names
temp_all_months = (
    temp_all_months.stack()
    .reset_index()
    .rename(columns={"level_1": "month", 0: "values"})
)
# Take a look at the start of this data data:
temp_all_months.head()


entries_less_than_q30 = temp_all_months["values"] < list_of_percentiles[0]
proportion_under_q30 = entries_less_than_q30.mean()
print(
    f"The proportion under {list_of_percentiles[0]} is {proportion_under_q30*100:.2f}%"
)

proportion_over_q70 = (temp_all_months["values"] > list_of_percentiles[1]).mean()
print(f"The proportion over {list_of_percentiles[1]} is {proportion_over_q70*100:.2f}%")

temp_all_months = (
    df.loc[:, "DJF":"SON"]
    .stack()
    .reset_index()
    .rename(columns={"level_1": "Season", 0: "Values"})
)
temp_all_months["Period"] = pd.cut(
    temp_all_months["Year"],
    bins=[1921, 1950, 1980, 2010],
    labels=["1921—1950", "1951—1980", "1981—2010"],
    ordered=True,
)
# Take a look at a cut of the data using `.iloc`, which provides position
temp_all_months.iloc[-135:-125]

grp_mean_var = temp_all_months.groupby(["Season", "Period"])["Values"].agg(
    [np.mean, np.var]
)
grp_mean_var




temp_all_months["Period"] = (
    temp_all_months["Period"]
    .astype("string")
    .astype("object")
    .astype("category")
)

temp_all_months["Period"] = temp_all_months["Period"].astype("object")

# =====================
# PARÁMETROS
# =====================

min_year = 1880
max_year = temp_all_months["Year"].max()

# =====================
# GRÁFICO
# =====================

p = (
    ggplot(temp_all_months, aes(x="Year", y="Values", color="Season"))
    + geom_abline(slope=0, intercept=0, color="black", size=1)
    + geom_line(size=1)
    + labs(
        title="Average annual temperature anomaly",
        x="Year",
        y="Annual temperature anomalies",
        color="Season"
    )
)

ggsave(p, str(RESULTS_PATH / "temperature_plot.html"))
ggsave(p, str(RESULTS_PATH / "temperature_plot.png"))





