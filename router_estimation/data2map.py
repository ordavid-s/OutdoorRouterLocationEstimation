import folium
import json


from data_processing.calculations import get_coordinates
from data_processing.postprocess import get_locations_distances_weights, merge_data, get_data

CONFIG_NAME = "config.json"


def get_config():
    # Opening JSON file
    with open(CONFIG_NAME) as nf:
        data = json.load(nf)
    return data


if __name__ == '__main__':
    config = get_config()
    ssid = config["maps"]["ssid"]
    gps_data, packets_data = get_data(config["maps"]["gps_path"], config["maps"]["packets_path"] )
    print("[+] retrieved data")
    df = merge_data(gps_data, packets_data)
    print("[+] merged data")
    df = df.loc[df['ssid'] == ssid]
    df = df.loc[df['rssi'] > config["data_processing"]["min_usable_rssi"]]
    if config["data_processing"]["limit_packets"]:
        df = df.iloc[::int(len(df)/config["data_processing"]["num_packets_to_use"]), :]
    if len(df) < config["data_processing"]["num_packets_to_use"] - 1:
        print("[!] Not enough data")
        exit(1)
    m = folium.Map(location=[config["maps"]["init_lat"], config["maps"]["init_long"]],
                   zoom_start=config["maps"]["init_zoom"])
    if config["maps"]["show_rssi_circles"]:
        for index, row in df.iterrows():
            folium.CircleMarker(
                location=[row["lat"], row["long"]],
                radius=row["dist"],
                popup=row["dist"],
                color="#3186cc",
                fill=True,
                fill_color="#3186cc",
            ).add_to(m)
    locations, distances, weights = get_locations_distances_weights(df)
    print("[+] calculating coordinates")
    lat, long = get_coordinates(locations, distances, weights)
    folium.Marker(
        location=[lat, long],
        popup=ssid,
        icon=folium.Icon(icon=config["maps"]["icon_to_display"]),
    ).add_to(m)
    m.save(config["maps"]["map_save_path"])
