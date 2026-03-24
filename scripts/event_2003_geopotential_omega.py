

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

# Ruta al archivo NetCDF de humedad
file_path_humidity = "C:/Users/ferfo/OneDrive/Escritorio/omega2003.nc"

# Ruta al archivo NetCDF de geopotencial (ajusta la ruta)
file_path_geopotential = "C:/Users/ferfo/OneDrive/Escritorio/geop2003.nc"

# Cargar el archivo NetCDF de humedad
ds_temp_humidity = xr.open_dataset(file_path_humidity)

# Cargar el archivo NetCDF de geopotencial
ds_temp_geopotential = xr.open_dataset(file_path_geopotential)

# Verificar las coordenadas de latitudes y longitudes en el archivo de humedad
latitudes = ds_temp_humidity['lat'].values
longitudes = ds_temp_humidity['lon'].values

# Seleccionar un solo índice de tiempo (por ejemplo, el primer tiempo) para la humedad
humidity_single_time = ds_temp_humidity['omega'].isel(time=0)

# Seleccionar un nivel específico para la humedad
humidity_level = humidity_single_time.isel(level=0)  # Ajusta el nivel según corresponda

# Seleccionar un índice de tiempo para el geopotencial (ajustar si es diferente)
geopotential_single_time = ds_temp_geopotential['hgt'].isel(time=0)

# Seleccionar un nivel específico para el geopotencial
geopotential_level = geopotential_single_time.isel(level=0)  # Ajusta el nivel según corresponda

# Ajustar los rangos de latitudes y longitudes para Sudamérica
latitude_range = slice(-60, 15)  # Latitudes de -60° a 15° para Sudamérica
longitude_range = slice(270, 330)  # Longitudes de 270° a 330° para Sudamérica

# Verificar los índices para las latitudes y longitudes
lat_idx = np.where((latitudes >= -60) & (latitudes <= 15))[0]
lon_idx = np.where((longitudes >= 270) & (longitudes <= 330))[0]

# Seleccionar los datos de la humedad usando los índices
humidity_region = humidity_level.isel(lat=lat_idx, lon=lon_idx)

# Seleccionar los datos de geopotencial usando los índices
geopotential_region = geopotential_level.isel(lat=lat_idx, lon=lon_idx)

# Verificar si se seleccionaron datos
if humidity_region.size > 0 and geopotential_region.size > 0:
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

    # Cargar el shapefile de Brasil
    brasil_shapefile = "C:/Users/ferfo/OneDrive/Escritorio/BR_UF_2022/BR_UF_2022.shp"
    brasil_gdf = gpd.read_file(brasil_shapefile)

    # Filtrar los estados de Brasil
    brasil_gdf.plot(ax=ax, facecolor='none', zorder=11, linewidth=0.2)

    # Graficar la humedad relativa
    levels_humidity = np.arange(-0.09, 0.1, 0.02)
    c = ax.contourf(
        humidity_region.lon,
        humidity_region.lat,
        humidity_region,
        transform=ccrs.PlateCarree(),
        cmap='coolwarm',
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
    # Agregar el contorno de geopotencial
    levels_geopotential = np.arange(5000, 5900, 20)  # Ajusta los niveles de geopotencial según sea necesario
    contours = ax.contour(
        geopotential_region.lon,
        geopotential_region.lat,
        geopotential_region,
        transform=ccrs.PlateCarree(),
        colors='black',  # Color del contorno
        levels=levels_geopotential,
        zorder=11,
        linewidths=0.9  # Grosor de la línea del contorno
    )
    
    ax.text(
        -40, 7,  # Coordenadas en longitud y latitud
        "(g)",
        fontsize=18,
        fontweight="bold",
        color="black",
        transform=ccrs.PlateCarree(),
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')  # Fondo blanco con borde negro
    )
    # Agregar etiquetas de los contornos de geopotencial
    ax.clabel(contours, inline=True, fontsize=12, fmt='%d', colors='black', inline_spacing=8)

    # Barra de color para la humedad
    cbar = plt.colorbar(c, ax=ax, orientation='vertical', pad=0.05, shrink=1, fraction=0.05)
    cbar.set_label('Omega (Pa/s))', fontsize=16, labelpad=10)
    cbar.ax.tick_params(labelsize=16)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=16)

    # Guardar la figura
    plt.savefig("geop-omega1.png", dpi=300, bbox_inches='tight')
    plt.show()

else:
    print("No se encontraron datos dentro de las coordenadas especificadas.")

# Cerrar los datasets
ds_temp_humidity.close()
ds_temp_geopotential.close()



