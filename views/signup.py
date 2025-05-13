import streamlit as st
import bcrypt
import sqlite3
import re

conn = sqlite3.connect('calorie_history.db', check_same_thread=False)
c = conn.cursor()

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