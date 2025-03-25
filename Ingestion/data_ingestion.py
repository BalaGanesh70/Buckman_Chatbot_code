import pandas as pd
import os

class DataIngestion:
    def __init__(self, file_path):
        """
        Ensure the file path is correctly set within the 'data' directory.
        Prevents duplicate 'data/data/' issues.
        """
        self.file_path = os.path.join("data", file_path)

    def load_data(self):
        """
        Load data from the given CSV file.
        """
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            print(f"✅ Data loaded successfully from {self.file_path}")
            return df
        else:
            print(f"❌ File not found at {self.file_path}. Please check the path.")
            return None

if __name__ == "__main__":
    # ✅ Ensure correct path reference within 'data' directory
    data_ingestion = DataIngestion(file_path="Students_Grading_Dataset.csv")
    df = data_ingestion.load_data()
