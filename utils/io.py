import pandas as pd
import os

def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["tarih"])
    else:
        return pd.DataFrame(columns=["tarih", "plaka", "tur_no", "sira_no", "musteri", "teslim_durumu"])

def save_data(df, path):
    df.to_csv(path, index=False)
