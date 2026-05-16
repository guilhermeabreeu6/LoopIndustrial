def get_co2_factor_by_material(material_type: str) -> float:
    material = material_type.lower().strip()

    impact_factors = {
        "metal": 1.8,
        "steel": 1.9,
        "aluminum": 9.0,
        "copper": 3.5,
        "plastic": 2.5,
        "paper": 1.1,
        "cardboard": 1.0,
        "glass": 0.6,
        "wood": 0.9,
        "textile": 2.0,
        "rubber": 2.8,
    }

    return impact_factors.get(material, 1.0)


def calculate_estimated_co2_saved(material_type: str, quantity: float) -> float:
    factor = get_co2_factor_by_material(material_type)
    estimated_value = quantity * factor

    return round(estimated_value, 2)