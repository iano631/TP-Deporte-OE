# Análisis de Resultados Deportivos — Torneo Falso
# Autor: P3-Luis  Rol: Revisor y QA
# Revisión: Mejora en la documentación y validar datos

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Evita errores de display
import matplotlib.pyplot as plt

# Cargar datos
# ruta relativa para reproducir en Colab
# El archivo tiene que existir en /datos antes de ejecutarse

df = pd.read_csv("datos/resultados_partidos.csv")

# Validación básica: verificar que el dataset no esté vacío
assert len(df) > 0, "ERROR: El dataset está vacío"
assert "equipo_local" in df.columns, "ERROR: Falta columna equipo_local"
assert "equipo_visitante" in df.columns, "ERROR: Falta columna equipo_visitante"
print(f" Dataset validado: {len(df)} partidos cargados")

# Estadisticas
# Se crea un diccionario con variables por equipo:
# PJ=Partidos Jugados, PG=Ganados, PE=Empatados, PP=Perdidos
# GF=Goles a Favor, GC=Goles en Contra, Pts=Puntos

equipos = pd.unique(df[["equipo_local", "equipo_visitante"]].values.ravel())
estadisticas = {e: {"PJ":0,"PG":0,"PE":0,"PP":0,
                    "GF":0,"GC":0,"Pts":0} for e in equipos}

# El proceso de los partidos
# Por cada partido se actualizan los datos de los dos equipos
# Puntuación: Victoria=3pts, Empate=1pt, Derrota=0pts

for _, fila in df.iterrows():
    local = fila["equipo_local"]
    visitante = fila["equipo_visitante"]
    gl = fila["goles_local"]
    gv = fila["goles_visitante"]

    estadisticas[local]["PJ"] += 1
    estadisticas[visitante]["PJ"] += 1
    estadisticas[local]["GF"] += gl
    estadisticas[local]["GC"] += gv
    estadisticas[visitante]["GF"] += gv
    estadisticas[visitante]["GC"] += gl

    if gl > gv:
        estadisticas[local]["PG"] += 1
        estadisticas[local]["Pts"] += 3
        estadisticas[visitante]["PP"] += 1
    elif gl < gv:
        estadisticas[visitante]["PG"] += 1
        estadisticas[visitante]["Pts"] += 3
        estadisticas[local]["PP"] += 1
    else:
        estadisticas[local]["PE"] += 1
        estadisticas[visitante]["PE"] += 1
        estadisticas[local]["Pts"] += 1
        estadisticas[visitante]["Pts"] += 1

# Tabla de pocisiones
# Ordenada por puntos descendente
# con diferencia de goles si se necesita un desempate secundario


tabla = pd.DataFrame(estadisticas).T
tabla["DG"] = tabla["GF"] - tabla["GC"]
tabla = tabla.sort_values(["Pts","DG"], ascending=False)
tabla.index.name = "Equipo"
tabla.to_csv("resultados/tabla_posiciones.csv")
print("\nTabla de posiciones")
print(tabla[["PJ","PG","PE","PP","GF","GC","DG","Pts"]])

# PROMEDIO DE GOLES
# Métrica global del torneo para evaluar nivel ofensivo

total_goles = df["goles_local"].sum() + df["goles_visitante"].sum()
promedio = total_goles / len(df)
print(f"\n Promedio de goles por partido: {promedio:.2f}")

# Graficos
# Dos subgráficos: puntos por equipo y goles a favor vs en contra
# Se guarda en /resultados para la estructura del repositorio

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Estadísticas del Torneo", fontsize=16, fontweight="bold")

colores = ["#2ecc71" if i == 0 else "#3498db" if i == 1
           else "#e74c3c" for i in range(len(tabla))]
axes[0].bar(tabla.index, tabla["Pts"], color=colores)
axes[0].set_title("Puntos por Equipo")
axes[0].set_xlabel("Equipo")
axes[0].set_ylabel("Puntos")
axes[0].tick_params(axis="x", rotation=45)
for i, v in enumerate(tabla["Pts"]):
    axes[0].text(i, v + 0.2, str(int(v)), ha="center", fontweight="bold")

x = range(len(tabla))
width = 0.35
axes[1].bar([i - width/2 for i in x], tabla["GF"],
            width, label="Goles a favor", color="#27ae60")
axes[1].bar([i + width/2 for i in x], tabla["GC"],
            width, label="Goles en contra", color="#e74c3c")
axes[1].set_title("Goles a Favor vs En Contra")
axes[1].set_xlabel("Equipo")
axes[1].set_ylabel("Goles")
axes[1].set_xticks(list(x))
axes[1].set_xticklabels(tabla.index, rotation=45)
axes[1].legend()

plt.tight_layout()
plt.savefig("resultados/grafico_rendimiento.png", dpi=150, bbox_inches="tight")
print("\n Gráfico guardado en resultados/grafico_rendimiento.png")
