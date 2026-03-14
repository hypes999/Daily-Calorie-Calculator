import streamlit as st
from calculation import (
    calculate_bmr, 
    calculate_tdee, 
    adjust_calories_for_goal, 
    round_calories, 
    calculate_bulk_cut_ranges,
    calculate_macros,
    calculate_custom_macros
)
from utils import get_activity_levels, get_goal_options

# Set page configuration
st.set_page_config(page_title="Daily Calorie Calculator", layout="centered")

# App Header
st.title("Daily Calorie Calculator")
st.markdown("Estimate your BMR, TDEE, and daily caloric needs based on scientifically accepted energy balance estimation.")

# Sidebar / Input Form
with st.container():
    st.subheader("User Inputs")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=25, step=1)
        sex = st.selectbox("Sex", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.1)

    with col2:
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
        
        # Activity Level
        activity_levels = get_activity_levels()
        activity_choice = st.selectbox(
            "Activity Level", 
            list(activity_levels.keys()),
            help="Select the activity profile that best describes your weekly routine."
        )
        
        # Factor Slider within range
        min_factor, max_factor = activity_levels[activity_choice]["range"]
        mid_factor = (min_factor + max_factor) / 2
        activity_factor = st.slider(
            f"Select Factor for '{activity_choice}'", 
            min_value=float(min_factor), 
            max_value=float(max_factor), 
            value=float(mid_factor), 
            step=0.01,
            help=f"Range: {min_factor} to {max_factor}."
        )

    # Activity Description Panel
    st.info(f"**{activity_choice} ({min_factor}–{max_factor})**\n\n**Description:**\n{activity_levels[activity_choice]['description']}")

    # Goal Selection
    goal_options = get_goal_options()
    goal_choice = st.selectbox(
        "Select Your Primary Goal", 
        list(goal_options.keys()),
        help="This will highlight the target calories and calculate macros based on this choice."
    )
    
    # Calorie Adjustment Slider
    min_adj, max_adj = goal_options[goal_choice]["range"]
    if min_adj != max_adj:
        adjustment_val = st.slider(
            f"Adjust {goal_choice.lower()} (kcal)", 
            min_value=int(min_adj), 
            max_value=int(max_adj), 
            value=int((min_adj + max_adj) / 2),
            step=10,
            help=f"Fine-tune the caloric adjustment for your goal."
        )
    else:
        adjustment_val = 0

# Core Calculation
bmr = calculate_bmr(weight, height, age, sex)
tdee = calculate_tdee(bmr, activity_factor)
ranges = calculate_bulk_cut_ranges(tdee)

# Round values
rounded_bmr = round_calories(bmr)
rounded_tdee = round_calories(tdee)
rounded_bulk_min = round_calories(ranges['bulk'][0])
rounded_bulk_max = round_calories(ranges['bulk'][1])
rounded_cut_min = round_calories(ranges['cut'][0])
rounded_cut_max = round_calories(ranges['cut'][1])

# Selected Goal Calculation
recommended_calories = adjust_calories_for_goal(tdee, goal_choice, adjustment_val)
rounded_recommended = round_calories(recommended_calories)

# Results Section
st.divider()
st.subheader("Calculation Summary")

# Show BMR, Activity Factor, and TDEE
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.metric(
        label="BMR", 
        value=f"≈ {rounded_bmr} kcal",
        help="Basal Metabolic Rate: calories burned at rest."
    )
with col_s2:
    st.metric(
        label="Activity Factor", 
        value=f"{activity_factor:.2f}",
        help="Multiplier based on your activity level."
    )
with col_s3:
    st.metric(
        label="TDEE", 
        value=f"≈ {rounded_tdee} kcal",
        help="Total Daily Energy Expenditure (Maintenance)."
    )

st.subheader("Daily Calorie Targets")

# Always show all three targets
col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    is_selected = goal_choice == "Maintain"
    st.markdown(f"### {'Selected: ' if is_selected else ''}Maintenance")
    st.markdown(f"**≈ {rounded_tdee} kcal**")
    st.caption("(TDEE)")

with col_t2:
    is_selected = goal_choice == "Gain"
    st.markdown(f"### {'Selected: ' if is_selected else ''}Lean Bulk")
    st.markdown(f"**{rounded_bulk_min} – {rounded_bulk_max} kcal**")
    st.caption("(TDEE +150 to +300 kcal)")

with col_t3:
    is_selected = goal_choice == "Lose"
    st.markdown(f"### {'Selected: ' if is_selected else ''}Fat Loss")
    st.markdown(f"**{rounded_cut_min} – {rounded_cut_max} kcal**")
    st.caption("(TDEE −300 to −500 kcal)")

st.info(f"**Plan: {goal_choice}** — Recommended intake: **≈ {rounded_recommended} kcal**")

# Macronutrients Section
st.divider()
st.subheader("Macronutrient Settings")

# Macro Mode Toggle
macro_mode = st.radio(
    "Macro Calculation Mode",
    ["Recommended (science-based)", "Custom macro percentages"],
    help="Recommended mode uses fixed g/kg targets. Custom mode uses percentages of total calories."
)

if macro_mode == "Recommended (science-based)":
    st.markdown("""
    **Recommended mode uses evidence-based targets:**
    - Protein ≈ 2 g/kg
    - Fat ≈ 0.8 g/kg
    - Carbohydrates fill remaining calories.
    """)
    macros = calculate_macros(rounded_recommended, weight)
    # Calculate percentages for the progress bars
    total_kcal = macros['protein']['kcal'] + macros['fat']['kcal'] + macros['carbs']['kcal']
    p_pct = (macros['protein']['kcal'] / total_kcal) * 100
    f_pct = (macros['fat']['kcal'] / total_kcal) * 100
    c_pct = (macros['carbs']['kcal'] / total_kcal) * 100
else:
    st.markdown("**Custom mode allows manual macro percentage adjustment.**")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        p_pct = st.number_input("Protein %", min_value=0, max_value=100, value=30, step=1)
    with col_p2:
        f_pct = st.number_input("Fat %", min_value=0, max_value=100, value=25, step=1)
    with col_p3:
        c_pct = st.number_input("Carbs %", min_value=0, max_value=100, value=45, step=1)
    
    total_pct = p_pct + f_pct + c_pct
    if total_pct != 100:
        st.warning(f"Total percentage is {total_pct}%. It must equal 100%.")
    
    macros = calculate_custom_macros(rounded_recommended, p_pct, f_pct, c_pct)

st.subheader("Daily Macronutrient Targets")
st.markdown(f"Based on **{rounded_recommended} kcal** target.")

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.metric("Protein", f"{macros['protein']['g']} g", f"{macros['protein']['kcal']} kcal")
    if macro_mode == "Recommended (science-based)":
        st.caption("2.0 g/kg")
    else:
        st.caption(f"{p_pct}%")
with col_m2:
    st.metric("Fat", f"{macros['fat']['g']} g", f"{macros['fat']['kcal']} kcal")
    if macro_mode == "Recommended (science-based)":
        st.caption("0.8 g/kg")
    else:
        st.caption(f"{f_pct}%")
with col_m3:
    st.metric("Carbohydrates", f"{macros['carbs']['g']} g", f"{macros['carbs']['kcal']} kcal")
    if macro_mode == "Recommended (science-based)":
        st.caption("Remaining")
    else:
        st.caption(f"{c_pct}%")

# Macro Progress Bars (Visual distribution)
st.markdown("#### Energy Distribution (%)")
st.progress(p_pct / 100, text=f"Protein: {p_pct:.1f}%")
st.progress(f_pct / 100, text=f"Fat: {f_pct:.1f}%")
st.progress(c_pct / 100, text=f"Carbs: {c_pct:.1f}%")

# Informational Note
st.info(
    "Note: Daily calorie needs are estimated using BMR and activity factors. "
    "Wearable devices often have large error margins when estimating calories burned, "
    "so caloric intake should be validated by monitoring body weight trends over time."
)

# Documentation / Footer
with st.expander("Detailed Scientific Calculation"):
    st.write("**BMR Calculation (Mifflin–St Jeor Equation):**")
    st.write("- Men: BMR = (10 × weight) + (6.25 × height) − (5 × age) + 5")
    st.write("- Women: BMR = (10 × weight) + (6.25 × height) − (5 × age) − 161")
    st.write("**TDEE Calculation:** TDEE = BMR × Activity Factor")
    st.write("**Rounding:** All calorie values are rounded to the nearest 10 kcal for practical accuracy.")
    st.write("**Macro Logic (Recommended):**")
    st.write("- Protein: fixed at 2.0g per kg of body weight (4 kcal/g).")
    st.write("- Fat: fixed at 0.8g per kg of body weight (9 kcal/g).")
    st.write("- Carbs: remaining calories from the daily target (4 kcal/g).")
    st.write("**Macro Logic (Custom):**")
    st.write("- Calculated as direct percentages of the total daily calorie target.")
