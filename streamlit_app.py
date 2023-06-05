import streamlit as st
import json
import os
from datetime import datetime

# Define the exercise data and default values
exercise_data = {
    "Combo 1": [
        "Barbell bench press",
        "Cable lat pulldown",
        "Barbell Shoulder Press",
        "Barbell Underhand grip",
        "Decline bench press",
        "Cable reverse fly",
        "Bicep concentration curl",
        "Leg raises"
    ],
    "Combo 2": [
        "Barbell Squat",
        "Dummbbell Split Squat",
        "Bilateral Seated Leg Press",
        "Db Bridges",
        "Db Walking lunges",
        "Superman",
        "Db Crunches"
    ],
    "Combo 3": [
        "Db Incline chest press",
        "Db Shoulder press seated",
        "Db Incline chest fly",
        "Db Alternating lateral raise",
        "Cable bar pushdown Tricep",
        "Db Front raise",
        "Decline bench leg raises"
    ],
    "Combo 4": [
        "Reverse lat pulldown",
        "Cable Facepulls",
        "Barbell upright row",
        "Barbell Shrug",
        "Low one arm standing row",
        "Barbell bicep curl",
        "Bicep 21",
        "Cable Standing twisting crunch"
    ],
    "Combo 5": [
        "Barbell Squat",
        "Dummbbell Stiff leg deadlift",
        "Dumbbell lunge",
        "Weighted floor hip thrust",
        "lateral leg raises abduction",
        "Seated db calf raises",
        "Cable twists up down",
        "Cable side bends"
    ]
}

def load_workout_data():
    if not os.path.exists("workout_data.json"):
        return {}
    try:
        with open("workout_data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data

def save_workout_data(data):
    with open("workout_data.json", "w") as file:
        json.dump(data, file)

def add_workout_entry(day, exercise, sets, reps, weight):
    data = load_workout_data()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "day": day,
        "exercise": exercise,
        "sets": []
    }
    if day not in data:
        data[day] = []
    data[day].append(entry)

    for set_num in range(1, sets + 1):
        reps_input = st.number_input(f"Reps for Set {set_num}", value=0, step=1, key=f"{day}-{exercise}-{set_num}")
        weight_input = st.number_input(f"Weight for Set {set_num} (in kg)", value=0.0, step=0.5, key=f"{day}-{exercise}-{set_num}")

        set_entry = {
            "set": set_num,
            "reps": reps_input,
            "weight": weight_input
        }
        data[day][-1]["sets"].append(set_entry)

    save_workout_data(data)
    st.write("Workout entry added successfully.")

def display_workout_entries():
    data = load_workout_data()
    entries_by_date = {}

    # Group entries by date
    for day, entries in data.items():
        if not day.endswith("_last"):
            for entry in entries:
