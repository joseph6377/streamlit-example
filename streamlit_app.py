import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re
import webbrowser

# Define the exercise data and default values
exercise_data = {
    "Chest + Back": [
        "Barbell bench press",
        "Cable lat pull down",
        "Barbell Shoulder Press",
        "Barbell Underhand grip",
        "Decline bench press",
        "Cable reverse fly",
        "Bicep concentration curl",
        "Leg raises"
    ],
    "Leg + Abs": [
        "Leg",
        "Dumbbell Split Squat",
        "Bilateral Seated Leg Press",
        "Db Bridges",
        "Db Walking lunges",
        "Superman",
        "Db Crunches"
    ],
    "Chest + Triceps": [
        "Db Incline chest press",
        "Db Shoulder press seated",
        "Db Incline chest fly",
        "Db Alternating lateral raise",
        "Cable bar pushdown Tricep",
        "Db Front raise",
        "Decline bench leg raises"
    ],
    "Back + Biceps": [
        "Reverse lat pull down",
        "Cable Face pulls",
        "Barbell upright row",
        "Barbell Shrug",
        "Low one arm standing row",
        "Barbell bicep curl",
        "Bicep 21",
        "Cable Standing twisting crunch"
    ],
    "Legs": [
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

def load_workout_data(email):
    filename = f"workout_data_{email}.json"
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return data

def save_workout_data(email, data):
    filename = f"workout_data_{email}.json"
    with open(filename, "w") as file:
        json.dump(data, file)

def add_workout_entry(email, day, exercise, reps, weight):
    data = load_workout_data(email)
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
    save_workout_data(email, data)
    st.write("Workout entry added successfully.")

def display_workout_entries(email):
    workout_entries = []
    data = load_workout_data(email)

    for day, entries in data.items():
        workout_entries.extend(entries)

    if not workout_entries:
        st.write("No workout entries found.")
    else:
        workout_entries = sorted(workout_entries, key=lambda x: (x["date"], x["exercise"]))
        grouped_entries = {}

        for entry in workout_entries:
            date_str = datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d %y (%a)")
            exercise = entry["exercise"]
            key = (date_str, exercise)
            if key not in grouped_entries:
                grouped_entries[key] = []
            grouped_entries[key].append(entry)

        st.write("Here are all your workout entries:")

        table_data = []
        exercise_volumes = {}  # To store exercise volumes

        for (date_str, exercise), entries in grouped_entries.items():
            total_sets = 0
            total_reps = 0
            total_weight = 0
            for i, entry in enumerate(entries, start=1):
                sets = entry["sets"]
                num_sets = len(sets)
                reps_list = [set_data.get("reps", 0) for set_data in sets]
                weight_list = [set_data.get("weight", 0) for set_data in sets]
                total_sets += num_sets
                total_reps += sum(reps_list)
                total_weight += sum(weight_list)
                table_data.append((date_str, exercise, num_sets, reps_list, weight_list))

            # Calculate exercise volume
            volume = total_sets * total_reps * total_weight
            if exercise not in exercise_volumes:
                exercise_volumes[exercise] = []
            exercise_volumes[exercise].append((datetime.strptime(date_str, "%b %d %y (%a)"), volume))

        # Display table
        df = pd.DataFrame(table_data, columns=["Date", "Exercise", "Number of Sets", "Reps", "Weight"])
        st.dataframe(df)

        # Plot exercise volumes
        if st.button("Plot Exercise Volumes"):
            plt.figure(figsize=(10, 6))
            for exercise, volumes in exercise_volumes.items():
                dates = [x[0] for x in volumes]
                volume = [x[1] for x in volumes]
                plt.plot(dates, volume, label=exercise)
            plt.xlabel("Date")
            plt.ylabel("Exercise Volume")
            plt.title("Exercise Volume over Time")
            plt.legend()
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d %y (%a)"))  # Format x-axis dates
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # Set x-axis tick frequency to daily
            plt.xticks(rotation=45)
            st.pyplot(plt)



def login():
    st.title("Welcome to Workout Tracker by Jo")

    st.sidebar.write("Enter your email ID and click Enter to start tracking your workout.")

    email_placeholder = st.sidebar.empty()
    email = email_placeholder.text_input("Email", key="email")

    # Email format validation
    email_valid = re.match(r"[^@]+@[^@]+\.[^@]+", email) if email else False

    if email and email_valid:
        email_placeholder.empty()  # Remove the email input field
        st.sidebar.success(f"Logged in as: {email}")
        if st.sidebar.button("Log Out"):
            webbrowser.open("https://www.google.com")  # Open google.com in the browser
        else:
            main(email)
    elif email and not email_valid:
        st.sidebar.warning("Please enter a valid email address")

def main(email):


    choice = st.selectbox("Select below to add or view past workouts and Graphs!", ["Add a workout entry","Display all workout entries"])

    if choice == "Add a workout entry":
        day = st.selectbox("Select a combo", list(exercise_data.keys()))
        exercise = st.selectbox("Select an exercise", exercise_data[day])
        reps = st.number_input("Reps", value=0, step=5)
        weight = st.number_input("Weight (in kg)", value=0.0, step=2.5)

        if st.button("Add Entry"):
            add_workout_entry(email, day, exercise, reps, weight)
            st.write("")  # Add an empty line for spacing

    elif choice == "Display all workout entries":
        display_workout_entries(email)

    st.write("")  # Add an empty line for spacing

if __name__ == "__main__":
    login()
