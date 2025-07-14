"""
Species name to FIA code lookup functions.
"""

from typing import Optional, List, Dict

# Basic species mappings
SPECIES_CODES = {
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

def get_species_code(name: str) -> Optional[int]:
    """Get FIA species code from common or scientific name."""
    if not isinstance(name, str):
        return None
    normalized = name.lower().strip()
    return SPECIES_CODES.get(normalized)

def search_species(query: str) -> List[Dict]:
    """Search for species by partial name match."""
    if not isinstance(query, str):
        return []
    query_lower = query.lower().strip()
    matches = []
    seen_codes = set()
    
    for name, spcd in SPECIES_CODES.items():
        if query_lower in name and spcd not in seen_codes:
            matches.append({'name': name.title(), 'spcd': spcd})
            seen_codes.add(spcd)
    
    return sorted(matches, key=lambda x: x['name'])