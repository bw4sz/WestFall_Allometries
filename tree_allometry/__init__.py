"""
Tree Allometry Package

A Python package for calculating tree volume using FIA allometric equations.
"""

from .core import calculate_volume, get_model_info
from .species import (
    get_species_code, 
    search_species, 
    get_species_names,
    get_species_info_from_csv,
    list_all_species,
    validate_species_code
)
from .models import get_volume_coefficients

__version__ = "0.1.0"
__author__ = "Tree Allometry Package"

__all__ = [
    'calculate_volume',
    'get_model_info', 
    'get_species_code',
    'search_species',
    'get_species_names',
    'get_species_info_from_csv',
    'list_all_species',
    'validate_species_code',
    'get_volume_coefficients'
]