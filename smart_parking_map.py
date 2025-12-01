# ======================================================
# smart_parking_map.py
#
# Smart Parking Folium Map
# ------------------------------------------------------
# - Loads two CSV files:
#       1) LADOT_Parking_Meter_Occupancy.csv
#       2) IIoT_Smart_Parking_Management.csv
# - Uses SDSU Parking Structure latitude/longitude values for
#   parking space (so we can visualize them on a map)
# - Builds an interactive folium map with:
#       * LADOT layer (occupied vs vacant)
#       * IoT layer (occupied vs vacant)
# - Saves output as SmartParkingMap.html
# ======================================================

import pandas as pd
import folium
import math

# -----------------------------
# 1. Configuration
# -----------------------------

# CSV file names (must be in same folder as this code)
LADOT_CSV = "LADOT_Parking_Meter_Occupancy.csv"
IOT_CSV   = "IIoT_Smart_Parking_Management.csv"

# Cluster centers for each SDSU parking structure
PARKING_CLUSTERS = {
    "PS1":  (32.775596, -117.067279),
    "PS3":  (32.772323, -117.066375),
    "PS4":  (32.771313, -117.066391),
    "PS16": (32.778200, -117.068776),
    "PS8":  (32.777959, -117.074231),
    "PS12": (32.775702, -117.074781),
    "PS7":  (32.772526, -117.076750),
    "PS6":  (32.772089, -117.074934),
}

PER_ROW = 8         # a narrow grid for the parking spots
SPACING = 0.00015   # tight cluster around each structure

# -----------------------------
# 2. Helper: generate parking cluster coordinates
# -----------------------------

def generate_fake_coordinates(ids, base_lat, base_lon, spacing=0.0002, per_row=10):
    """
    Center the fake grid around (base_lat, base_lon) so the cluster
    stays roughly on top of the parking structure.
    """
    ids = list(ids)
    n = len(ids)
    if n == 0:
        return {}

    # How many rows we need for this many IDs?
    num_rows = math.ceil(n / per_row)

    # We'll treat base_lat/base_lon as the center of the grid
    row_center = (num_rows - 1) / 2.0
    col_center = (per_row - 1) / 2.0

    coords = {}
    for i, pid in enumerate(ids):
        row = i // per_row
        col = i % per_row

        lat = base_lat + (row - row_center) * spacing
        lon = base_lon + (col - col_center) * spacing

        coords[pid] = (lat, lon)

    return coords

def assign_coords_to_clusters(ids, cluster_centers, spacing=0.0002, per_row=10):
    ids = list(ids)
    coords = {}
    cluster_map = {}
    n = len(ids)
    k = len(cluster_centers)

    if k == 0 or n == 0:
        return coords, cluster_map

    # Roughly even split of spots among structures
    chunk_size = math.ceil(n / k)
    idx = 0

    for name, (base_lat, base_lon) in cluster_centers.items():
        chunk = ids[idx:idx + chunk_size]
        if not chunk:
            break

        local_coords = generate_fake_coordinates(
            chunk,
            base_lat,
            base_lon,
            spacing=spacing,
            per_row=per_row
        )

        coords.update(local_coords)
        for pid in chunk:
            cluster_map[pid] = name
        idx += chunk_size

    return coords, cluster_map

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
    ladot_coords, ladot_cluster_map = assign_coords_to_clusters(
        ladot_ids,
        PARKING_CLUSTERS,
        spacing=SPACING,
        per_row=PER_ROW
    )

    ladot["Latitude"] = ladot["SpaceID"].apply(lambda x: ladot_coords[x][0])
    ladot["Longitude"] = ladot["SpaceID"].apply(lambda x: ladot_coords[x][1])
    ladot["Structure"] = ladot["SpaceID"].apply(lambda x: ladot_cluster_map.get(x, "Unknown"))

    # ----- IoT coordinates -----
    iot_ids = iot["Parking_Spot_ID"].unique()
    iot_coords, iot_cluster_map = assign_coords_to_clusters(
        iot_ids,
        PARKING_CLUSTERS,
        spacing=SPACING,
        per_row=PER_ROW
    )   

    iot["Latitude"] = iot["Parking_Spot_ID"].apply(lambda x: iot_coords[x][0])
    iot["Longitude"] = iot["Parking_Spot_ID"].apply(lambda x: iot_coords[x][1])
    iot["Structure"] = iot["Parking_Spot_ID"].apply(lambda x: iot_cluster_map.get(x, "Unknown"))

    # Normalize LADOT occupancy status:
    ladot["OccNormalized"] = (
        ladot["OccupancyState"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.upper()
        .str.strip()
        .apply(lambda v: "VACANT" if v == "VACANT" else "OCCUPIED")
    )

    # Each LADOT row = one marker on the map, so use size (row count)
    capacity = (
        ladot.groupby("Structure")
             .agg(
                 total_spots=("SpaceID", "size"),  # how many LADOT markers in that structure
                 occupied=("OccNormalized", lambda s: (s == "OCCUPIED").sum())
             )
             .reset_index()
    )

    capacity["vacant"] = capacity["total_spots"] - capacity["occupied"]
    capacity["pct_full"] = (capacity["occupied"] / capacity["total_spots"] * 100).round(1)

    # Build small HTML table for overlay
    rows_html = ""
    for _, r in capacity.iterrows():
        struct = r["Structure"]
        total = int(r["total_spots"])
        occ   = int(r["occupied"])
        vac   = int(r["vacant"])
        pct   = r["pct_full"]
        rows_html += (
            f"<tr>"
            f"<td style='padding:2px 4px;'>{struct}</td>"
            f"<td style='padding:2px 4px;'>{total}</td>"
            f"<td style='padding:2px 4px;'>{occ}</td>"
            f"<td style='padding:2px 4px;'>{vac}</td>"
            f"<td style='padding:2px 4px;'>{pct}%</td>"
            f"</tr>"
        )

    capacity_html = (
        "<div style=\""
        "position: fixed; top: 80px; right: 20px; z-index:9999;"
        "background: white; padding: 8px 10px; border: 1px solid #ccc;"
        "border-radius: 6px; font-size: 11px; font-family: system-ui, sans-serif;"
        "max-height: 260px; overflow-y: auto;\">"
        "<b>Structure Capacity (LADOT Only)</b>"
        "<table style='border-collapse: collapse; margin-top: 6px;'>"
        "<tr>"
        "<th style='padding:2px 4px; border-bottom:1px solid #ddd;'>Struct</th>"
        "<th style='padding:2px 4px; border-bottom:1px solid #ddd;'>Total</th>"
        "<th style='padding:2px 4px; border-bottom:1px solid #ddd;'>Occ</th>"
        "<th style='padding:2px 4px; border-bottom:1px solid #ddd;'>Vac</th>"
        "<th style='padding:2px 4px; border-bottom:1px solid #ddd;'>% Full</th>"
        "</tr>"
        + rows_html +
        "</table>"
        "</div>"
    )

    # -------------------------
    # Build the folium map
    # -------------------------
    print("Building folium map...")
    m = folium.Map(location=[32.7763, -117.0720], zoom_start=16)

    ladot_layer = folium.FeatureGroup(name="LADOT Occupancy")
    iot_layer   = folium.FeatureGroup(name="IoT Occupancy")

    # ---------- STYLING: TITLE OVERLAY ----------
    title_html = """
         <div style="
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            background: rgba(0,0,0,0.75);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            font-family: system-ui, sans-serif;
            font-size: 16px;">
            <b>SDSU Smart Parking Map</b><br>
            <span style="font-size: 12px;">
                Green = Available | Red = Occupied
            </span>
         </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    # ---------- STYLING: LEGEND OVERLAY ----------
    legend_html = """
    <div style="
         position: fixed;
         bottom: 20px;
         left: 20px;
         z-index:9999;
         background: white;
         padding: 10px 12px;
         border: 1px solid #ccc;
         border-radius: 6px;
         font-size: 12px;
         font-family: system-ui, sans-serif;">
      <b>Legend</b><br>
      <i style="background: green; width:10px; height:10px; display:inline-block;"></i>
      Available<br>
      <i style="background: red; width:10px; height:10px; display:inline-block;"></i>
      Occupied
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # ---------- STYLING: CAPACITY OVERLAY (LADOT ONLY) ----------
    m.get_root().html.add_child(folium.Element(capacity_html))

    # ---------- JS: Reserve function ----------
    reserve_js = """
    <script>
    function reserveSpot(elId) {
        var container = document.getElementById(elId);
        if (!container) return;

        // Change the status text
        var statusSpan = container.querySelector('.spot-status');
        if (statusSpan) {
            statusSpan.textContent = 'RESERVED (demo)';
            statusSpan.style.color = 'red';
        }

        // Disable the button after reserving
        var btn = container.querySelector('button');
        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Spot Reserved';
        }
    }
    </script>
    """
    m.get_root().html.add_child(folium.Element(reserve_js))

    # -------------------------
    # LADOT markers
    # -------------------------

    # OccupancyState is typically "OCCUPIED" or "VACANT"
    for idx, row in ladot.iterrows():
        status = str(row.get("OccupancyState", "UNKNOWN")).upper()
        color = "green" if status == "VACANT" else "red"

        # give each popup a unique HTML id
        popup_id = f"ladot_spot_{row['SpaceID']}_{idx}"

        if status == "VACANT":
            popup_html = f"""
            <div id="{popup_id}">
                <b>LADOT Spot:</b> {row['SpaceID']}<br>
                <b>Status:</b> <span class="spot-status">VACANT</span><br>
                <b>Event Time (UTC):</b> {row.get('EventTime_UTC', 'N/A')}<br><br>
                <button onclick="reserveSpot('{popup_id}')">
                    Reserve this spot
                </button>
            </div>
            """
        else:
            popup_html = f"""
            <div>
                <b>LADOT Spot:</b> {row['SpaceID']}<br>
                <b>Status:</b> {status}<br>
                <b>Event Time (UTC):</b> {row.get('EventTime_UTC', 'N/A')}
            </div>
            """

        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=color, icon="car", prefix="fa")
        ).add_to(ladot_layer)

    # -------------------------
    # IoT markers
    # -------------------------

    # Sensor_Reading_Proximity:
    #   we will assume 0 = VACANT, anything else = OCCUPIED
    for idx, row in iot.iterrows():
        prox = row.get("Sensor_Reading_Proximity", 1)
        status = "VACANT" if prox == 0 else "OCCUPIED"
        color = "green" if status == "VACANT" else "red"
        popup_id = f"iot_spot_{row['Parking_Spot_ID']}_{idx}"

        if status == "VACANT":
            popup_html = f"""
            <div id="{popup_id}">
                <b>IoT Spot:</b> {row['Parking_Spot_ID']}<br>
                <b>Status:</b> <span class="spot-status">VACANT</span><br>
                <b>Timestamp:</b> {row.get('Timestamp', 'N/A')}<br><br>
                <button onclick="reserveSpot('{popup_id}')">
                    Reserve this spot
                </button>
            </div>
            """
        else:
            popup_html = f"""
            <div>
                <b>IoT Spot:</b> {row['Parking_Spot_ID']}<br>
                <b>Status:</b> {status}<br>
                <b>Timestamp:</b> {row.get('Timestamp', 'N/A')}
            </div>
            """
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_html, max_width=250),
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

if __name__ == "__main__":
    main()
