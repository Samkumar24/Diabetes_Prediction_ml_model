import streamlit as st
import pickle
import numpy as np
import pandas as pd
import json
import requests


with open(r"C:\\Users\\sam\\Diabietes_best_final_model.pkl", "rb") as f:
    model = pickle.load(f)

url = "http://127.0.0.1:8000/Predict/"

st.title(" Diabetes Risk Prediction For Medical Team 🩺")
st.write("**Family_history_diabaities 0 means patient has no history , 1 mean yes** ")

with open("reference_values.json", "r") as f:
    ref = json.load(f)


int_cols = ref["int_columns"]
float_cols = ref["float_columns"]
#cat_cols = ref["categorical_columns"]

feature_order   = [
    "hba1c",
    "glucose_postprandial",
    "glucose_fasting",
    "diabetes_risk_score",
    "physical_activity_minutes_per_week",
    "family_history_diabetes",
    "age",
    "triglycerides",
    "waist_to_hip_ratio",
    "ldl_hdl_ratio",
    "insulin_level",
]
inputs = {}



cols = st.columns(2)
for i , j in enumerate(int_cols.items()):
    with cols[i% 2]:
        val = st.number_input(label=j[0],
                              max_value=j[1]['max'],
                              min_value=j[1]['min'],step=1)
    
    inputs[j[0]] = val

cols = st.columns(2)
for idx, (col, info) in enumerate(float_cols.items()):
    with cols[idx % 2]:
        val = st.number_input(
            label=col,
            min_value=float(info["min"]),
            max_value=float(info["max"]),
            step=0.1
        )
        inputs[col] = val

# -------- Converting into Dataframe  --------
if st.button("Predict"):
    data_frame = pd.DataFrame(inputs,index=[0])
    data_frame = data_frame[feature_order]

    try:
        records = data_frame.to_dict(orient='records')[0]
        response = requests.post(url,json=records)
        if response.status_code == 200:
            result =  response.json()
            result_response = (result['prediction'])
            if 'has diabetes' in result_response:
                st.error("Patient has diabetes ")
            else:
                st.success("Patient has no  diabetes")
        else:
            st.error(f"Api error {response.status_code}  {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to fast api server ")