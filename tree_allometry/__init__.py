"""
Tree Allometry Package

A Python package for tree allometric calculations based on the FIA biomass modeling system.
"""

from .core import calculate_volume, get_available_species, get_species_info
from .species import get_species_code, search_species  
from .models import get_model_coefficients, list_available_models

__version__ = "0.1.0"
__author__ = "Tree Allometry Project"

__all__ = [
    "calculate_volume",
    "get_species_code", 
    "search_species",
    "get_available_species",
    "get_species_info",
    "get_model_coefficients",
    "list_available_models",
]