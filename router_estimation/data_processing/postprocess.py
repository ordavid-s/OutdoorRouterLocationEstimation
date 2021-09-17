import pandas as pd
import numpy as np
import json
from data_processing.calculations import get_dist


def merge_data(gps_data: pd.DataFrame, net_data: pd.DataFrame):
    complete_data = []
    for _, row_net in net_data.iterrows():
        pos = gps_data["timestamp"].sub(row_net["timestamp"]).abs().values.argmin()
        closest_match = gps_data.loc[[pos]]
        data = {"addr": row_net["addr"],
                "rssi": (row_net["signal"]),
                "ssid": row_net["ssid"],
                "freq": row_net["frequency"],
                "lat": float(closest_match["latitude"]),
                "long": float(closest_match["longitude"]),
                "dist": get_dist(row_net["frequency"], row_net["signal"]),
                "timestamp": int(closest_match["timestamp"])}
        complete_data.append(data)

    df = pd.DataFrame(complete_data)
    return df


def preprocess_data(df, step_size=80):
    mean_data = []
    for i in range(0,len(df), step_size):
        average_rssi = np.mean(df[i:i + step_size]["rssi"])
        lat = np.mean(df[i:i + step_size]["lat"])
        long = np.mean(df[i:i + step_size]["long"])
        ssid = df.loc[i, ["ssid"]].values[0]
        freq = df.loc[i, ["freq"]].values[0]
        addr = df.loc[i, ["addr"]].values[0]
        dist = get_dist(freq, average_rssi)
        data = {"addr": addr,
                "rssi": average_rssi,
                "ssid": ssid,
                "freq": freq,
                "lat": lat,
                "long": long,
                "dist": dist}
        mean_data.append(data)
    df = pd.DataFrame(mean_data)
    return df


def get_locations_distances_weights(df):
    dataset = {}
    for index, row in df.iterrows():
        if row["lat"] in dataset.keys():
            if dataset[row["lat"]][2] < row["rssi"]:
                dataset[row["lat"]] = [row["lat"], row["long"], row["rssi"], row["dist"]]
        else:
            dataset[row["lat"]] = [row["lat"], row["long"], row["rssi"], row["dist"]]
    df = pd.DataFrame(dataset.values(), columns=["lat", "long", "rssi", "dist"])
    locations = []
    distances = []
    weights = []
    for index, row in df.iterrows():
        locations.append([row["lat"], row["long"]])
        distances.append(row["dist"])
        max_sig = -85
        min_sig = -60
        if row["rssi"] < max_sig:
            weight = 0
        elif max_sig <= row["rssi"] <= min_sig:
            weight = np.power(np.abs(np.abs(row["rssi"] - max_sig) / (max_sig - min_sig)), 1)
        else:
            weight = 1

        weights.append(weight)
    return locations, distances, weights


def get_data(gps_path, packet_path):
    gps_data = pd.read_csv(gps_path, names=["latitude", "longitude", "timestamp"])
    gps_data['timestamp'] = gps_data['timestamp'].apply(lambda x: int(x))
    with open(packet_path, 'r') as f:
        char_to_split = "}\n"
        data = f.read()
    new_data = data.split(char_to_split)

    new_data = [line + char_to_split for line in new_data]
    del new_data[-1]
    new_data = [json.loads(line) for line in new_data]
    packets_data = pd.DataFrame(new_data)
    return gps_data, packets_data
