# SACZ–ENSO influences on leptospirosis in Minas Gerais, Brazil

This repository contains the code and analysis used in the manuscript:

**Dutra et al. (2026)**  
*"Linking climate variability, topography, and health: SACZ–ENSO influences on leptospirosis in Minas Gerais, Brazil"* :contentReference[oaicite:0]{index=0}

---

## 📌 Overview

This study investigates how large-scale climate variability, particularly the South Atlantic Convergence Zone (SACZ) and its modulation by the El Niño–Southern Oscillation (ENSO), interacts with regional geomorphological features to influence precipitation extremes and leptospirosis outbreaks in Minas Gerais, Brazil.

The analysis integrates:
- Atmospheric circulation diagnostics (multi-level fields)
- Hydroclimatic variability (precipitation and moisture transport)
- Geomorphological controls on runoff and flooding
- Epidemiological records of leptospirosis incidence

The results highlight how multiscale interactions between climate, topography, and vulnerability amplify flood-related disease risk.

---

## 🔬 Methods implemented in this repository

The repository includes scripts for:

- Identification and analysis of SACZ events (DJF, 2002–2012)
- ENSO classification based on Niño 3.4 SST anomalies  
- Composite analysis of atmospheric fields:
  - Temperature
  - Relative humidity
  - Geopotential height
  - Vertical velocity (omega)
  - Moisture divergence
  - Wind divergence
- Case study analysis (e.g., 2003 and 2012 events)
- Integration with leptospirosis incidence data
- Figure generation for publication

---

## 📂 Repository structure
scripts/ # Main analysis scripts
data/ # (Not included) Input datasets
figures/ # Output figures


---

## 📊 Data

Due to their size and/or access restrictions, datasets are not included in this repository.

They can be obtained from:

- NCEP/NCAR Reanalysis 1:  
  https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html  

- Sea Surface Temperature (ERSSTv5):  
  https://www.ncei.noaa.gov/products/extended-reconstructed-sst  

- Topographic data (TOPODATA / SRTM):  
  http://www.dsr.inpe.br/topodata  

- Epidemiological data (DATASUS):  
  https://datasus.saude.gov.br/  

---

## ⚙️ Requirements

- Python 3.x  
- numpy  
- pandas  
- xarray  
- matplotlib  
- cartopy  

---

## ▶️ How to run

1. Preprocess climate and epidemiological datasets  
2. Identify SACZ events and ENSO phases  
3. Compute composites and anomalies  
4. Generate figures and diagnostics  

---

## 🌎 Key scientific contribution

This work provides an integrated framework linking:

- Synoptic-scale climate variability (SACZ–ENSO)  
- Regional geomorphology  
- Hydrological responses  
- Public health outcomes  

It demonstrates that terrain acts as a **first-order amplifier** of climate–health interactions, particularly in southeastern Minas Gerais.

---

## 📄 Citation

If you use this code, please cite:

Dutra et al. (2026)  
*"Linking climate variability, topography, and health: SACZ–ENSO influences on leptospirosis in Minas Gerais, Brazil"* :contentReference[oaicite:1]{index=1}

---

## ⚖️ License

This project is licensed under the MIT License.
