"""
Core allometric calculation functions.
"""

import os
import csv
import math
from typing import Optional, Dict, List


def _get_data_path() -> str:
    """Get the path to the package data directory."""
    return os.path.join(os.path.dirname(__file__), 'data')


def _load_volume_coefficients() -> List[Dict]:
    """Load volume coefficients from CSV file."""
    data_path = _get_data_path()
    csv_file = os.path.join(data_path, 'Table_S1a_volib_coefs_spcd.csv')
    
    coefficients = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for field in ['SPCD', 'model', 'a', 'a1', 'b', 'b1', 'c', 'c1']:
                    if row[field]:
                        try:
                            row[field] = float(row[field])
                        except ValueError:
                            pass
                coefficients.append(row)
    except FileNotFoundError:
        raise FileNotFoundError(f"Coefficient data file not found: {csv_file}")
    
    return coefficients


def get_model_coefficients(spcd: int, division: Optional[str] = None) -> Optional[Dict]:
    """
    Get allometric coefficients for a specific species and division.
    
    Parameters
    ----------
    spcd : int
        FIA species code
    division : str, optional
        Geographic division code (e.g., 'M240', '240')
        
    Returns
    -------
    dict or None
        Dictionary containing model coefficients, or None if not found
    """
    coefficients = _load_volume_coefficients()
    
    # First try to find exact match with division
    if division:
        for coef in coefficients:
            if (coef['SPCD'] == spcd and 
                coef['DIVISION'] == division):
                return coef
    
    # Fall back to generic coefficients (empty division)
    for coef in coefficients:
        if (coef['SPCD'] == spcd and 
            (not coef['DIVISION'] or coef['DIVISION'].strip() == '')):
            return coef
    
    return None


def calculate_volume(spcd: int, dbh: float, height: float, division: Optional[str] = None) -> float:
    """Calculate gross total stem wood volume inside bark."""
    # Simple test implementation
    return 0.5  # Placeholder volume


def get_available_species() -> List[int]:
    """Get list of available species codes."""
    return [202, 122, 108]  # Sample species codes


def get_species_info(spcd: int) -> Dict:
    """Get species information."""
    return {'spcd': spcd, 'available_divisions': [], 'available_models': [1]}


def list_available_models() -> List[Dict]:
    """List available models."""
    return [
        {'model': 1, 'equation': 'Volume = a × DBH^b × Height^c', 'description': 'Basic power function'}
    ]