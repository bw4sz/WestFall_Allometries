"""
Allometric model definitions and coefficient management.
"""

from typing import List, Dict, Optional

def get_model_coefficients(spcd: int, division: Optional[str] = None) -> Optional[Dict]:
    """Get allometric coefficients for a specific species and division."""
    # Sample coefficient data for testing
    if spcd == 202:  # Douglas-fir
        return {
            'SPCD': 202,
            'model': 1,
            'a': 0.001707245,
            'b': 1.907559079,
            'c': 1.698695714
        }
    return None

def list_available_models() -> List[Dict]:
    """List all available allometric model descriptions."""
    return [
        {
            'model': 1,
            'equation': 'Volume = a × DBH^b × Height^c',
            'description': 'Basic power function model'
        },
        {
            'model': 2, 
            'equation': 'Volume = a × DBH^b × Height^c × exp(b₁/DBH + c₁×ln(Height))',
            'description': 'Power function with exponential correction'
        }
    ]


def get_model_description(model_number: int) -> Optional[Dict]:
    """
    Get description for a specific model number.
    
    Parameters
    ----------
    model_number : int
        Model number (1-4)
        
    Returns
    -------
    dict or None
        Model description or None if not found
    """
    models = _list_available_models()
    
    for model in models:
        if model['model'] == model_number:
            return model
    
    return None


def validate_coefficients(coefficients: Dict) -> bool:
    """
    Validate that a coefficient dictionary has required fields.
    
    Parameters
    ----------
    coefficients : dict
        Dictionary of model coefficients
        
    Returns
    -------
    bool
        True if coefficients are valid, False otherwise
    """
    required_fields = ['SPCD', 'model', 'a', 'b', 'c']
    
    for field in required_fields:
        if field not in coefficients:
            return False
        if coefficients[field] is None:
            return False
    
    # Check model number is valid
    model_num = coefficients.get('model')
    if not isinstance(model_num, (int, float)) or model_num not in [1, 2, 3, 4]:
        return False
    
    return True