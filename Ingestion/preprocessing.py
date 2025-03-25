import pandas as pd

def preprocess_data(data):
    data.dropna(inplace=True)
    return data

if __name__ == "__main__":
    df = pd.read_csv("../data/sample_data.csv")
    cleaned_df = preprocess_data(df)
    print(cleaned_df.head())
