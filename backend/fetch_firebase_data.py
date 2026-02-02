import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from datetime import datetime, timedelta

# Initialize Firebase only once
firebase_initialized = False

def fetch_and_store_firebase_data():
    global firebase_initialized
    if not firebase_initialized:
        cred = credentials.Certificate("config/firebase_key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://test-parking-database-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        firebase_initialized = True

    
    ref = db.reference("hourly_occupancy")  
    logs = ref.get()

    if not logs:
        print("No new data found ")
        return

    print(f"Pulled {len(logs)} entries from Firebase")

    # Only use logs from the last 7 days
    cutoff = datetime.now() - timedelta(days=7)
    data = []
    for timestamp_key, entry in logs.items():
        try:
            ts = datetime.strptime(timestamp_key, "%Y-%m-%d_%H:%M") 
            if ts >= cutoff:
                occupancy = entry.get("occupied")
                if occupancy is not None:
                    data.append({
                        "Datetime": ts.strftime("%Y-%m-%d %H:%M:%S"),
                        "Occupancy": occupancy
                    })
        except Exception as e:
            print(f"Skipping invalid entry {timestamp_key}: {e}")

    df = pd.DataFrame(data)
    collected_path = "data/Collected_Data.csv"

    if df.empty:
        print("No new data found in the last 7 days.")
    else:
        try:
            existing_df = pd.read_csv(collected_path)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.drop_duplicates(inplace=True)
            updated_df.to_csv(collected_path, index=False)
            print("Firebase data appended to Collected_Data.csv!")
        except FileNotFoundError:
            df.to_csv(collected_path, index=False)
            print("Collected_Data.csv updated!")


fetch_and_store_firebase_data()
