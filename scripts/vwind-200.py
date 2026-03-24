# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:28:51 2025

@author: ferfo
"""

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Cargar los archivos NetCDF (ajusta las rutas)
u_wind_file = "C:/Users/ferfo/OneDrive/Escritorio/anomuwnd-2012-200.nc"
v_wind_file = "C:/Users/ferfo/OneDrive/Escritorio/anomvwnd-2012-200.nc"

u_wind_data = xr.open_dataset(u_wind_file)
v_wind_data = xr.open_dataset(v_wind_file)

# Seleccionar las variables de viento (ajusta los nombres si es necesario)
u_anomalies = u_wind_data['uwnd']  # Ajusta si el nombre es diferente
v_anomalies = v_wind_data['vwnd']  # Ajusta si el nombre es diferente

# Seleccionar el nivel de presión 850 hPa (ajusta la dimensión si es necesario)
if 'pressure_level' in u_anomalies.dims:
    u_anomalies = u_anomalies.sel(pressure_level=200.0)
    v_anomalies = v_anomalies.sel(pressure_level=200.0)
elif 'level' in u_anomalies.dims:  # Si la dimensión se llama 'level'
    u_anomalies = u_anomalies.sel(level=200.0)
    v_anomalies = v_anomalies.sel(level=200.0)

# Seleccionar el primer tiempo (si 'time' está presente)
u_anomalies = u_anomalies.isel(time=0)
v_anomalies = v_anomalies.isel(time=0)

# Ajustar las longitudes de (0-360) a (-180, 180)
u_anomalies = u_anomalies.assign_coords(
    lon=((u_anomalies.lon + 180) % 360 - 180)
).sortby("lon")
v_anomalies = v_anomalies.assign_coords(
    lon=((v_anomalies.lon + 180) % 360 - 180)
).sortby("lon")

# Interpolar v_anomalies a la malla de u_anomalies (si es necesario)
v_anomalies = v_anomalies.interp(lat=u_anomalies.lat, lon=u_anomalies.lon)

# Calcular la velocidad del viento en m/s (magnitud)
wind_speed_anomalies = np.sqrt(u_anomalies**2 + v_anomalies**2)

# Convertir a arrays 2D para graficar
wind_speed_anomalies_2d = wind_speed_anomalies.values
u_anomalies_2d = u_anomalies.values
v_anomalies_2d = v_anomalies.values

# Definir niveles para la barra de color
levels = np.arange(0, 24.1, 4)  # Niveles de magnitud de viento

# Crear el plot
fig, ax = plt.subplots(
    subplot_kw={'projection': ccrs.PlateCarree(central_longitude=290)},  # Centrar en el Pacífico
    figsize=(12, 7)
)

# Graficar las anomalías de velocidad del viento usando contourf
contour = ax.contourf(
    wind_speed_anomalies.lon,
    wind_speed_anomalies.lat,
    wind_speed_anomalies_2d,
    levels=levels,
    cmap='PuBuGn',
    extend='both',
    transform=ccrs.PlateCarree()
)

# Agregar la barra de color
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', shrink=0.5, pad=0.03, ticks=levels)
cbar.set_label('Wind Speed Anomalies (m/s)', fontsize=14)
cbar.ax.tick_params(labelsize=14)

# Graficar los vectores de viento
skip = 3  # Saltar puntos para evitar saturación
quiver = ax.quiver(
    u_anomalies.lon[::skip],
    u_anomalies.lat[::skip],
    u_anomalies_2d[::skip, ::skip],
    v_anomalies_2d[::skip, ::skip],
    transform=ccrs.PlateCarree(),
    scale=400,  # Ajusta la escala para la longitud de las flechas
    color='black',
    width=0.002
)

# Agregar la etiqueta de referencia de viento
quiver_key = ax.quiverkey(
    quiver, 
    X=0.95, Y=-0.05, U=14,  # Centrar y bajar la flecha debajo del gráfico
    label='',  # Se deja vacío porque el texto se pondrá aparte
    labelpos='N',
    coordinates='axes',
    fontproperties={'size': 14},
    labelsep=0.05
)

# Agregar texto manualmente con fondo blanco
ax.text(
    0.95, -0.11,  # Coordenadas en el espacio de los ejes
    "10 m/s", 
    fontsize=12,
    fontweight="bold",
    ha="center",
    transform=ax.transAxes
)

# Agregar etiqueta en el gráfico
ax.text(
    75, 55,  # Coordenadas en longitud y latitud
    "(h)",
    fontsize=16,
    fontweight="bold",
    color="black",
    transform=ccrs.PlateCarree(),
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
)

# Configurar el mapa
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='black')
ax.set_extent([-180, 180, -60, 70], crs=ccrs.PlateCarree())

# Guardar la figura
plt.savefig("C:/Users/ferfo/OneDrive/Escritorio/wind-200-2.png", dpi=300, bbox_inches='tight')

# Mostrar el gráfico
plt.show()