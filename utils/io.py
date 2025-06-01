import pandas as pd
import os

def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["tarih"])
    else:
        return pd.DataFrame(columns=["tarih", "plaka", "tur_no", "sira_no", "musteri", "teslim_durumu"])

def save_data(df, path):
    df.to_csv(path, index=False)

def load_arac_listesi(path="data/arac_listesi.csv"):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return pd.DataFrame(columns=["plaka", "aciklama"])

def save_arac_listesi(df, path="data/arac_listesi.csv"):
    df.to_csv(path, index=False)
