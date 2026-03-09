from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and encoders
model = joblib.load("fertilizer_rf_model.pkl")
le_dict = joblib.load("fertilizer_label_encoders.pkl")


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Send dropdown options
@app.route("/get_options")
def get_options():

    options = {}

    for key in ["Soil_Type","Crop_Type","Crop_Growth_Stage","Season",
                "Irrigation_Type","Previous_Crop","Region"]:
        options[key] = list(le_dict[key].classes_)

    return jsonify(options)


# Prediction API
@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        manual_input = {
            "Soil_Type": data["Soil_Type"],
            "Soil_pH": float(data["Soil_pH"]),
            "Soil_Moisture": float(data["Soil_Moisture"]),
            "Organic_Carbon": float(data["Organic_Carbon"]),
            "Electrical_Conductivity": float(data["Electrical_Conductivity"]),
            "Nitrogen_Level": float(data["Nitrogen_Level"]),
            "Phosphorus_Level": float(data["Phosphorus_Level"]),
            "Potassium_Level": float(data["Potassium_Level"]),
            "Temperature": float(data["Temperature"]),
            "Humidity": float(data["Humidity"]),
            "Rainfall": float(data["Rainfall"]),
            "Crop_Type": data["Crop_Type"],
            "Crop_Growth_Stage": data["Crop_Growth_Stage"],
            "Season": data["Season"],
            "Irrigation_Type": data["Irrigation_Type"],
            "Previous_Crop": data["Previous_Crop"],
            "Region": data["Region"],
            "Fertilizer_Used_Last_Season": float(data["Fertilizer_Used_Last_Season"]),
            "Yield_Last_Season": float(data["Yield_Last_Season"])
        }

        # Encode categorical values
        for col in ["Soil_Type","Crop_Type","Crop_Growth_Stage","Season",
                    "Irrigation_Type","Previous_Crop","Region"]:
            manual_input[col] = le_dict[col].transform([manual_input[col]])[0]

        X = pd.DataFrame([manual_input])

        pred = model.predict(X)[0]

        fertilizer = le_dict["Recommended_Fertilizer"].inverse_transform([pred])[0]

        return jsonify({
            "success": True,
            "prediction": fertilizer
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)