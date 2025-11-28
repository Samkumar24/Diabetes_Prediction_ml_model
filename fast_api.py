from fastapi import   FastAPI 
from pydantic import Field , create_model
import json
import uvicorn
import pickle
import pandas as pd

with open(r"C:\\Users\\sam\\Diabietes_best_final_model.pkl", "rb") as f:
    model = pickle.load(f)


app = FastAPI()

with open("reference_values.json",'r') as f:
    reference_df = json.load(f)


@app.get("/message/")
def meassage():
    return {"message":"Welcome"}

ref = {}


for col, values in reference_df['int_columns'].items():
    ref[col] = (int, Field(
        ...,
        ge=values['min'],
        le=values['max'],
        description=f"value should be between {values['min']} and {values['max']}"
    ))



for col , values in reference_df['float_columns'].items():
    ref[col] = (float ,Field(...,ge=values['min'],le=values['max']))


PatientModel = create_model("PatientModel", **ref)

@app.post('/Predict/')
def predict(data: PatientModel):
    

    data_df = data.model_dump()

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
    data_df = pd.DataFrame([data_df])
    data_df = data_df[feature_order]
    
    pred = int(model.predict(data_df)[0])

    result = "Patient has diabetes" if pred == 1 else "Patient has no diabetes"

    return {
        "input_data": data_df.to_dict(orient='records')[0],
        "prediction": result,
        "message": "Model predicition done"
    }





