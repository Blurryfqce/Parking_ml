from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

# Total parking slots in system
TOTAL_SPOTS = 4

@app.route("/predict", methods=["POST"])
def predict():
    try:
        #Load model every time to ensure latest one is used
        model = joblib.load("backend/rf_parking_model2.pkl")

        content = request.json
        datetime_str = content["datetime"]
        dt = pd.to_datetime(datetime_str)

        features = {
            'hour': [dt.hour],
            'day': [dt.day],
            'dayofweek': [dt.dayofweek],
            'month': [dt.month]
        }

        input_df = pd.DataFrame(features)
        prediction = model.predict(input_df)[0]

        # Clamp prediction between 0 and total spots
        prediction = max(0, min(prediction, TOTAL_SPOTS))

        print("Prediction made:", prediction)

        # Convert to percentage
        percentage = round((prediction / TOTAL_SPOTS) * 100, 2)

        return jsonify({
            "predicted_occupancy": round(prediction, 2),
            "occupancy_percentage": percentage
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
