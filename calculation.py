def calculate_bmr(weight, height, age, sex):
    """
    Calculates BMR using the Mifflin-St Jeor equation.
    Units: weight (kg), height (cm), age (years).
    """
    if sex.lower() == 'male':
        # BMR = (10 × weight) + (6.25 × height) − (5 × age) + 5
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        # BMR = (10 × weight) + (6.25 × height) − (5 × age) − 161
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(bmr, activity_factor):
    """
    TDEE = BMR × Activity Factor.
    This value represents maintenance calories.
    """
    return bmr * activity_factor

def round_calories(calories):
    """
    Rounds calories to the nearest 10 kcal.
    """
    return round(calories / 10) * 10

def calculate_bulk_cut_ranges(tdee):
    """
    Calculates Lean Bulk (TDEE + 150-300) and Fat Loss (TDEE - 300-500) ranges.
    """
    bulk_min = tdee + 150
    bulk_max = tdee + 300
    cut_min = tdee - 500
    cut_max = tdee - 300
    return {
        "bulk": (bulk_min, bulk_max),
        "cut": (cut_min, cut_max)
    }

def adjust_calories_for_goal(tdee, goal, adjustment_value):
    """
    Adjusts TDEE based on the user's goal.
    - Maintain weight: Daily calories = TDEE
    - Weight gain: Daily calories = TDEE + adjustment_value (150 to 300 kcal)
    - Weight loss: Daily calories = TDEE - adjustment_value (300 to 500 kcal)
    """
    if goal == 'Maintain':
        return tdee
    elif goal == 'Gain':
        return tdee + adjustment_value
    elif goal == 'Lose':
        return tdee - adjustment_value
    return tdee

def calculate_macros(total_calories, weight):
    """
    Calculates daily macronutrient targets based on total calories and body weight.
    Protein: 2.0 g/kg (range 1.6-2.2)
    Fat: 0.8 g/kg (range 0.6-1.0)
    Carbohydrates: Remaining calories / 4
    """
    protein_g = weight * 2.0
    fat_g = weight * 0.8
    
    protein_kcal = protein_g * 4
    fat_kcal = fat_g * 9
    
    remaining_kcal = total_calories - (protein_kcal + fat_kcal)
    carbs_g = max(0, remaining_kcal / 4)
    carbs_kcal = carbs_g * 4
    
    return {
        "protein": {"g": round(protein_g), "kcal": round(protein_kcal)},
        "fat": {"g": round(fat_g), "kcal": round(fat_kcal)},
        "carbs": {"g": round(carbs_g), "kcal": round(carbs_kcal)}
    }

def calculate_custom_macros(total_calories, p_pct, f_pct, c_pct):
    """
    Calculates macros based on custom percentages of total calories.
    """
    protein_kcal = total_calories * (p_pct / 100)
    fat_kcal = total_calories * (f_pct / 100)
    carbs_kcal = total_calories * (c_pct / 100)
    
    protein_g = protein_kcal / 4
    fat_g = fat_kcal / 9
    carbs_g = carbs_kcal / 4
    
    return {
        "protein": {"g": round(protein_g), "kcal": round(protein_kcal)},
        "fat": {"g": round(fat_g), "kcal": round(fat_kcal)},
        "carbs": {"g": round(carbs_g), "kcal": round(carbs_kcal)}
    }
