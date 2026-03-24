# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 15:16:07 2024

@author: ferfo
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as mcolors
from scipy.ndimage import gaussian_filter
import matplotlib.ticker as mticker

# Cargar el archivo NetCDF
file_path = "C:/Users/ferfo/OneDrive/Escritorio/pp2012-1.nc"
data = xr.open_dataset(file_path)

# Seleccionar la variable de precipitación
pp = data['prate']

# Seleccionar el primer tiempo
if 'time' in data.dims:
    pp = pp.isel(time=0)

# Convertir la precipitación a milímetros
pp_mm = pp # Convertir de mm/s a mm/día (si está en mm/s)

# # Interpolar a una grilla más fina para suavizar
# new_lat = np.linspace(pp_mm.lat.min(), pp_mm.lat.max(), 200)
# new_lon = np.linspace(pp_mm.lon.min(), pp_mm.lon.max(), 200)
# pp_interp = pp_mm.interp(lat=new_lat, lon=new_lon)

# # Aplicar filtro Gaussiano para suavizar los valores
# pp_smooth = gaussian_filter(pp_interp, sigma=0)

# Crear la figura
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(10, 6))

# Definir niveles y colores
levels_omega = np.linspace(0, 1400, 15)
cmap = plt.get_cmap('ocean_r')
norm = mcolors.BoundaryNorm(levels_omega, cmap.N, clip=True)

# Graficar con `contourf` en lugar de `pcolormesh`
c = ax.contourf(
    pp.lon, pp.lat, pp_mm,
    # pp_interp.lon, pp_interp.lat, pp_smooth,  # Datos interpolados y suavizados
    levels=levels_omega,
    cmap=cmap,
    norm=norm,
    transform=ccrs.PlateCarree()
)

# Crear la barra de color personalizada
cbar = plt.colorbar(c, ax=ax, orientation='vertical', pad=0.05, shrink=1, fraction=0.05, extend='both')
cbar.set_label('Precipitation (mm)', fontsize=16, labelpad=10)
cbar.set_ticks(levels_omega)
cbar.ax.tick_params(labelsize=16)

# Añadir detalles al mapa
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.LAKES, edgecolor='black')

# Establecer el extent para Brasil
ax.set_extent([-90, -30, -41, 11], crs=ccrs.PlateCarree())
# ax.set_xticks(np.arange(-90, -10, 5))
# ax.set_yticks(np.arange(-40, 21, 5))


############################# TICKS de coordenadas ############################
    
    # Configurar las etiquetas de coordenadas SIN cuadriculado
gl = ax.gridlines(draw_labels=True, linewidth=0)  # Elimina las líneas del grid
    
    # Personalizar etiquetas de los ejes
gl.xlabel_style = {'size': 14, 'color': 'black'}
gl.ylabel_style = {'size': 14, 'color': 'black'}
    
    # Configurar los localizadores de ticks desde matplotlib.ticker
gl.xlocator = mticker.FixedLocator(np.arange(-90, -29, 5))  # Longitudes fijas
gl.ylocator = mticker.FixedLocator(np.arange(-50, 21, 5))  # Latitudes fijas
    
    # Opcional: Remover etiquetas en los bordes superior e izquierdo
gl.right_labels = False
gl.top_labels = False

##########################------------------------------#################################    
    


# Agregar una letra "(f)" en el gráfico
ax.text(
    -40, 7,
    "(h)",
    fontsize=16,
    fontweight="bold",
    color="black",
    transform=ccrs.PlateCarree(),
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
)

# Agregar límites de los estados de Brasil
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none'
)
ax.add_feature(states_provinces, edgecolor='black', linestyle='--', linewidth=0.8)

# Guardar la figura
plt.savefig('C:/Users/ferfo/OneDrive/Escritorio/pp2.png', dpi=300, bbox_inches='tight')
plt.show()