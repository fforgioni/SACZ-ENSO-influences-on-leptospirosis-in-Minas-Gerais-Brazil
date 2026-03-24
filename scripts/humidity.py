# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:18:27 2025

@author: ferfo
"""

from pathlib import Path
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw"
SHAPE_DIR = BASE_DIR / "data" / "shapefiles"
FIG_DIR = BASE_DIR / "figures" / "events"

FIG_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

ds = xr.open_dataset(DATA_DIR / "humlanina.nc")

# ============================================================
# SELECT DATA
# ============================================================

humidity = ds['rhum'].isel(time=0, level=0)

latitudes = humidity['lat'].values
longitudes = humidity['lon'].values

# Región Sudamérica
lat_idx = np.where((latitudes >= -60) & (latitudes <= 15))[0]
lon_idx = np.where((longitudes >= 270) & (longitudes <= 330))[0]

humidity_region = humidity.isel(lat=lat_idx, lon=lon_idx)

# ============================================================
# CHECK
# ============================================================

if humidity_region.size > 0:

    print("Datos encontrados.")

    # ============================================================
    # PLOT
    # ============================================================

    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_extent([270, 330, -41, 11], crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='black')

    # ============================================================
    # GRID LABELS
    # ============================================================

    gl = ax.gridlines(draw_labels=True, linewidth=0)

    gl.xlabel_style = {'size': 14, 'color': 'black'}
    gl.ylabel_style = {'size': 14, 'color': 'black'}

    gl.xlocator = mticker.FixedLocator(np.arange(-90, -29, 5))
    gl.ylocator = mticker.FixedLocator(np.arange(-50, 21, 5))

    gl.right_labels = False
    gl.top_labels = False

    # ============================================================
    # SHAPEFILE
    # ============================================================

    brasil_path = SHAPE_DIR / "BR_UF_2022" / "BR_UF_2022.shp"
    brasil_gdf = gpd.read_file(brasil_path)

    brasil_gdf.plot(ax=ax, facecolor='none', zorder=11, linewidth=0.2)

    # ============================================================
    # HUMIDITY
    # ============================================================

    levels_humidity = np.arange(0, 91, 5)

    c = ax.contourf(
        humidity_region.lon,
        humidity_region.lat,
        humidity_region,
        transform=ccrs.PlateCarree(),
        cmap='terrain_r',
        extend='both',
        levels=levels_humidity
    )

    # ============================================================
    # MINAS GERAIS BOX
    # ============================================================

    rect = mpatches.Rectangle(
        xy=(-51, -22),
        width=12,
        height=8,
        linewidth=2,
        edgecolor='black',
        linestyle='--',
        facecolor='none',
        transform=ccrs.PlateCarree()
    )
    ax.add_patch(rect)

    # ============================================================
    # LABEL
    # ============================================================

    ax.text(
        -40, 7,
        "(f)",
        fontsize=18,
        fontweight="bold",
        transform=ccrs.PlateCarree(),
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3')
    )

    # ============================================================
    # COLORBAR
    # ============================================================

    cbar = plt.colorbar(c, ax=ax, orientation='vertical', pad=0.05, shrink=1, fraction=0.05)
    cbar.set_label('Relative Humidity (%)', fontsize=16)
    cbar.set_ticks(np.arange(0, 91, 5))
    cbar.ax.tick_params(labelsize=16)

    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)

    # ============================================================
    # SAVE
    # ============================================================

    output_path = FIG_DIR / "hum3.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')

    plt.show()

    print(f"Saved figure to {output_path}")

else:
    print("No se encontraron datos en la región.")

# ============================================================
# CLOSE
# ============================================================

ds.close()

