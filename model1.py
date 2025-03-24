import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib


df = pd.read_csv("soil_crop_dataset.csv")  


label_encoder = LabelEncoder()
df["Soil_Type"] = label_encoder.fit_transform(df["Soil_Type"])
df["Suitable_Crop"] = label_encoder.fit_transform(df["Suitable_Crop"])

X = df.drop("Suitable_Crop", axis=1)
y = df["Suitable_Crop"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


joblib.dump(model, "soil_crop_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("Model and label encoder saved!")
