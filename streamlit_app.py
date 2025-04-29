import streamlit as st
import requests
import matplotlib.pyplot as plt
import time
import pandas as pd
import sqlite3
import bcrypt
#import streamlit_authenticator as stauth
#import pickle
#from pathlib import Path

st.set_page_config(page_title="Calorie Burn Predictor",page_icon="calories.ico")

# Connect to SQLite database
conn = sqlite3.connect('calorie_history.db', check_same_thread=False)
c = conn.cursor()

# Create users table if not exists (to store usernames and hashed passwords)
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()
# Create calorie history table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        gender TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        duration INTEGER,
        heart_rate INTEGER,
        body_temp REAL,
        calories_burned REAL
    )
''')
conn.commit()

def Show_Splash_Screen():
    splash = st.empty()  
    splash.markdown("""
        <div style='text-align: center; margin-top: 250px;'>
            <h1>Welcome to Calories Burn Predictor</h1>
            <p>Loading, please wait...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    splash.empty()

def Show_Sign_Up_Screen():
    st.title("📝 Sign Up")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Register"):
        if not new_username or not new_password or not confirm_password:
            st.warning("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            c.execute("SELECT * FROM users WHERE username = ?", (new_username,))
            if c.fetchone():
                st.error("Username already exists.")
            else:
                hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, hashed))
                conn.commit()
                st.success("Account created! Please log in.")
                st.session_state.show_signup = False
                st.rerun()

    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()
        
def Show_Login_Screen():
    st.title("🔐 Login")

    username = st.text_input("Enter your Username")
    password = st.text_input("Enter your Password", type="password")

    if st.button("Login"):
        if username and password:
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            if user and bcrypt.checkpw(password.encode(), user[2].encode()):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please fill in all fields.")

    if st.button("Forgot Password?"):
        st.session_state.forgot_password = True
        st.rerun()

    st.markdown("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.show_signup = True
        st.session_state.logged_in = False
        st.rerun()

def Show_Forgot_Password_Screen():
    st.title("🔑 Forgot Password")

    username = st.text_input("Enter your username")
    new_password = st.text_input("Enter new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")

    if st.button("Reset Password"):
        if not username or not new_password or not confirm_password:
            st.error("Please fill in all fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            if c.fetchone():
                hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_pw, username))
                conn.commit()
                st.success("Password reset successfully. Please login.")
                st.session_state.forgot_password = False
                st.rerun()
            else:
                st.error("Username not found.")

    if st.button("Back to Login"):
        st.session_state.forgot_password = False
        st.rerun()
        
def Show_Main_Screen():
    
    st.title("🔥 Calorie Burn Predictor")
    api_url = "https://electibz-api.onrender.com/predict/"
    if "history" not in st.session_state:
        st.session_state.history = []
    
    # User Inputs
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    duration = st.number_input("Workout Duration (minutes)", min_value=1, max_value=300, value=30)
    heart_rate = st.number_input("Heart Rate", min_value=30, max_value=200, value=100)
    body_temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=37.0, step=1.0)
    
    if st.button("Predict Calories Burned"):
        data = [{
        "Gender": 1 if gender.lower() == "male" else 0,
        "Age": age,
        "Height": height,
        "Weight": weight,
        "Duration": duration,
        "Heart_Rate": heart_rate,
        "Body_Temp": body_temp
    }]

    
        with st.spinner("Sending data to API..."):
            response = requests.post(api_url, json=data)

        if response.status_code == 200:
            prediction = response.json()["Predicted Calories"][0]
            st.success(f"🔥 Estimated Calories Burned: {prediction:.2f}")
            # Save to history
            st.session_state.history.append({
                "Gender": gender,
                "Age": age,
                "Height (cm)": height,
                "Weight (kg)": weight,
                "Duration (min)": duration,
                "Heart Rate": heart_rate,
                "Body Temp (°C)": body_temp,
                "Calories Burned": round(prediction, 2)
        })
        else:
            st.error(f"Error from API: {response.text}")
            
        # Show history
    if st.checkbox("📜 Show Prediction History"):
        st.subheader("Prediction History")
        if st.session_state.history:
            history_df = pd.DataFrame(st.session_state.history)
            st.dataframe(history_df)
        else:
            st.info("No history yet. Predict some calories first!")


    if st.checkbox("Show Calories vs Duration Graph"):
        st.subheader("📊 Calories Burned vs Workout Duration")

        # Range of durations to simulate
        durations = list(range(5, 65, 5))  # 5 to 60 minutes, step 5
        predictions = []

        for d in durations:
            temp_data = [{
                "Gender": 1 if gender.lower() == "male" else 0,
                "Age": age,
                "Height": height,
                "Weight": weight,
                "Duration": d,
                "Heart_Rate": heart_rate,
                "Body_Temp": body_temp
            }]
            response = requests.post(api_url, json=temp_data)
            if response.status_code == 200:
                predictions.append(response.json()["Predicted Calories"][0])
            else:
                predictions.append(None)

        # Filter out None values (errors)
        durations = [d for d, p in zip(durations, predictions) if p is not None]
        predictions = [p for p in predictions if p is not None]

        if predictions:
            fig, ax = plt.subplots()
            ax.plot(durations, predictions, marker='o')
            ax.set_xlabel("Duration (minutes)")
            ax.set_ylabel("Calories Burned")
            ax.set_title("Calories Burned vs Workout Duration")
            st.pyplot(fig)
        else:
            st.warning("Could not generate graph due to API errors.")


# Show splash screen only once per session
if "splash_shown" not in st.session_state:
    Show_Splash_Screen()
    st.session_state.splash_shown = True

# Initialize login session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "forgot_password" not in st.session_state:
    st.session_state.forgot_password = False
if

# Main navigation flow
if st.session_state.logged_in:
    Show_Main_Screen()
else:
    if st.session_state.forgot_password:
        Show_Forgot_Password_Screen()  # You'll define this function
    elif st.session_state.show_signup:
        Show_SignUp_Screen(
    else:
        page = st.sidebar.selectbox("Choose a page", ["Login", "Sign Up"])

        if page == "Sign Up":
            Show_Sign_Up_Screen()
        else:
            Show_Login_Screen()
