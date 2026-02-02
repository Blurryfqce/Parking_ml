import pandas as pd
import os
from trainmodel import train_model
from fetch_firebase_data import fetch_and_store_firebase_data

# File paths
original_file = 'data/Dataset.csv'
collected_file = 'data/Collected_Data.csv'

try:
    fetch_and_store_firebase_data()

    if os.path.exists(collected_file) and os.path.getsize(collected_file) > 0:
        original_df = pd.read_csv(original_file)
        collected_df = pd.read_csv(collected_file)

        updated_df = pd.concat([original_df, collected_df], ignore_index=True)
        updated_df.drop_duplicates(inplace=True)  #avoid re-appending same rows

        updated_df.to_csv(original_file, index=False)
        print("Dataset updated successfully!")

        pd.DataFrame(columns=collected_df.columns).to_csv(collected_file, index=False)
        print("Collected data cleared!")

        train_model()
        print("Model retrained!")

    else:
        print("No new data to append.")

except Exception as e:
    print(f"Error during weekly update: {e}")
