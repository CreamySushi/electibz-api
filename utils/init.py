import streamlit as st
import sqlite3
import bcrypt
import time

def setup_session_state():
    defaults = {
        "logged_in": False, "username": None, "show_signup": False,
        "forgot_password": False, "splash_shown": False,
        "email": None, "admin": False
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def initialize_database():
    conn = sqlite3.connect('calorie_history.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, email TEXT UNIQUE, password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, gender TEXT, age INTEGER, height REAL,
        weight REAL, duration INTEGER, heart_rate INTEGER, 
        body_temp REAL, calories_burned REAL)''')

    admin_email = "Admin123@administrator.com"
    admin_password = "group3admin"
    c.execute("SELECT * FROM users WHERE email = ?", (admin_email,))
    if not c.fetchone():
        hashed = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", ("Admin", admin_email, hashed))

    conn.commit()
    conn.close()

def Show_Splash_Screen():
    splash = st.empty()
    splash.markdown("""
        <div style='text-align: center; margin-top: 250px;font-family: "Arial", sans-serif;'>
            <h1>Welcome to Calories Burn Predictor</h1>
            <p>Loading, please wait...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    splash.empty()
