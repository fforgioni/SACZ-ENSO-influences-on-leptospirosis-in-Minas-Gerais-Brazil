# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:16:35 2025

@author: ferfo
"""

import xarray as xr
import numpy as np
from metpy.units import units
import metpy.calc as mpcalc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as mpatches
from scipy.ndimage import zoom


# Cargar los datos
humedad = xr.open_dataset('C:/Users/ferfo/OneDrive/Escritorio/shum2003-1.nc')
uwind = xr.open_dataset('C:/Users/ferfo/OneDrive/Escritorio/uwnddjf.nc')
vwind = xr.open_dataset('C:/Users/ferfo/OneDrive/Escritorio/vwnddjf.nc')

# Extraer variables
q = humedad['shum'].isel(time=0, level=0)       # Humedad específica
temp_u = uwind['uwnd'].isel(time=0, level=0)      # Viento zonal
temp_v = vwind['vwnd'].isel(time=0, level=0)      # Viento meridional

# Convertir a unidades de MetPy
u = temp_u.values * units("m/s")
v = temp_v.values * units("m/s")

# Calcular el transporte de humedad
qu = q.values * u
qv = q.values * v

# Calcular dx y dy (distancias entre puntos)
lat, lon = np.meshgrid(q['lat'], q['lon'], indexing='ij')
lat, lon = lat * units.degrees, lon * units.degrees
dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat, x_dim=-1, y_dim=-2)

# Calcular la divergencia
divergence = mpcalc.divergence(qu, qv, dx=dx, dy=dy)

# Crear DataArray para el ploteo
convergencia_xr = xr.DataArray(
    data=divergence.magnitude,
    dims=["lat", "lon"],
    coords={"lat": q["lat"], "lon": q["lon"]},
    attrs={"units": "1/s", "long_name": "Convergencia de humedad"}
)

# Suavizar el campo
suavizado = gaussian_filter(convergencia_xr, sigma=0)

# Crear la figura
fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(10, 6))

# Configurar el mapa
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5)
ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')
ax.set_extent([-90, -20, -40, 10], crs=ccrs.PlateCarree())
ax.set_xticks(np.arange(-90, -10, 5))
ax.set_yticks(np.arange(-40, 21, 5))

# Definir niveles manualmente en el rango deseado
levels = np.linspace(-1.2e-4, 8.6e-5, 11)  # 11 niveles entre los valores deseados

cmap = plt.cm.twilight_shifted

data = ax.contourf(
    convergencia_xr.lon,
    convergencia_xr.lat,
    suavizado,
    levels,
    cmap=cmap,
    extend='both',
    transform=ccrs.PlateCarree()
)

# Crear malla de coordenadas
lon_grid, lat_grid = np.meshgrid(q['lon'], q['lat'])
lon_grid = np.where(lon_grid > 180, lon_grid - 360, lon_grid)
sorted_indices = np.argsort(lon_grid[0, :])  # Ordena longitudes
lon_grid = lon_grid[:, sorted_indices]
temp_u = temp_u[:, sorted_indices]
temp_v = temp_v[:, sorted_indices]

# Graficar las líneas de corriente
ax.streamplot(
    lon_grid,
    lat_grid,
    temp_u.values,
    temp_v.values,
    transform=ccrs.PlateCarree(),
    color='black',
    linewidth=0.8,
    density=3,  # Reducir densidad si hay demasiadas líneas
    arrowsize=1
)

# Agregar contorno punteado para Minas Gerais
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none'
)
ax.add_feature(states_provinces, edgecolor='black', linestyle='--', linewidth=1)

# Agregar un rectángulo para Minas Gerais
min_long = -51  
max_long = -39  
min_lat = -22   
max_lat = -14   
rect = mpatches.Rectangle(
    xy=(min_long, min_lat),
    width=(max_long - min_long),
    height=(max_lat - min_lat),
    linewidth=2,
    edgecolor='black',
    linestyle='--',
    facecolor='none',
    transform=ccrs.PlateCarree()
)
ax.add_patch(rect)

# Agregar etiqueta "(c)"
ax.text(
    -25, 15,
    "(a)",
    fontsize=16,
    fontweight="bold",
    color="black",
    transform=ccrs.PlateCarree(),
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
)

ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)

# Barra de color
cbar = plt.colorbar(data, orientation='vertical', pad=0.05, shrink=1, fraction=0.05, ax=ax)
cbar.set_label('Humidity divergence (1/s)', fontsize=16, labelpad=10)
cbar.ax.tick_params(labelsize=16)
cbar.set_ticks(levels)

def scientific_formatter(x, _):
    return "0" if np.isclose(x, 0, atol=1e-10) else f"{x:.1e}"
formatter = FuncFormatter(scientific_formatter)
cbar.ax.yaxis.set_major_formatter(formatter)

plt.savefig('C:/Users/ferfo/OneDrive/Escritorio/div-hum-1.png', dpi=300, bbox_inches='tight')
plt.show()
