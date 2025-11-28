import pandas as pd
import json
import os


# Load full dataset once (offline)
data = pd.read_csv('C:\\Users\\sam\\Dib_columns.csv')
data.drop(columns='diagnosed_diabetes',inplace=True)
print(data.columns)
# Prepare numerical info

int_col = (data.select_dtypes(include='int'))
float_cols = (data.select_dtypes(include='float'))
#cat_cols = (data[cols].select_dtypes(include='object'))

print(int_col)
print(float_cols)

int_dict = {
    col: {"min": int(data[col].min()), "max": int(data[col].max())}
    for col in int_col
}

float_dict = {
    col : {"min":float(data[col].min()),"max":float(data[col].max())}
    for col in float_cols
}

print(int_dict)

reference_values = {
    "int_columns": int_dict,
    "float_columns": float_dict,
    #"categorical_columns": category_dict
}

if os.path.exists("reference_values.json"):
    print("path exist ")
    print("overwriting safely")

else:
    print("File does NOT exist.")

    with open("reference_values.json", "w") as f:
        json.dump(reference_values, f, indent=4)
