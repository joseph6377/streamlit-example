import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

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
        "sets": [],
    }

   for set_num in range(1, sets + 1):
        set_key = f"{day}-{exercise}-set-{set_num}"
        set_header = st.subheader(f"Set {set_num}")
        with st.expander(set_header):
            reps_input_key = f"{day}-{exercise}-reps-{set_num}"
            weight_input_key = f"{day}-{exercise}-weight-{set_num}"
            reps_input = st.number_input(f"Reps for Set {set_num}", value=0, step=1, key=reps_input_key)
            weight_input = st.number_input(f"Weight for Set {set_num} (in kg)", value=0.0, step=0.5, key=weight_input_key)
            entry["sets"].append({"reps": reps_input, "weight": weight_input})

    if day not in data:
        data[day] = []
    data[day].append(entry)
    save_workout_data(data)
    st.write("Workout entry added successfully.")


def display_workout_entries():
    data = load_workout_data()

    # Group entries by date
    entries_by_date = {}
    for day, entries in data.items():
        for entry in entries:
            date = entry["date"]
            if date not in entries_by_date:
                entries_by_date[date] = []
            entries_by_date[date].append(entry)

    # Display entries by date in a table
    for date, entries in entries_by_date.items():
        st.subheader(f"Workout Entries for Date: {date}")
        table_data = []
        header = ["Exercise", "Sets", "Reps", "Weight"]
        table_data.append(header)

        for entry in entries:
            exercise = entry["exercise"]
            sets = len(entry["sets"])
            for set_entry in entry["sets"]:
                reps = set_entry["reps"]
                weight = set_entry["weight"]
                table_data.append([exercise, sets, reps, weight])

        st.table(table_data)
        st.write()


def main():
    st.title("Workout Tracker")

    choice = st.sidebar.selectbox("Menu", ["Add a workout entry", "Display all workout entries"])

    if choice == "Add a workout entry":
        day = st.selectbox("Select a combo", list(exercise_data.keys()))
        exercise = st.selectbox("Select an exercise", exercise_data[day])
        sets = st.number_input("Enter the number of sets", value=0, step=1)

        if sets > 0:
            st.write("Enter the reps and weight for each set:")
            for set_num in range(1, sets + 1):
                st.write(f"Set {set_num}")
                reps = st.number_input("Reps", value=0, step=1, key=f"{day}-{exercise}-reps-{set_num}")
                weight = st.number_input("Weight (in kg)", value=0.0, step=0.5, key=f"{day}-{exercise}-weight-{set_num}")

        if st.button("Add Entry"):
            add_workout_entry(day, exercise, sets, reps, weight)

    elif choice == "Display all workout entries":
        display_workout_entries()

if __name__ == "__main__":
    main()
