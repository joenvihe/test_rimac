import streamlit as st
import requests 

url_api = 'https://api-heart-disease-xbdu5qelna-uc.a.run.app/predict'

st.title("Heart Disease Prediction")
st.markdown(
    """
    <style>
    .title {
        color: #800000;
        text-align: center;
    }
    .btn {
        background-color: #800000;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("heart-image.png", use_column_width=True)  

age = st.slider("Age", min_value=0, max_value=150, step=1)
sex = st.radio("Sex", options=["M", "F"])
chest_pain_type = st.selectbox("Chest Pain Type", options=["TA: Typical Angina", "ATA: Atypical Angina", "NAP: Non-Anginal Pain", "ASY: Asymptomatic"])
resting_bp = st.slider("Resting BP (mm Hg)", min_value=0, max_value=300, step=1)
cholesterol = st.slider("Cholesterol (mm/dl)", min_value=0, max_value=600, step=1)
fasting_bs = st.radio("Fasting BS", options=["0", "1"])
resting_ecg = st.selectbox("Resting ECG", options=["Normal", "ST", "LVH"])
max_hr = st.slider("Max HR", min_value=60, max_value=202, step=1)
exercise_angina = st.radio("Exercise Angina", options=["N", "Y"])
oldpeak = st.slider("Oldpeak", min_value=0.0, max_value=10.0, step=0.1)
st_slope = st.selectbox("ST Slope", options=["Up", "Flat", "Down"])

if st.button("Predict Heart Disease", key="predict_btn"):
    # Here you can add code to predict heart disease based on the input fields
    # For now, let's just display the input values
    st.markdown("---")
    st.write("## Input Values:")
    st.write(f"**Age:** {age} years")
    st.write(f"**Sex:** {sex}")
    st.write(f"**Chest Pain Type:** {chest_pain_type}")
    st.write(f"**Resting BP:** {resting_bp} mm Hg")
    st.write(f"**Cholesterol:** {cholesterol} mm/dl")
    st.write(f"**Fasting BS:** {fasting_bs}")
    st.write(f"**Resting ECG:** {resting_ecg}")
    st.write(f"**Max HR:** {max_hr}")
    st.write(f"**Exercise Angina:** {exercise_angina}")
    st.write(f"**Oldpeak:** {oldpeak}")
    st.write(f"**ST Slope:** {st_slope}")

    params = {
        'age':age,
        'sex': sex,
        'chest_pain':chest_pain_type.split(':')[0].strip(),
        'resting_bp':resting_bp,
        'cholesterol': cholesterol,
        'fasting_bs':fasting_bs,
        'resting_ecg': resting_ecg,
        'max_hr': max_hr,
        'exercise_angina': exercise_angina,
        'oldpeak': oldpeak,
        'st_slope':st_slope
    }
    response = requests.get(url_api, params=params)

    if response.status_code == 200:
        class_prediction = response.json()['prediction']
        st.markdown(f'The prediction is **{class_prediction}**.')
    else:
        st.markdown(f'There was an error.')



