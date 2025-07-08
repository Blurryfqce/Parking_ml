import pandas as pd
import os
import subprocess
from trainmodel import train_model  # assuming this is a function in trainmodel.py

# File paths
original_file = 'backend/Dataset.csv'
collected_file = 'backend/Collected_Data.csv'

# Step 1: Check if Collected_Data.csv exists and is not empty
if os.path.exists(collected_file) and os.path.getsize(collected_file) > 0:
    # Step 2: Load both datasets
    original_df = pd.read_csv(original_file)
    collected_df = pd.read_csv(collected_file)

    # Step 3: Append new data to main dataset
    updated_df = pd.concat([original_df, collected_df], ignore_index=True)
    updated_df.drop_duplicates(inplace=True)  # Optional: avoid re-appending same rows

    # Step 4: Save back to Dataset.csv
    updated_df.to_csv(original_file, index=False)
    print("✅ Dataset updated successfully!")

    # Step 5: Clear Collected_Data.csv
    pd.DataFrame(columns=collected_df.columns).to_csv(collected_file, index=False)
    print("🧹 Collected data cleared!")

    # Step 6: Retrain the model
    train_model()  # make sure train_model.py has a callable function
    print("📈 Model retrained!")

else:
    print("⚠️ No new data to append.")

# #Make app.py re run using new model
# print("Reloading Flask app")
# subprocess.Popen(["python", "backend/app.py"])