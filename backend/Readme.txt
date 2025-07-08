1. Dataset.csv
   - The main dataset used to train the model.

2. Collected_Data.csv
   - Temporary file that stores newly collected data throughout the week.


4. trainmodel.py
   - Trains the Random Forest model using Dataset.csv.
   - Saves the trained model as `rf_parking_model2.pkl`.

5. rf_parking_model2.pkl
   - Trained Random Forest model.

6. app.py
   - Flask backend API.
   - Accepts a datetime input and returns predicted parking occupancy.

7. test.py
   - Used to test the Flask prediction manually.

8. weekly_update.py
   - Appends collected_data.csv to Dataset.csv weekly.
   - Retrains the model using the updated data.

weekly_update.py and app.py will be run at weeky intervals to retrain.
