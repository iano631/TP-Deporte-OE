
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("datos/resultados_partidos.csv")
equipos = pd.unique(df[["equipo_local", "equipo_visitante"]].values.ravel())
estadisticas = {e: {"PJ":0,"PG":0,"PE":0,"PP":0,"GF":0,"GC":0,"Pts":0} for e in equipos}

for _, fila in df.iterrows():
    local, visitante = fila["equipo_local"], fila["equipo_visitante"]
    gl, gv = fila["goles_local"], fila["goles_visitante"]
    estadisticas[local]["PJ"] += 1; estadisticas[visitante]["PJ"] += 1
    estadisticas[local]["GF"] += gl; estadisticas[local]["GC"] += gv
    estadisticas[visitante]["GF"] += gv; estadisticas[visitante]["GC"] += gl
    if gl > gv:
        estadisticas[local]["PG"] += 1; estadisticas[local]["Pts"] += 3
        estadisticas[visitante]["PP"] += 1
    elif gl < gv:
        estadisticas[visitante]["PG"] += 1; estadisticas[visitante]["Pts"] += 3
        estadisticas[local]["PP"] += 1
    else:
        estadisticas[local]["PE"] += 1; estadisticas[visitante]["PE"] += 1
        estadisticas[local]["Pts"] += 1; estadisticas[visitante]["Pts"] += 1

tabla = pd.DataFrame(estadisticas).T
tabla["DG"] = tabla["GF"] - tabla["GC"]
tabla = tabla.sort_values(["Pts","DG"], ascending=False)
tabla.to_csv("resultados/tabla_posiciones.csv")
print(tabla)
