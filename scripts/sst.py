# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 19:44:15 2024

@author: ferfo
"""

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from cartopy.io import shapereader
from shapely.geometry import Point, shape

# Cargar el archivo NetCDF
file_path = "C:/Users/ferfo/OneDrive/Escritorio/anomsst2012.nc"
data = xr.open_dataset(file_path)

# Seleccionar la variable de anomalías de temperatura superficial del mar (SST)
sst_anomalies = data['skt']

# Seleccionar el primer tiempo disponible
sst_anomalies = sst_anomalies.isel(time=0)

# Ajustar longitudes de (0-360) a (-180, 180)
sst_anomalies = sst_anomalies.assign_coords(
    lon=((sst_anomalies.lon + 180) % 360 - 180)
).sortby("lon")

# Obtener coordenadas de latitud y longitud
lon = sst_anomalies.lon.values
lat = sst_anomalies.lat.values

# Crear una grilla de coordenadas
lon2d, lat2d = np.meshgrid(lon, lat)

# Cargar la máscara de tierra desde Natural Earth
land_shp = shapereader.natural_earth(resolution='110m', category='physical', name='land')
land_geom = [shape(record.geometry) for record in shapereader.Reader(land_shp).records()]

# Crear una máscara para la tierra
land_mask = np.zeros(lon2d.shape, dtype=bool)

# Iterar sobre cada punto y verificar si está en la tierra
for i in range(lon2d.shape[0]):  # Iterar sobre latitudes
    for j in range(lon2d.shape[1]):  # Iterar sobre longitudes
        point = Point(lon2d[i, j], lat2d[i, j])
        if any(geom.contains(point) for geom in land_geom):
            land_mask[i, j] = True  # Marcar como tierra

# Aplicar la máscara: los valores en la tierra se convierten en NaN
sst_anomalies_2d = np.where(land_mask, np.nan, sst_anomalies.values)

# Definir niveles para la barra de color
levels = np.linspace(-2, 2, 11)

# Crear la figura
fig, ax = plt.subplots(
    subplot_kw={'projection': ccrs.PlateCarree(central_longitude=290)},
    figsize=(12, 7)
)

# Graficar las anomalías de SST con contourf (solo sobre el océano)
contour = ax.contourf(
    lon2d, lat2d, sst_anomalies_2d,
    levels=levels,
    cmap='coolwarm',
    extend='both',
    transform=ccrs.PlateCarree()
)

# Agregar texto identificador
ax.text(
    75, 55, "(b)", fontsize=16, fontweight="bold",
    color="black", transform=ccrs.PlateCarree(),
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
)

# Agregar la barra de color
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', shrink=0.5, pad=0.03)
cbar.set_label('SST Anomalies (°C)', fontsize=14)
cbar.set_ticks(levels)
cbar.ax.tick_params(labelsize=14)

# Configurar el mapa
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.LAND, facecolor='lightgray', edgecolor='black')
ax.set_extent([-180, 180, -60, 70], crs=ccrs.PlateCarree())

# Guardar la figura
plt.savefig("C:/Users/ferfo/OneDrive/Escritorio/sst-2.png", dpi=300, bbox_inches='tight')

# Mostrar el gráfico
plt.show()
