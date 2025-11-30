# ======================================================
# smart_parking_map.py
#
# Smart Parking Folium Map (with fake coordinates)
# ------------------------------------------------------
# - Loads two CSV files:
#       1) LADOT_Parking_Meter_Occupancy.csv
#       2) IIoT_Smart_Parking_Management.csv
# - Creates FAKE latitude/longitude values for each
#   parking space (so we can visualize them on a map)
# - Builds an interactive folium map with:
#       * LADOT layer (occupied vs vacant)
#       * IoT layer (occupied vs vacant)
# - Saves output as SmartParkingMap.html
# ======================================================

import pandas as pd
import folium


# -----------------------------
# 1. Configuration
# -----------------------------

# CSV file names (same folder as this script)
LADOT_CSV = "LADOT_Parking_Meter_Occupancy.csv"
IOT_CSV   = "IIoT_Smart_Parking_Management.csv"

# Base coordinate near SDSU (just for visualization)
BASE_LAT = 32.7755
BASE_LON = -117.0710

# How many markers per row in the fake grid
PER_ROW = 10
# How far apart each marker is (in degrees)
SPACING = 0.0002


# -----------------------------
# 2. Helper: generate fake coordinates
# -----------------------------

def generate_fake_coordinates(ids, base_lat, base_lon, spacing=0.0002, per_row=10):
    """
    Given a list/array of unique IDs, generate a small grid of
    fake (lat, lon) coordinates so we can plot them on a map.

    ids      : iterable of unique spot IDs
    base_lat : starting latitude
    base_lon : starting longitude
    spacing  : distance between markers (degrees)
    per_row  : how many markers per "row" in the grid
    """
    coords = {}
    for i, pid in enumerate(ids):
        row = i // per_row
        col = i % per_row
        lat = base_lat + (row * spacing)
        lon = base_lon + (col * spacing)
        coords[pid] = (lat, lon)
    return coords


# -----------------------------
# 3. Main script
# -----------------------------

def main():
    # -------------------------
    # Load CSV data
    # -------------------------
    print("Loading CSV files...")
    ladot = pd.read_csv(LADOT_CSV)
    iot   = pd.read_csv(IOT_CSV)

    # (Optional) down-sample so the map isn't crazy busy
    # Comment these two lines out if you want all rows
    ladot = ladot.head(150)
    iot   = iot.head(150)

    print("LADOT columns:", ladot.columns.tolist())
    print("IoT columns:", iot.columns.tolist())

    # -------------------------
    # Generate fake coordinates
    # -------------------------

    # LADOT uses SpaceID as the parking spot identifier
    ladot_ids = ladot["SpaceID"].unique()
    ladot_coords = generate_fake_coordinates(
        ladot_ids,
        BASE_LAT,
        BASE_LON,
        spacing=SPACING,
        per_row=PER_ROW
    )

    ladot["Latitude"] = ladot["SpaceID"].apply(lambda x: ladot_coords[x][0])
    ladot["Longitude"] = ladot["SpaceID"].apply(lambda x: ladot_coords[x][1])

    # IoT dataset uses Parking_Spot_ID as the identifier
    # Shift it slightly south so it doesn't overlap exactly
    iot_ids = iot["Parking_Spot_ID"].unique()
    iot_coords = generate_fake_coordinates(
        iot_ids,
        BASE_LAT - 0.002,   # a little below the LADOT grid
        BASE_LON,
        spacing=SPACING,
        per_row=PER_ROW
    )

    iot["Latitude"] = iot["Parking_Spot_ID"].apply(lambda x: iot_coords[x][0])
    iot["Longitude"] = iot["Parking_Spot_ID"].apply(lambda x: iot_coords[x][1])

    # -------------------------
    # Build the folium map
    # -------------------------
    print("Building folium map...")
    m = folium.Map(location=[BASE_LAT, BASE_LON], zoom_start=16)

    ladot_layer = folium.FeatureGroup(name="LADOT Occupancy")
    iot_layer   = folium.FeatureGroup(name="IoT Occupancy")

    # -------------------------
    # LADOT markers
    # -------------------------
    # OccupancyState is typically "OCCUPIED" or "VACANT"
    for _, row in ladot.iterrows():
        status = str(row.get("OccupancyState", "UNKNOWN")).upper()
        color = "green" if status == "VACANT" else "red"

        popup_text = (
            f"LADOT Spot: {row['SpaceID']}<br>"
            f"Status: {status}<br>"
            f"Event Time (UTC): {row.get('EventTime_UTC', 'N/A')}"
        )

        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color=color, icon="car", prefix="fa")
        ).add_to(ladot_layer)

    # -------------------------
    # IoT markers
    # -------------------------
    # Sensor_Reading_Proximity:
    #   we will assume 0 = VACANT, anything else = OCCUPIED
    for _, row in iot.iterrows():
        prox = row.get("Sensor_Reading_Proximity", 1)
        status = "VACANT" if prox == 0 else "OCCUPIED"
        color = "green" if status == "VACANT" else "red"

        popup_text = (
            f"IoT Spot: {row['Parking_Spot_ID']}<br>"
            f"Status: {status}<br>"
            f"Timestamp: {row.get('Timestamp', 'N/A')}"
        )

        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(iot_layer)

    # Add layers & controls
    ladot_layer.add_to(m)
    iot_layer.add_to(m)
    folium.LayerControl().add_to(m)

    # -------------------------
    # Save map
    # -------------------------
    output_file = "SmartParkingMap.html"
    m.save(output_file)
    print(f"Map saved as {output_file}")
    print("Open it in your browser to view the interactive map.")


# Standard Python entry point
if __name__ == "__main__":
    main()
