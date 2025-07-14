#!/usr/bin/env python3
"""
Basic Usage Example for Tree Allometry Package

This example demonstrates the main functionality of the tree_allometry package.
"""

import sys
import os

# Add the package to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tree_allometry as ta


def main():
    print("=== Tree Allometry Package - Basic Usage Example ===\n")
    
    # 1. Species lookup examples
    print("1. Species Lookup Examples:")
    print("-" * 30)
    
    # Look up Douglas-fir
    douglas_fir_code = ta.get_species_code("Douglas-fir")
    print(f"Douglas-fir SPCD: {douglas_fir_code}")
    
    # Try scientific name
    scientific_name_code = ta.get_species_code("Pseudotsuga menziesii")
    print(f"Pseudotsuga menziesii SPCD: {scientific_name_code}")
    
    # Search for pine species
    pine_species = ta.search_species("pine")
    print(f"\nPine species found: {len(pine_species)}")
    for species in pine_species[:3]:  # Show first 3
        print(f"  - {species['name']} (SPCD: {species['spcd']})")
    
    print()
    
    # 2. Volume calculation examples
    print("2. Volume Calculation Examples:")
    print("-" * 35)
    
    # Douglas-fir example
    try:
        douglas_volume = ta.calculate_volume(
            spcd=202,           # Douglas-fir
            dbh=25.4,          # 10 inches = 25.4 cm
            height=20.0,       # 20 meters
            division="M240"    # Pacific Northwest mountains
        )
        print(f"Douglas-fir (25.4cm DBH, 20m height, M240): {douglas_volume:.3f} m³")
    except Exception as e:
        print(f"Error calculating Douglas-fir volume: {e}")
    
    # Ponderosa pine example
    try:
        ponderosa_volume = ta.calculate_volume(
            spcd=122,          # Ponderosa pine
            dbh=30.5,          # 12 inches = 30.5 cm  
            height=18.5        # 18.5 meters
        )
        print(f"Ponderosa pine (30.5cm DBH, 18.5m height): {ponderosa_volume:.3f} m³")
    except Exception as e:
        print(f"Error calculating Ponderosa pine volume: {e}")
    
    print()
    
    # 3. Species information
    print("3. Species Information:")
    print("-" * 25)
    
    try:
        douglas_info = ta.get_species_info(202)
        print(f"Douglas-fir (SPCD 202):")
        print(f"  Available divisions: {douglas_info['available_divisions']}")
        print(f"  Available models: {douglas_info['available_models']}")
        print(f"  Coefficient entries: {douglas_info['coefficient_entries']}")
    except Exception as e:
        print(f"Error getting species info: {e}")
    
    print()
    
    # 4. Available models
    print("4. Available Allometric Models:")
    print("-" * 35)
    
    models = ta.list_available_models()
    for model in models:
        print(f"Model {model['model']}: {model['description']}")
        print(f"  Equation: {model['equation']}")
        print()
    
    # 5. Batch calculation example
    print("5. Batch Calculation Example:")
    print("-" * 32)
    
    # Sample tree data
    sample_trees = [
        {"species": "Douglas-fir", "dbh": 25.4, "height": 20.0},
        {"species": "Ponderosa pine", "dbh": 30.5, "height": 18.5},
        {"species": "Western hemlock", "dbh": 20.3, "height": 15.2},
    ]
    
    print("Tree\tSpecies\t\tDBH(cm)\tHeight(m)\tVolume(m³)")
    print("-" * 60)
    
    for i, tree in enumerate(sample_trees, 1):
        try:
            spcd = ta.get_species_code(tree["species"])
            if spcd:
                volume = ta.calculate_volume(spcd, tree["dbh"], tree["height"])
                print(f"{i}\t{tree['species']:<15}\t{tree['dbh']:.1f}\t{tree['height']:.1f}\t\t{volume:.3f}")
            else:
                print(f"{i}\t{tree['species']:<15}\t{tree['dbh']:.1f}\t{tree['height']:.1f}\t\tN/A (species not found)")
        except Exception as e:
            print(f"{i}\t{tree['species']:<15}\t{tree['dbh']:.1f}\t{tree['height']:.1f}\t\tError: {e}")


if __name__ == "__main__":
    main()