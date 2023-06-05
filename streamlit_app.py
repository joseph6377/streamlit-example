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

def add_workout_entry(day, exercise, reps, weight):
    data = load_workout_data()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "day": day,
        "exercise": exercise,
        "sets": [],
    }

    entry["sets"].append({"reps": reps, "weight": weight})

    if day not in data:
        data[day] = []
    data[day].append(entry)
    save_workout_data(data)
    st.write("Workout entry added successfully.")

def display_workout_entries():
    workout_entries = []
    data = load_workout_data()

    for day, entries in data.items():
        workout_entries.extend(entries)

    if not workout_entries:
        st.write("No workout entries found.")
    else:
        workout_entries = sorted(workout_entries, key=lambda x: (x["date"], x["exercise"]), reverse=True)
        grouped_entries = {}

        for entry in workout_entries:
            date = entry["date"]
            exercise = entry["exercise"]
            key = (date, exercise)
            if key not in grouped_entries:
                grouped_entries[key] = []
            grouped_entries[key].append(entry)

        st.write("Here are all your workout entries:")

        for (date, exercise), entries in grouped_entries.items():
            st.subheader(date)
            st.write(f"Exercise: {exercise}")
            st.write(f"Number of Sets: {len(entries)}")

            for entry in entries:
                set_data = entry["sets"][0]
                reps = set_data.get("reps", 0)
                weight = set_data.get("weight", 0)
                st.write(f"Set: Reps={reps}, Weight={weight} kg")

            st.write("---")

def main():
    st.title("Workout Tracker")

    choice = st.sidebar.selectbox("Menu", ["Add a workout entry", "Display all workout entries"])

    if choice == "Add a workout entry":
        day = st.selectbox("Select a combo", list(exercise_data.keys()))
        exercise = st.selectbox("Select an exercise", exercise_data[day])
        reps = st.number_input("Reps", value=0, step=1)
        weight = st.number_input("Weight (in kg)", value=0.0, step=0.5)

        if st.button("Add Entry"):
            add_workout_entry(day, exercise, reps, weight)

    elif choice == "Display all workout entries":
        display_workout_entries()

if __name__ == "__main__":
    main()
