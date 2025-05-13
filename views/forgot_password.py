import streamlit as st
import bcrypt
import sqlite3
import re

conn = sqlite3.connect('calorie_history.db', check_same_thread=False)
c = conn.cursor()

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