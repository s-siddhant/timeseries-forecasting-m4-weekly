import numpy as np
import pandas as pd

def preprocess_data(df):
    # Temporal Features
    df["week_of_year"] = df["timestamp"].dt.isocalendar().week
    df["month"] = df["timestamp"].dt.month

    # Cyclic Features
    df["week_of_year_sin"] = np.sin(2 * np.pi * df["week_of_year"] / 52)
    df["week_of_year_cos"] = np.cos(2 * np.pi * df["week_of_year"] / 52)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    # Lagged Features
    for lag in [1, 2, 4, 8, 12, 26, 52]:
        df[f"lag_{lag}"] = df["target"].shift(lag)

    # Rolling Features
    df["rolling_mean_4"] = df["target"].rolling(window=4).mean()
    df["rolling_std_4"] = df["target"].rolling(window=4).std()
    df["rolling_mean_12"] = df["target"].rolling(window=12).mean()
    df["rolling_std_12"] = df["target"].rolling(window=12).std()
    df["rolling_mean_52"] = df["target"].rolling(window=52).mean()
    df["rolling_std_52"] = df["target"].rolling(window=52).std()

    # Drop unnecessary columns
    return df.drop(columns=["timestamp", "target"])
