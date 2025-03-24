import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Function to create the RandomForest model
def train_model():
    # Load datasets
    calories = pd.read_csv("calories.csv")
    exercise = pd.read_csv("exercise.csv")

    # Merge the datasets and preprocess
    exercise_df = exercise.merge(calories, on="User_ID")
    exercise_df.drop(columns="User_ID", inplace=True)

    # Add BMI column
    exercise_df["BMI"] = exercise_df["Weight"] / ((exercise_df["Height"] / 100) ** 2)
    exercise_df["BMI"] = round(exercise_df["BMI"], 2)

    # Prepare data for training
    exercise_train_data, exercise_test_data = train_test_split(exercise_df, test_size=0.2, random_state=1)

    exercise_train_data = exercise_train_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
    exercise_test_data = exercise_test_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
    exercise_train_data = pd.get_dummies(exercise_train_data, drop_first=True)
    exercise_test_data = pd.get_dummies(exercise_test_data, drop_first=True)

    X_train = exercise_train_data.drop("Calories", axis=1)
    y_train = exercise_train_data["Calories"]

    # Train Random Forest Regressor
    random_reg = RandomForestRegressor(n_estimators=1000, max_features=3, max_depth=6)
    random_reg.fit(X_train, y_train)

    return random_reg, X_train.columns


# Function to make prediction based on user input
def make_prediction():
    try:
        # Get user inputs
        age = int(age_entry.get())
        bmi = float(bmi_entry.get())
        duration = int(duration_entry.get())
        heart_rate = int(heart_rate_entry.get())
        body_temp = float(body_temp_entry.get())
        gender = 1 if gender_var.get() == "Male" else 0

        # Create a DataFrame for input features
        user_data = pd.DataFrame({
            "Age": [age],
            "BMI": [bmi],
            "Duration": [duration],
            "Heart_Rate": [heart_rate],
            "Body_Temp": [body_temp],
            "Gender_male": [gender]
        })

        # Align input with training data columns
        user_data = user_data.reindex(columns=features, fill_value=0)

        # Predict the calories burned
        prediction = model.predict(user_data)
        result_label.config(text=f"Predicted Calories Burned: {round(prediction[0], 2)} kcal")
        
        # Show graph
        plot_graph(prediction[0])

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs.")


# Function to plot a graph
def plot_graph(predicted_calories):
    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(["Predicted Calories"], [predicted_calories], color='blue')
    ax.set_ylabel("Calories (kcal)")
    ax.set_title("Calories Burned Prediction")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Initialize Tkinter window
root = tk.Tk()
root.title("Fitness Tracker")
root.geometry("500x600")
root.config(bg="black")

# Create UI components
title_label = tk.Label(root, text="Personal Fitness Tracker", font=("Arial", 16), fg="white", bg="black")
title_label.pack(pady=10)

input_frame = tk.Frame(root, bg="black")
input_frame.pack(pady=20)

# Age Input
age_label = tk.Label(input_frame, text="Age:", fg="white", bg="black")
age_label.grid(row=0, column=0, padx=5, pady=5)
age_entry = tk.Entry(input_frame)
age_entry.grid(row=0, column=1, padx=5, pady=5)

# BMI Input
bmi_label = tk.Label(input_frame, text="BMI:", fg="white", bg="black")
bmi_label.grid(row=1, column=0, padx=5, pady=5)
bmi_entry = tk.Entry(input_frame)
bmi_entry.grid(row=1, column=1, padx=5, pady=5)

# Duration Input
duration_label = tk.Label(input_frame, text="Duration (min):", fg="white", bg="black")
duration_label.grid(row=2, column=0, padx=5, pady=5)
duration_entry = tk.Entry(input_frame)
duration_entry.grid(row=2, column=1, padx=5, pady=5)

# Heart Rate Input
heart_rate_label = tk.Label(input_frame, text="Heart Rate:", fg="white", bg="black")
heart_rate_label.grid(row=3, column=0, padx=5, pady=5)
heart_rate_entry = tk.Entry(input_frame)
heart_rate_entry.grid(row=3, column=1, padx=5, pady=5)

# Body Temperature Input
body_temp_label = tk.Label(input_frame, text="Body Temperature (°C):", fg="white", bg="black")
body_temp_label.grid(row=4, column=0, padx=5, pady=5)
body_temp_entry = tk.Entry(input_frame)
body_temp_entry.grid(row=4, column=1, padx=5, pady=5)

# Gender Input
gender_var = tk.StringVar(value="Male")
gender_label = tk.Label(input_frame, text="Gender:", fg="white", bg="black")
gender_label.grid(row=5, column=0, padx=5, pady=5)
gender_radio_male = tk.Radiobutton(input_frame, text="Male", variable=gender_var, value="Male", fg="white", bg="black")
gender_radio_female = tk.Radiobutton(input_frame, text="Female", variable=gender_var, value="Female", fg="white", bg="black")
gender_radio_male.grid(row=5, column=1, padx=5, pady=5)
gender_radio_female.grid(row=5, column=2, padx=5, pady=5)

# Submit Button
submit_button = tk.Button(root, text="Predict Calories", command=make_prediction, bg="blue", fg="white")
submit_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="Predicted Calories Burned: ", font=("Arial", 14), fg="white", bg="black")
result_label.pack(pady=10)

# Graph Frame
graph_frame = tk.Frame(root, bg="black")
graph_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Train the model initially
model, features = train_model()

# Run the Tkinter app
root.mainloop()
