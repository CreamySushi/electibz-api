import streamlit as st
import requests
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Calorie Burn Predictor",page_icon="calories.ico")

def Show_Splash_Screen():
    splash = st.empty()  
    splash.markdown("""
        <div style='text-align: center; margin-top: 200px;'>
            <h1>dawdawfawfaw</h1>
            <p>Loading, please wait...</p>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    splash.empty()

def Show_Main_Screen():
    
    st.title("🔥 Calorie Burn Predictor")
    api_url = "https://electibz-api.onrender.com/predict/"

    defaults = {
        "gender": "Male",
        "age": 25,
        "height": 170,
        "weight": 70,
        "duration": 30,
        "heart_rate": 100,
        "body_temp": 37.0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
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
        else:
            st.error(f"Error from API: {response.text}")


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

Show_Main_Screen()
