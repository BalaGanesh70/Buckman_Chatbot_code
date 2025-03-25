import pandas as pd
import os

def test_pipeline(data_path):
    # Ensure the file is correctly referenced within the 'data' directory
    file_path = os.path.join("data", data_path) if not os.path.isabs(data_path) else data_path

    try:
        df = pd.read_csv(file_path)
        print(f"✅ Data loaded successfully from {file_path}")
        print("📌 Sample Data:")
        print(df.head())
    except Exception as e:
        print(f"❌ Error loading data: {e}")

if __name__ == "__main__":
    test_pipeline("Students_Grading_Dataset.csv")
