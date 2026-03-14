def get_activity_levels():
    """
    Returns a dictionary of activity levels with their descriptions and factor ranges.
    """
    return {
        "Sedentary": {
            "description": "Little structured exercise. Mostly sitting during the day. Low step count.",
            "range": (1.45, 1.55)
        },
        "Strength training regularly": {
            "description": "3–4 resistance training sessions per week. Low to moderate cardio. Normal daily activity.",
            "range": (1.55, 1.60)
        },
        "Strength + cardio + moderate NEAT": {
            "description": "3–5 strength training sessions. Regular cardio sessions. 7,000–12,000 daily steps.",
            "range": (1.65, 1.70)
        },
        "Very high volume / endurance athlete": {
            "description": "High training frequency. Long endurance sessions. Very high activity levels.",
            "range": (1.75, 1.90)
        }
    }

def get_goal_options():
    """
    Returns a dictionary of goal options and their kcal adjustment ranges.
    """
    return {
        "Maintain": {
            "description": "Maintain weight",
            "range": (0, 0)
        },
        "Gain": {
            "description": "Weight gain (controlled bulk)",
            "range": (150, 300)
        },
        "Lose": {
            "description": "Weight loss (fat loss)",
            "range": (300, 500)
        }
    }
