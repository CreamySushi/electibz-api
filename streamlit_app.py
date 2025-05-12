import streamlit as st
import requests
import matplotlib.pyplot as plt
import time
import pandas as pd
import sqlite3
import bcrypt
import re

st.set_page_config(page_title="Calorie Burn Predictor",page_icon="calories.ico",initial_sidebar_state="collapsed")


# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "forgot_password" not in st.session_state:
    st.session_state.forgot_password = False
if "splash_shown" not in st.session_state:
    st.session_state.splash_shown = False
if "email" not in st.session_state:
    st.session_state.email = None
if "admin" not in st.session_state:
    st.session_state.admin = False

background_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://t3.ftcdn.net/jpg/04/29/35/62/360_F_429356296_CVQ5LkC6Pl55kUNLqLisVKgTw9vjyif1.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
}

/* Make main container background transparent */
[data-testid="stAppViewContainer"] > .main {
    background-color: rgba(0,0,0,0);
}

/*Make sidebar transparent */
[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.6);
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

hide_streamlit_style = """
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

conn = sqlite3.connect('calorie_history.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

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

#Styling Sidebar buttons
st.markdown("""
    <style>
        section[data-testid="stSidebar"] div.stButton > button {
            background: none !important;
            border: none !important;
            padding: 0.25rem 0 !important;
            font-size: inherit !important;
            color: #FFFFFF !important;
            text-align: left !important;
            font-weight: Bold !important;
            cursor: pointer;
        }

        section[data-testid="stSidebar"] div.stButton > button > div {
            font-size: 2rem !important;
            font-weight: Bold !important
        }

        section[data-testid="stSidebar"] div.stButton {
            margin-bottom: 0.25rem;
        }

        section[data-testid="stSidebar"] {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        section[data-testid="stSidebar"] > div.stButton:last-child {
            margin-top: auto;
        }
    </style>
""", unsafe_allow_html=True)
                

def initialize_database():
    conn = sqlite3.connect('calorie_history.db')
    c = conn.cursor()

   
    admin_email = "Admin123@administrator.com" 
    admin_password = "group3admin"
    

    c.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')

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

    
    admin = "Admin"
    c.execute("SELECT * FROM users WHERE email = ?", (admin_email,))
    if not c.fetchone():
        hashed_admin_pw = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (admin, admin_email, hashed_admin_pw))
        print("Admin account created.")

    conn.commit()
    conn.close()

def Show_Splash_Screen():
    splash = st.empty()  
    splash.markdown("""
        <div style='text-align: center; margin-top: 250px;font-family: 'Arial', sans-serif;'>
            <h1>Welcome to Calories Burn Predictor</h1>
            <p>Loading, please wait...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    splash.empty()

def Show_Sign_Up_Screen():
    st.title("Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email", placeholder="username@gmail.com")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm password", type="password")

    # Check for email format like @something.com
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if st.button("Register"):
        if not email or not password or not password_confirm or not username:
            st.warning("Please fill in all fields.")
        elif len(email) < 6:
            st.error("Email must be at least 6 characters long.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long.")
        elif password != password_confirm:
            st.error("Passwords do not match.")
        elif email == username:
            st.error("Email and Username must be different.")
        elif not re.match(email_regex, email):
            st.error("Email must be in the format 'username@something.com'.")
        else:
            # Check if username already exists
            c.execute("SELECT * FROM users WHERE username = ?", (username,))
            if c.fetchone():
                st.error("Username already exists.")
            else:
                # Check if email is already used
                c.execute("SELECT * FROM users WHERE email = ?", (email,))
                if c.fetchone():
                    st.error("Email is already registered.")
                else:
                    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
                    conn.commit()
                    st.success("Account created! Please log in.")
                    st.session_state.show_signup = False
                    st.session_state.username = None
                    st.session_state.email = None
                    st.rerun()

    if st.button("Back to Login"):
        st.session_state.show_signup = False
        st.rerun()
                
def Show_Login_Screen():
    st.title("Login")
    
    with st.form(clear_on_submit=False, key="login-form"):
        email = st.text_input("Email", placeholder="username@gmail.com")
        password = st.text_input("Password", type="password", placeholder="Password must be at least 6 characters long")
        submitted = st.form_submit_button("Login")

        if submitted:
            if email and password:
                c.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = c.fetchone()

                if user and bcrypt.checkpw(password.encode(), user[3].encode()):
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.session_state.email = user[2]
                    if user[2] == "Admin123@administrator.com":
                        st.session_state.admin = True
                    else:
                        st.session_state.admin = False 
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            else:
                st.warning("Please fill in both fields.")

    st.markdown("""
        <style>

            div[data-testid="stForm"] {
                background-color: transparent;
                border: none;
                box-shadow: none;
                padding: 0;
            }

            .stButton[id="forgot-password-button"] > button {
                width: auto;
                text-align: left;
                padding-left: 0;
                font-weight: normal;
                margin-top: 10px;
            }

            .stform[id="login-form"], .stButton[id="forgot-password-button"] {
                width: auto;
                display: inline-block;
            }

            .stButton[id="signup-button"] {
                margin-top: 20px !important;
            }

            .stText {
                font-size: 14px;
                margin-top: 0.25rem;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)


    if st.button("Forgot Password?"):
        st.session_state.forgot_password = True
        st.rerun()

    st.markdown("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.show_signup = True
        st.session_state.logged_in = False
        st.rerun()

def Show_Forgot_Password_Screen():
    st.title("Forgot Password")

    email = st.text_input("Enter your email", placeholder="username@gmail.com")
    password = st.text_input("Enter new password", type="password")
    password_confirm = st.text_input("Confirm new password", type="password")

    # Check for email format like @something.com
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if st.button("Reset Password"):
        if not email or not password or not password_confirm:
            st.error("Please fill in all fields.")
        elif password != password_confirm:
            st.error("Passwords do not match.")
        elif not re.match(email_regex, email):
            st.error("Email must be in the format 'username@gmail.com'.")
        else:
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            if c.fetchone():
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_pw, email))
                conn.commit()
                st.success("Password reset successfully. Please login.")
                st.session_state.forgot_password = False
                st.rerun()
            else:
                st.error("Email not found.")

    if st.button("Back to Login"):
        st.session_state.forgot_password = False
        st.rerun()

def Show_Main_Screen():
    
    st.title("🔥 Calorie Burn Predictor")
    api_url = "https://electibz-api.onrender.com/predict/"
    if "history" not in st.session_state:
        st.session_state.history = []
        
    if "username" not in st.session_state:
        st.error("No user session found. Please log in again.")
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.admin:
        st.subheader("📜 All Users' Prediction History ")

        c.execute('''
            SELECT username, gender, age, height, weight, duration, heart_rate, body_temp, calories_burned
            FROM history
        ''')
        data = c.fetchall()

        if data:
            df = pd.DataFrame(data, columns=[
                "Username", "Gender", "Age", "Height (cm)", "Weight (kg)",
                "Duration (min)", "Heart Rate", "Body Temp (°C)", "Calories Burned"
            ])
            st.dataframe(df)
        else:
            st.info("No prediction history available.")
        return
    
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
            try:
                response = requests.post(api_url, json=data, timeout=10)
                response.raise_for_status()  
                prediction = response.json()["Predicted Calories"][0]
                st.success(f"🔥 Estimated Calories Burned: {prediction:.2f}")
 
                if prediction < 50:
                    st.info("Your workout was light. Try to add a few more minutes next time to achieve more calorie burn.")
                elif 50 <= prediction <= 150:
                   st.success("Good effort! You had a steady workout. Aim for a slightly higher intensity next time.")
                elif 151 < prediction <= 250:
                    st.success("Well done! That's a solid calorie burn. Stay consistent!")
                else:
                    st.success("Amazing! That was a long session, you're definitely making progress. Keep up the momentum!")

                # Save to database
                c.execute('''
                    INSERT INTO history (username, gender, age, height, weight, duration, heart_rate, body_temp, calories_burned)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (st.session_state.username, gender, age, height, weight, duration, heart_rate, body_temp, round(prediction, 2)))
                conn.commit()

            except requests.exceptions.RequestException as e:
                st.error(f"API Error: {e}")

            
        # Show history
    if st.checkbox("📜 Show Prediction History"):
        st.subheader("Prediction History")

        c.execute('''
            SELECT gender, age, height, weight, duration, heart_rate, body_temp, calories_burned
            FROM history WHERE username = ?
        ''', (st.session_state.username,))
        data = c.fetchall()

        if data:
            df = pd.DataFrame(data, columns=["Gender", "Age", "Height (cm)", "Weight (kg)","Duration (min)", "Heart Rate", "Body Temp (°C)", "Calories Burned"])
            st.dataframe(df)
        else:
            st.info("No history found yet.")


    if st.checkbox("Show Calories vs Duration Graph"):
        st.subheader("Calories Burned vs Workout Duration")

        # Range of durations to simulate
        durations = list(range(5, 65, 5))  
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

       
        durations = [d for d, p in zip(durations, predictions) if p is not None]
        predictions = [p for p in predictions if p is not None]

        if predictions:
            fig, ax = plt.subplots(facecolor="#1e1e1e")
            ax.plot(durations, predictions, marker='o', color="#00ff99")
            ax.set_facecolor("#2b2b2b")  
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')      
            ax.grid(True, linestyle='--', alpha=0.3)
            st.pyplot(fig)
        else:
            st.warning("Could not generate graph due to API errors.")

# Main navigation flow
if not st.session_state.splash_shown:
    Show_Splash_Screen()
    st.session_state.splash_shown = True
    st.rerun()
else:
    with st.sidebar:
        if st.session_state.logged_in:
            st.button(f"Welcome, {st.session_state.username}")
            st.markdown("---")
            st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
            if st.button(" Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.admin = False
                conn.commit()
                st.rerun()
            
            st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
            if st.button("About Us"):
                st.write("This is a project made by college students of University of Perpetual Help System [Laguna] as an output application to track the calorie burn of the user by input some necessary details to calculate the calories. This application uses a machine learning algorithm to calculate calories individually using xgb algorithm.")
            
            if st.button("Contact Us"):
                st.markdown("""
                    <a href="https://www.facebook.com/profile.php?id=61576137483701" target="_blank">
                        <button style='font-size:20px;padding:10px 20px;border-radius:10px;background-color:#4CAF50;color:white;border:none;cursor:pointer; font-family: 'Arial', sans-serif;'>
                            Visit Facebook Page
                        </button>
                    </a>
                """, unsafe_allow_html=True)
                

        else:
            if st.button("About Us"):
                st.write("This is a project made by college students of University of Perpetual Help System [Laguna] as an output application to track the calorie burn of the user by input some necessary details to calculate the calories. This application uses a machine learning algorithm to calculate calories individually using xgb algorithm.")
            if st.button("Contact Us"):
                st.markdown("""
                    <a href="https://www.facebook.com/profile.php?id=61576137483701" target="_blank">
                        <button style='font-size:20px;padding:10px 20px;border-radius:10px;background-color:#4CAF50;color:white;border:none;cursor:pointer;font-family: 'Arial', sans-serif;'>
                            Visit Facebook Page
                        </button>
                    </a>
                """, unsafe_allow_html=True)
initialize_database()

if st.session_state.logged_in:
    Show_Main_Screen()
else:
    if st.session_state.forgot_password:
        Show_Forgot_Password_Screen()
    elif st.session_state.show_signup:
        Show_Sign_Up_Screen()
    else:
        Show_Login_Screen()

