# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 16:16:35 2025

@author: ferfo
"""

from pathlib import Path
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
import matplotlib.ticker as mticker

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw"
FIG_DIR = BASE_DIR / "figures" / "events"

FIG_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

humedad = xr.open_dataset(DATA_DIR / "hum2003.nc")
uwind = xr.open_dataset(DATA_DIR / "uwnd2003-850.nc")
vwind = xr.open_dataset(DATA_DIR / "vwnd2003-850.nc")

# ============================================================
# EXTRACT VARIABLES
# ============================================================

q = humedad["shum"].isel(time=0, level=0)
temp_u = uwind["uwnd"].isel(time=0, level=0)
temp_v = vwind["vwnd"].isel(time=0, level=0)

# ============================================================
# MOISTURE TRANSPORT
# ============================================================

u = temp_u.values * units("m/s")
v = temp_v.values * units("m/s")

qu = q.values * u
qv = q.values * v

# ============================================================
# GRID DELTAS
# ============================================================

lat, lon = np.meshgrid(q["lat"], q["lon"], indexing="ij")
lat = lat * units.degrees
lon = lon * units.degrees

dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat, x_dim=-1, y_dim=-2)

# ============================================================
# DIVERGENCE
# ============================================================

divergence = mpcalc.divergence(qu, qv, dx=dx, dy=dy)

convergencia_xr = xr.DataArray(
    data=divergence.magnitude,
    dims=["lat", "lon"],
    coords={"lat": q["lat"], "lon": q["lon"]},
    attrs={"units": "1/s", "long_name": "Humidity divergence"}
)

# ============================================================
# SMOOTH
# ============================================================

suavizado = gaussian_filter(convergencia_xr, sigma=0)

# ============================================================
# PLOT
# ============================================================

fig, ax = plt.subplots(
    subplot_kw={"projection": ccrs.PlateCarree()},
    figsize=(10, 6)
)

ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5)
ax.add_feature(cfeature.LAND, edgecolor="black", facecolor="lightgray")
ax.add_feature(cfeature.LAKES, edgecolor="black", facecolor="lightblue")

ax.set_extent([270, 330, -41, 11], crs=ccrs.PlateCarree())

# ============================================================
# GRID LABELS
# ============================================================

gl = ax.gridlines(draw_labels=True, linewidth=0)

gl.xlabel_style = {"size": 14, "color": "black"}
gl.ylabel_style = {"size": 14, "color": "black"}

gl.xlocator = mticker.FixedLocator(np.arange(-90, -29, 5))
gl.ylocator = mticker.FixedLocator(np.arange(-50, 21, 5))

gl.right_labels = False
gl.top_labels = False

# ============================================================
# CONTOURF
# ============================================================

levels = np.linspace(-1.8e-7, 12e-8, 11)
cmap = plt.cm.twilight_shifted

data = ax.contourf(
    convergencia_xr.lon,
    convergencia_xr.lat,
    suavizado,
    levels,
    cmap=cmap,
    extend="both",
    transform=ccrs.PlateCarree()
)

# ============================================================
# STREAMLINES
# ============================================================

lon_grid, lat_grid = np.meshgrid(q["lon"], q["lat"])
lon_grid = np.where(lon_grid > 180, lon_grid - 360, lon_grid)

sorted_indices = np.argsort(lon_grid[0, :])
lon_grid = lon_grid[:, sorted_indices]

temp_u = temp_u[:, sorted_indices]
temp_v = temp_v[:, sorted_indices]

ax.streamplot(
    lon_grid,
    lat_grid,
    temp_u.values,
    temp_v.values,
    transform=ccrs.PlateCarree(),
    color="black",
    linewidth=0.8,
    density=3,
    arrowsize=1
)

# ============================================================
# STATES / MINAS GERAIS BOX
# ============================================================

states_provinces = cfeature.NaturalEarthFeature(
    category="cultural",
    name="admin_1_states_provinces_lines",
    scale="50m",
    facecolor="none"
)
ax.add_feature(states_provinces, edgecolor="black", linestyle="--", linewidth=1)

rect = mpatches.Rectangle(
    xy=(-51, -22),
    width=12,
    height=8,
    linewidth=2,
    edgecolor="black",
    linestyle="--",
    facecolor="none",
    transform=ccrs.PlateCarree()
)
ax.add_patch(rect)

# ============================================================
# PANEL LABEL
# ============================================================

ax.text(
    -40, 7,
    "(b)",
    fontsize=16,
    fontweight="bold",
    color="black",
    transform=ccrs.PlateCarree(),
    bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3")
)

ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)

# ============================================================
# COLORBAR
# ============================================================

cbar = plt.colorbar(
    data,
    orientation="vertical",
    pad=0.05,
    shrink=1,
    fraction=0.05,
    ax=ax
)
cbar.set_label("Humidity divergence (1/s)", fontsize=16, labelpad=10)
cbar.ax.tick_params(labelsize=16)
cbar.set_ticks(levels)

def scientific_formatter(x, _):
    return "0" if np.isclose(x, 0, atol=1e-10) else f"{x:.1e}"

formatter = FuncFormatter(scientific_formatter)
cbar.ax.yaxis.set_major_formatter(formatter)

# ============================================================
# SAVE
# ============================================================

output_path = FIG_DIR / "div-hum-2.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Saved figure to {output_path}")

# ============================================================
# CLOSE
# ============================================================

humedad.close()
uwind.close()
vwind.close()