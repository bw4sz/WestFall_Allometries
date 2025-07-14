"""
Basic tests for tree_allometry package.
"""

import sys
import os

# Add the package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tree_allometry as ta


def test_species_lookup():
    """Test species code lookup functionality."""
    # Test Douglas-fir lookup
    assert ta.get_species_code("Douglas-fir") == 202
    assert ta.get_species_code("douglas-fir") == 202
    assert ta.get_species_code("DOUGLAS-FIR") == 202
    
    # Test scientific name
    assert ta.get_species_code("Pseudotsuga menziesii") == 202
    
    # Test Ponderosa pine
    assert ta.get_species_code("Ponderosa pine") == 122
    assert ta.get_species_code("Pinus ponderosa") == 122
    
    # Test non-existent species
    assert ta.get_species_code("Fake tree") is None
    assert ta.get_species_code("") is None
    assert ta.get_species_code(None) is None


def test_species_search():
    """Test species search functionality."""
    # Search for pine species
    pine_results = ta.search_species("pine")
    assert len(pine_results) > 0
    
    # Check result format
    for result in pine_results:
        assert 'name' in result
        assert 'spcd' in result
        assert isinstance(result['spcd'], int)
        assert isinstance(result['name'], str)
    
    # Search for non-existent
    no_results = ta.search_species("xyz123")
    assert len(no_results) == 0


def test_volume_calculation():
    """Test volume calculation functionality."""
    # Test basic volume calculation
    volume = ta.calculate_volume(202, 25.4, 20.0)  # Douglas-fir
    assert volume > 0
    assert isinstance(volume, float)
    
    # Test with division
    volume_with_div = ta.calculate_volume(202, 25.4, 20.0, "M240")
    assert volume_with_div > 0
    
    # Test invalid inputs
    try:
        ta.calculate_volume(202, -10, 20.0)  # Negative DBH
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        ta.calculate_volume(202, 25.4, -5)  # Negative height
        assert False, "Should raise ValueError"  
    except ValueError:
        pass
    
    try:
        ta.calculate_volume(99999, 25.4, 20.0)  # Non-existent species
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_available_species():
    """Test getting available species."""
    species_list = ta.get_available_species()
    assert len(species_list) > 0
    assert isinstance(species_list, list)
    assert all(isinstance(spcd, int) for spcd in species_list)
    
    # Check Douglas-fir is in the list
    assert 202 in species_list


def test_species_info():
    """Test getting species information."""
    # Test Douglas-fir info
    info = ta.get_species_info(202)
    assert isinstance(info, dict)
    assert 'spcd' in info
    assert 'available_divisions' in info
    assert 'available_models' in info
    assert 'coefficient_entries' in info
    
    assert info['spcd'] == 202
    assert isinstance(info['available_divisions'], list)
    assert isinstance(info['available_models'], list)
    assert info['coefficient_entries'] > 0
    
    # Test non-existent species
    try:
        ta.get_species_info(99999)
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_models():
    """Test model-related functions."""
    # Test list available models
    models = ta.list_available_models()
    assert len(models) == 4  # Should have 4 models
    
    for model in models:
        assert 'model' in model
        assert 'equation' in model
        assert 'description' in model
        assert model['model'] in [1, 2, 3, 4]
    
    # Test get model coefficients
    coefs = ta.get_model_coefficients(202)  # Douglas-fir
    if coefs:  # If coefficients exist
        assert 'SPCD' in coefs
        assert 'model' in coefs
        assert 'a' in coefs
        assert 'b' in coefs
        assert 'c' in coefs


def test_integration():
    """Test integration between different components."""
    # Find Douglas-fir code
    spcd = ta.get_species_code("Douglas-fir")
    assert spcd == 202
    
    # Get info for that species
    info = ta.get_species_info(spcd)
    assert info['spcd'] == spcd
    
    # Calculate volume
    volume = ta.calculate_volume(spcd, 25.4, 20.0)
    assert volume > 0


if __name__ == "__main__":
    # Run tests manually if called directly
    test_functions = [
        test_species_lookup,
        test_species_search, 
        test_volume_calculation,
        test_available_species,
        test_species_info,
        test_models,
        test_integration,
    ]
    
    print("Running tests...")
    
    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
        except Exception as e:
            print(f"✗ {test_func.__name__}: {e}")
    
    print("Tests completed!")