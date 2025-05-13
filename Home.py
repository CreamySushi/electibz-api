import streamlit as st
from views.login import Show_Login_Screen
from views.signup import Show_Sign_Up_Screen
from views.forgot_password import Show_Forgot_Password_Screen
from views.main_app import Show_Main_Screen
from utils.init import setup_session_state, initialize_database, Show_Splash_Screen
from utils.styles import sidebar_styles, hide_streamlit_style, background_style


st.set_page_config(page_title="Calorie Burn Predictor", page_icon="calories.ico", initial_sidebar_state="collapsed")
setup_session_state()
initialize_database()

if not st.session_state.splash_shown:
    Show_Splash_Screen()
    st.session_state.splash_shown = True
    
    st.markdown(background_style(), unsafe_allow_html=True)
    st.markdown(hide_streamlit_style(), unsafe_allow_html=True)
    st.rerun()

if st.session_state.logged_in:
    with st.sidebar:
        st.markdown(
            f"""
            <div style="font-size: 0.9rem; font-weight: 500; padding: 0.5rem 0; color: white;">
                Welcome, {st.session_state.username}
            </div>
            """, unsafe_allow_html=True
        )

        if st.button("🔄 Refresh"):
            st.rerun()

        st.markdown(sidebar_styles(), unsafe_allow_html=True)

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.admin = False
            st.rerun()

    Show_Main_Screen()
else:
    if st.session_state.forgot_password:
        Show_Forgot_Password_Screen()
    elif st.session_state.show_signup:
        Show_Sign_Up_Screen()
    else:
        Show_Login_Screen()