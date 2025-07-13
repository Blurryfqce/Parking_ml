import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
from datetime import datetime, timedelta

# Initialize Firebase only once
firebase_initialized = False

def fetch_and_store_firebase_data():
    global firebase_initialized
    if not firebase_initialized:
        cred = credentials.Certificate("backend/firebase_key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://test-parking-database-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        firebase_initialized = True

    # Reference to hourly_occupancy
    ref = db.reference("hourly_occupancy")
    logs = ref.get()

    # Only use entries from the last 7 days
    cutoff = datetime.now() - timedelta(days=7)
    data = []

    for timestamp_key, value in logs.items():
        try:
            # Convert key like "2025-07-12_15:00" to datetime
            dt = datetime.strptime(timestamp_key, "%Y-%m-%d_%H:%M")
            if dt >= cutoff:
                occupancy = value.get("occupied")
                if occupancy is not None:
                    data.append({
                        "Datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                        "Occupancy": occupancy
                    })
        except Exception as e:
            print(f"⚠️ Error parsing entry {timestamp_key}: {e}")

    df = pd.DataFrame(data)
    collected_path = "backend/Collected_Data.csv"

    if df.empty:
        print("⚠️ No new data found in Firebase.")
    else:
        try:
            existing_df = pd.read_csv(collected_path)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.drop_duplicates(inplace=True)
            updated_df.to_csv(collected_path, index=False)
            print("✅ Firebase data appended to Collected_Data.csv!")
        except FileNotFoundError:
            df.to_csv(collected_path, index=False)
            print("✅ Created Collected_Data.csv with Firebase data!")
