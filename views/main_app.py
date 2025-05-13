import streamlit as st
import requests
import altair as alt
import pandas as pd
import sqlite3

conn = sqlite3.connect('calorie_history.db', check_same_thread=False)
c = conn.cursor()



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
            st.data_editor(df, use_container_width=True, disabled=True)
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
                response = requests.post(api_url, json=data, timeout=20)
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
            chart_data = pd.DataFrame({
                "Duration (min)": durations,
                "Calories Burned": predictions
            })

            chart = alt.Chart(chart_data).mark_line(point=True).encode(
                x=alt.X("Duration (min)", title="Workout Duration (minutes)"),
                y=alt.Y("Calories Burned", title="Calories Burned"),
                tooltip=["Duration (min)", "Calories Burned"]
            ).properties(
                title="Calories Burned vs Workout Duration",
                width=600,
                height=400
            )

            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Could not generate graph due to API errors.")