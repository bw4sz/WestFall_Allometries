# Tree Allometry

A Python package for tree allometric calculations based on the Forest Inventory and Analysis (FIA) biomass modeling system.

## Overview

This package provides functions to predict tree biomass and volume components using allometric equations. It includes coefficients and models for various tree species across different geographic regions in the United States.

## Features

- **Volume Calculations**: Predict gross total stem wood volume from diameter at breast height (DBH) and total height
- **Species Lookup**: Find FIA species codes (SPCD) from common or scientific names
- **Geographic Specificity**: Region-specific coefficients for improved accuracy
- **Multiple Models**: Support for different allometric model forms

## Installation

```bash
pip install tree-allometry
```

## Quick Start

```python
import tree_allometry as ta

# Look up species code for Douglas-fir
spcd = ta.get_species_code("Douglas-fir")
print(f"Douglas-fir SPCD: {spcd}")  # Output: 202

# Calculate volume for a Douglas-fir tree
volume = ta.calculate_volume(
    spcd=202,
    dbh=25.4,  # diameter at breast height in cm
    height=20.0,  # total height in meters
    division="M240"  # geographic division (optional)
)
print(f"Estimated volume: {volume:.2f} cubic meters")
```

## Main Functions

### Volume Calculation

Calculate gross total stem wood volume inside bark using allometric equations:

```python
volume = ta.calculate_volume(spcd, dbh, height, division=None)
```

**Parameters:**
- `spcd`: FIA species code (integer)
- `dbh`: Diameter at breast height in centimeters
- `height`: Total tree height in meters  
- `division`: Optional geographic division code for region-specific coefficients

### Species Lookup

Find species codes from common or scientific names:

```python
# Using common name
spcd = ta.get_species_code("Douglas-fir")

# Using scientific name
spcd = ta.get_species_code("Pseudotsuga menziesii")

# Get species information
info = ta.get_species_info(202)
```

## Allometric Models

The package supports four different model forms:

1. **Model 1**: Volume = a × DBH^b × Height^c
2. **Model 2**: Volume = a × DBH^b × Height^c × exp(b₁/DBH + c₁ × ln(Height))
3. **Model 3**: Volume = (a + a₁ × Height) × DBH^b × Height^c
4. **Model 4**: Volume = a × DBH^b × Height^(c + c₁ × ln(DBH) + b₁ × Height)

## Example Analysis

```python
import tree_allometry as ta
import pandas as pd

# Create a sample dataset
trees = pd.DataFrame({
    'species': ['Douglas-fir', 'Ponderosa pine', 'Western hemlock'],
    'dbh': [30.5, 45.2, 25.1],
    'height': [25.3, 30.8, 22.4]
})

# Calculate volumes
trees['spcd'] = trees['species'].apply(ta.get_species_code)
trees['volume'] = trees.apply(
    lambda row: ta.calculate_volume(row['spcd'], row['dbh'], row['height']), 
    axis=1
)

print(trees)
```

## Data Sources

This package uses coefficient tables from:
- USDA Forest Service General Technical Report WO-GTR-104 Supplement 1
- Forest Inventory and Analysis (FIA) database

## Geographic Divisions

The package supports region-specific calculations using FIA geographic divisions:
- M240: Mountains (e.g., Pacific Northwest)
- M210: Northern Mountains
- M330: Southwest Mountains
- And others as defined in the FIA system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this package in your research, please cite:
```
Tree Allometry Python Package (2024). Available at: https://github.com/example/tree-allometry
```

## Disclaimer

This package is for research and educational purposes. Users should verify results and consult original sources for critical applications.
