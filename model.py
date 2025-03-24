import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib


data = pd.read_csv('weather_farming_practice.csv')


label_encoder = LabelEncoder()
data['Farming_Practice'] = label_encoder.fit_transform(data['Farming_Practice'])


X = data[['Temperature', 'Humidity', 'Rainfall']]
y = data['Farming_Practice']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)


joblib.dump(model, 'weather_farming_model.pkl')
joblib.dump(label_encoder, 'farming_label_encoder.pkl')

print("Model and label encoder saved!")
