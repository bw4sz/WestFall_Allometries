"""
Species name to FIA code lookup functions.
"""

import os
import csv
from typing import Optional, List, Dict


def _get_data_path() -> str:
    """Get the path to the package data directory."""
    return os.path.join(os.path.dirname(__file__), 'data')


def _load_species_codes() -> Dict[str, int]:
    """Load species codes from CSV file."""
    data_path = _get_data_path()
    csv_file = os.path.join(data_path, 'fia_species_codes.csv')
    
    species_codes = {}
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    spcd = int(row['SPCD'])
                    common_name = row['COMMON_NAME'].lower().strip()
                    scientific_name = row['SCIENTIFIC_NAME'].lower().strip()
                    
                    # Add common name
                    species_codes[common_name] = spcd
                    
                    # Add scientific name
                    species_codes[scientific_name] = spcd
                    
                    # Add variations of common name
                    # Replace hyphens with spaces and vice versa
                    if '-' in common_name:
                        species_codes[common_name.replace('-', ' ')] = spcd
                    if ' ' in common_name:
                        species_codes[common_name.replace(' ', '-')] = spcd
                    
                    # Add genus + species format
                    genus = row['GENUS'].lower().strip()
                    species = row['SPECIES'].lower().strip()
                    if genus and species and species != 'spp.' and species != 'unknown':
                        species_codes[f"{genus} {species}"] = spcd
                        
                except (ValueError, KeyError):
                    continue
                    
    except FileNotFoundError:
        # Fallback to basic species codes if file not found
        species_codes = {
            "douglas-fir": 202,
            "douglas fir": 202,
            "pseudotsuga menziesii": 202,
            "ponderosa pine": 122,
            "pinus ponderosa": 122,
            "lodgepole pine": 108,
            "pinus contorta": 108,
            "western hemlock": 263,
            "tsuga heterophylla": 263,
        }
    
    return species_codes


# Load species codes once when module is imported
_SPECIES_CODES = _load_species_codes()


def get_species_code(name: str) -> Optional[int]:
    """
    Get FIA species code from common or scientific name.
    
    Parameters
    ----------
    name : str
        Common name or scientific name (case insensitive)
        
    Returns
    -------
    int or None
        FIA species code (SPCD) if found, None otherwise
        
    Examples
    --------
    >>> get_species_code("Douglas-fir")
    202
    >>> get_species_code("Pseudotsuga menziesii") 
    202
    >>> get_species_code("ponderosa pine")
    122
    """
    if not isinstance(name, str):
        return None
    
    normalized = name.lower().strip()
    
    # Direct lookup
    if normalized in _SPECIES_CODES:
        return _SPECIES_CODES[normalized]
    
    # Try with variations
    variations = [
        normalized.replace("-", " "),  # douglas-fir -> douglas fir
        normalized.replace(" ", "-"),  # douglas fir -> douglas-fir
        normalized.replace("_", " "),  # douglas_fir -> douglas fir
        normalized.replace(".", ""),   # remove periods
    ]
    
    for variation in variations:
        if variation in _SPECIES_CODES:
            return _SPECIES_CODES[variation]
    
    return None


def search_species(query: str) -> List[Dict]:
    """
    Search for species by partial name match.
    
    Parameters
    ----------
    query : str
        Search query (case insensitive)
        
    Returns
    -------
    list of dict
        List of matching species with 'name' and 'spcd' keys
        
    Examples
    --------
    >>> results = search_species("pine")
    >>> for result in results:
    ...     print(f"{result['name']} (SPCD: {result['spcd']})")
    """
    if not isinstance(query, str):
        return []
    
    query_lower = query.lower().strip()
    if not query_lower:
        return []
    
    matches = []
    seen_codes = set()
    
    for name, spcd in _SPECIES_CODES.items():
        if query_lower in name and spcd not in seen_codes:
            matches.append({'name': name.title(), 'spcd': spcd})
            seen_codes.add(spcd)
    
    return sorted(matches, key=lambda x: x['name'])


def get_species_names(spcd: int) -> List[str]:
    """
    Get all known names (common and scientific) for a species code.
    
    Parameters
    ----------
    spcd : int
        FIA species code
        
    Returns
    -------
    list of str
        List of known names for the species
    """
    names = []
    
    for name, code in _SPECIES_CODES.items():
        if code == spcd:
            names.append(name.title())
    
    return sorted(list(set(names)))  # Remove duplicates and sort


def get_species_info_from_csv(spcd: int) -> Optional[Dict]:
    """
    Get detailed species information from CSV file.
    
    Parameters
    ----------
    spcd : int
        FIA species code
        
    Returns
    -------
    dict or None
        Species information or None if not found
    """
    data_path = _get_data_path()
    csv_file = os.path.join(data_path, 'fia_species_codes.csv')
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['SPCD']) == spcd:
                    return {
                        'spcd': spcd,
                        'common_name': row['COMMON_NAME'],
                        'genus': row['GENUS'],
                        'species': row['SPECIES'],
                        'scientific_name': row['SCIENTIFIC_NAME']
                    }
    except (FileNotFoundError, ValueError, KeyError):
        pass
    
    return None


def list_all_species() -> List[Dict]:
    """
    Get a list of all available species in the database.
    
    Returns
    -------
    list of dict
        List of all species with name and SPCD
    """
    data_path = _get_data_path()
    csv_file = os.path.join(data_path, 'fia_species_codes.csv')
    
    species_list = []
    
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                species_list.append({
                    'name': row['COMMON_NAME'],
                    'spcd': int(row['SPCD']),
                    'scientific_name': row['SCIENTIFIC_NAME']
                })
    except (FileNotFoundError, ValueError, KeyError):
        # Fallback to basic list
        species_list = [
            {'name': 'Douglas-fir', 'spcd': 202, 'scientific_name': 'Pseudotsuga menziesii'},
            {'name': 'Ponderosa pine', 'spcd': 122, 'scientific_name': 'Pinus ponderosa'},
        ]
    
    return sorted(species_list, key=lambda x: x['name'])


def validate_species_code(spcd: int) -> bool:
    """
    Check if a species code exists in our database.
    
    Parameters
    ----------
    spcd : int
        FIA species code to validate
        
    Returns
    -------
    bool
        True if species code is known, False otherwise
    """
    return spcd in _SPECIES_CODES.values()