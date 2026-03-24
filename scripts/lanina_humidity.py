# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:18:27 2025

@author: ferfo
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

# Configurar las líneas de la grilla y las etiquetas de coordenadas


# Ruta al archivo NetCDF
file_path = "C:/Users/ferfo/OneDrive/Escritorio/divergencia-omega/datis/humlanina.nc"

# Cargar el archivo NetCDF
ds_temp = xr.open_dataset(file_path)

# Verificar las coordenadas de latitudes y longitudes en el archivo
latitudes = ds_temp['lat'].values
longitudes = ds_temp['lon'].values

print("Latitudes disponibles:", latitudes)
print("Longitudes disponibles:", longitudes)

# Seleccionar un solo índice de tiempo (por ejemplo, el primer tiempo)
humidity_single_time = ds_temp['rhum'].isel(time=0)  # Esto reduce la dimensión de tiempo

# Seleccionar un nivel específico (por ejemplo, el primer nivel o 850 hPa)
humidity_level = humidity_single_time.isel(level=0)  # Selecciona el primer nivel

# Revisar las dimensiones de la humedad
print(humidity_level.dims)

# Ajustar los rangos de latitudes y longitudes para Sudamérica
latitude_range = slice(-60, 15)  # Latitudes de -60° a 15° para Sudamérica
longitude_range = slice(270, 330)  # Longitudes de 270° a 330° para Sudamérica (equivalente a -90° a -30°)

# Verificar los índices para las latitudes y longitudes
lat_idx = np.where((latitudes >= -60) & (latitudes <= 15))[0]
lon_idx = np.where((longitudes >= 270) & (longitudes <= 330))[0]

# Seleccionar los datos de humedad relativa usando índices
humidity_region = humidity_level.isel(lat=lat_idx, lon=lon_idx)

# Verificar si se seleccionaron datos
if humidity_region.size > 0:
    print("Datos encontrados.")
    
    # Crear el gráfico
    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([270, 330, -41, 11], crs=ccrs.PlateCarree())  # Ajustar la extensión para Sudamérica

    # Agregar características del mapa
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='black')
    # ax.set_xticks(np.arange(-90, -29, 5))
    # ax.set_yticks(np.arange(-40, 16, 5))

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
    

    # Cargar el shapefile de Brasil (asegurarse de que el archivo .shp está en la ruta correcta)
    brasil_shapefile = "C:/Users/ferfo/OneDrive/Escritorio/BR_UF_2022/BR_UF_2022.shp"  # Ajustar la ruta al archivo shapefile de Brasil
    brasil_gdf = gpd.read_file(brasil_shapefile)

    # Filtrar los estados de Brasil (no es necesario filtrar por país, ya que el shapefile solo contiene Brasil)
    # Si quieres seleccionar estados específicos, puedes hacerlo aquí por nombre, por ejemplo:
    # brasil_gdf = brasil_gdf[brasil_gdf['NM_UF'] == 'São Paulo']  # Para filtrar por un estado específico

    # Agregar los límites de los estados de Brasil al mapa
    brasil_gdf.plot(ax=ax, facecolor='none', zorder =11, linewidth =0.2)

    # Configurar niveles para la humedad relativa
    levels_humidity = np.arange(0, 91, 5)

    # Graficar la humedad relativa
    c = ax.contourf(
        humidity_region.lon,
        humidity_region.lat,
        humidity_region,
        transform=ccrs.PlateCarree(),
        cmap='terrain_r',
        extend='both',
        levels=levels_humidity
    )
    
    # Agregar un rectángulo que englobe el estado de Minas Gerais
    # Coordenadas aproximadas del límite del estado
    min_long = -51  # Longitud mínima
    max_long = -39  # Longitud máxima
    min_lat = -22   # Latitud mínima
    max_lat = -14   # Latitud máxima

    # Dibujar el rectángulo con color negro y líneas punteadas
    rect = mpatches.Rectangle(
        xy=(min_long, min_lat),  # Coordenadas de la esquina inferior izquierda
        width=(max_long - min_long),  # Ancho
        height=(max_lat - min_lat),  # Altura
        linewidth=2,
        edgecolor='black',
        linestyle='--',  # Estilo de línea punteada
        facecolor='none',
        transform=ccrs.PlateCarree()
    )
    ax.add_patch(rect)
    
    ax.text(
        -40, 7,  # Coordenadas en longitud y latitud
        "(f)",
        fontsize=18,
        fontweight="bold",
        color="black",
        transform=ccrs.PlateCarree(),
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')  # Fondo blanco con borde negro
    )
    
    # Barra de color con ticks personalizados
    cbar = plt.colorbar(c, ax=ax, orientation='vertical', pad=0.05, shrink=1, fraction=0.05)
    cbar.set_label('Relative Humidity (%)', fontsize=16, labelpad=10)
    
    # Ajustar los ticks de la barra de color de 0 a 100
    cbar.set_ticks(np.arange(0, 91, 5))  # Establecer los ticks de 0 a 100 en intervalos de 10
    cbar.ax.tick_params(labelsize=16)

    ax.xaxis.set_tick_params(labelsize=12)  # Tamaño de la etiqueta en los ejes X
    ax.yaxis.set_tick_params(labelsize=12)  # Tamaño de la etiqueta en los ejes Y

    # Guardar la figura
    plt.savefig("hum3.png", dpi=300, bbox_inches='tight')
    plt.show()

else:
    print("No se encontraron datos dentro de las coordenadas especificadas.")

# Cerrar el dataset
ds_temp.close()

