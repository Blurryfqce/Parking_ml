Parking Lot Occupancy Prediction System

Overview
   This project is a machine learning–based system for predicting parking lot occupancy using synthetic and real-time data. It integrates data collection and model training to provide occupancy forecasts based on date and time.

   The system was originally developed as an IoT-based intelligent parking management solution and later extended with predictive analytics.

   Multiple models were evaluated and to select the best performing model for this project (performance.ipynb)

Features
   - Machine Learning model (Random Forest)
   - Automatic weekly data updates from Firebase
   - Flask web application for predictions
   - Deployable on Render / cloud platforms


Project Structure
   - backend/        # Training, API, automation
   - data/           # Datasets
   - config/         # Firebase config 
   - requirements.txt
   - README.md

How To Run Locally
1. Install Dependencies
pip install -r requirements.txt

2. Train Model
   backend
   -trainmodel.py

3. Run Web App
   -app.py

4. Then open in browser:
   http://127.0.0.1:5000

5. To Retrain
   weekly_update.py


About Model
   - Algorithm: Random Forest Regressor
   - Synthetic data and real-time data
   - Input: Date, time, historical occupancy
   - Output: Predicted parking occupancy



Firebase credentials are excluded from this repository using .gitignore.


Awwal Ajao

This project is for educational and portfolio purposes.