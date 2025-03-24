from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
import requests

app = Flask(__name__)

# Load models
soil_model = joblib.load("soil_crop_model.pkl")
soil_label_encoder = joblib.load("label_encoder.pkl")
weather_model = joblib.load("weather_farming_model.pkl")
weather_label_encoder = joblib.load("farming_label_encoder.pkl")

# Landing page
@app.route('/')
def landing_page():
    return render_template("landing_page.html")

# Soil crop prediction
@app.route("/soil_crop")
def soil_crop_home():
    return render_template("index1.html")

@app.route("/predict_crop", methods=["POST"])
def predict_crop():
    try:
        nitrogen = float(request.form["nitrogen"])
        phosphorus = float(request.form["phosphorus"])
        potassium = float(request.form["potassium"])
        ph = float(request.form["ph"])
        soil_type = int(request.form["soil_type"])
        input_data = [[soil_type, ph, nitrogen, phosphorus, potassium]]
        prediction = soil_model.predict(input_data)
        predicted_crop = soil_label_encoder.inverse_transform(prediction)[0]
        return render_template("index1.html", prediction_text=f"Best Crop: {predicted_crop}")
    except Exception as e:
        return render_template("index1.html", prediction_text=f"Error: {e}")

# Weather farming prediction
def fetch_weather_data(city):
    api_key = '3c7ff6ada1446ae4068848b328a5f28a'  # Replace with a valid API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url).json()
    print("Weather API Response:", response)  # Debugging
    if response.get("main"):
        temperature = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        rainfall = response.get("rain", {}).get("1h", 0)  # Default to 0 if no rainfall data
        return temperature, humidity, rainfall
    return None, None, None

@app.route('/weather_predict')
def weather_predict_home():
    return render_template('index2.html')

@app.route('/predict', methods=['POST'])
def predict_weather():
    city = request.form['city'].strip()
    temperature, humidity, rainfall = fetch_weather_data(city)

    if temperature is None:
        return render_template('error.html', message=f"Could not fetch weather data for the city '{city}'. Please try again.")

    input_data = [[temperature, humidity, rainfall]]
    print("Input Data for Prediction:", input_data)

    try:
        prediction = weather_model.predict(input_data)
        farming_practice = weather_label_encoder.inverse_transform(prediction)[0]
        print("Prediction:", farming_practice)  # Debugging
        return render_template('result.html', city=city, practice=farming_practice)
    except Exception as e:
        print("Error during prediction:", e)
        return render_template('error.html', message="An error occurred during prediction. Please try again.")

  

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Farmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(100), nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.id'), nullable=False)

@app.route('/resource_pooling')
def resource_pooling_home():
    return render_template('home.html')

@app.route('/add_farmer', methods=['GET', 'POST'])
def add_farmer():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        contact = request.form['contact']
        resources = request.form['resources'].split(',')
        farmer = Farmer(name=name, location=location, contact=contact)
        db.session.add(farmer)
        db.session.commit()
        for resource_name in resources:
            resource = Resource(resource_name=resource_name.strip(), farmer_id=farmer.id)
            db.session.add(resource)
        db.session.commit()
        return redirect('/')
    return render_template('add_farmer.html')

@app.route('/find_resources', methods=['GET', 'POST'])
def find_resources():
    farmers = []
    if request.method == 'POST':
        resource_query = request.form['resource_query']
        farmers = Farmer.query.join(Resource).filter(Resource.resource_name.like(f"%{resource_query}%")).all()
    return render_template('find_resources.html', farmers=farmers)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if "hello" in user_message.lower():
        reply = "Hi there! How can I help you today?"
    elif "weather" in user_message.lower():
        reply = "The weather is sunny with a chance of coding!"
    else:
        reply = "I'm not sure how to respond to that, but I'm here to help!"
    return jsonify({"reply": reply})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)
