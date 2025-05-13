import streamlit as st
import bcrypt
import sqlite3

conn = sqlite3.connect('calorie_history.db', check_same_thread=False)
c = conn.cursor()

def Show_Login_Screen():
    st.title("Login")

    with st.form("login-form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if email and password:
                c.execute("SELECT * FROM users WHERE email = ?", (email,))
                user = c.fetchone()
                if user and bcrypt.checkpw(password.encode(), user[3].encode()):
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.session_state.email = user[2]
                    st.session_state.admin = (user[2] == "Admin123@administrator.com")
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
            else:
                st.warning("Please fill in all fields.")

    if st.button("Forgot Password?"):
        st.session_state.forgot_password = True
        st.rerun()

    st.markdown("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.show_signup = True
        st.rerun()
