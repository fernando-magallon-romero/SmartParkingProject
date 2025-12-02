# Smart Parking IoT Simulation – SDSU Parking MVP
This project demonstrates a simulated Smart Parking system designed for SDSU parking garages.  
Due to real sensor and infrastructure limitations, this MVP uses Python, Folium, and **sample datasets** to visualize parking availability on an interactive map. 
A Figma UI prototype accompanies the system to demonstrate what a full SDSU-facing app could look like.

The goal of this project is to show how IoT technologies, real-time sensors, and mapped data can improve parking efficiency, reduce student, staff, decrease congestion on campus and faculty frustration.

---

## Project Overview
Students at SDSU regularly waste 10–20 minutes searching for available parking.  
This MVP addresses that challenge by simulating a system that:

- Reads parking datasets  
- Processes occupancy status  
- Generates an interactive campus parking map  
- Shows **available** and **occupied** spots  
- Lays out the foundation for real future sensor integration  

Our prototype combines:
1. **Real occupancy data** (LADOT dataset)  
2. **Simulated IoT sensor readings** (proximity-based dataset)  
3. **A Folium-based map** showing spot availability  
4. **Figma UI mockups** for future mobile integration  

---

## Project Structure
smart_parking_map.py

SmartParkingMap.html

LADOT_Parking_Meter_Occupancy.csv

IIoT_Smart_Parking_Management.csv

README.md

---

## Datasets Used 

### 1. LADOT Parking Meter Occupancy 
Fields include:
- `SpaceID`
- `EventTime_UTC`
- `OccupancyState` (VACANT / OCCUPIED)

### 2. IoT Smart Parking Management Dataset (Simulated)
Fields include:
- `Parking_Spot_ID`
- `Sensor_Reading_Proximity` (0 = vacant, 1 = occupied)
- `Timestamp`

---

## How to Run 

### **1. Install Dependencies**
pip install pandas folium 

### **2. Run Script**
python smart_parking_map.py 

### **3. View Output**
SmartParkingMap.html

---
---
---
Below is what I added: fernandoMR 

Team Member List:
1. Fernando Magallon-Romero
2. Xabier Rivera
3. Luis Saabedra


## Description
This project was created by Fernando Magallon-Romero for MIS 695 (Strategic Program Management).
It simulates a Smart Parking Management System by combining two datasets - LADOT Parking Meter Occupancy and IIoT Smart Parking - and visualizing real-time availability using Folium (interactive web mapping).

The system assigns parking spaces to SDSU parking structures and indicates whether each spot is:
  - 🟢 Available
  - 🔴 Occupied
  - ⛔ Reserved (demo functionality)

The result is displayed in an interactive HTML map with:
  - Popup reservation buttons
  - Live capacity % by structure
  - Layer toggles (LADOT vs IoT data)

## Installation
Requires Python ≥ 3.8
Install dependencies:
  - `pip install pandas folium`
Ensure the two input CSV files are located in the same folder as smart_parking_map.py:
  - LADOT_Parking_Meter_Occupancy.csv
  - IIoT_Smart_Parking_Management.csv

## Inputs
The project uses the following datasets:
  - LADOT_Parking_Meter_Occupancy.csv
  - IIoT_Smart_Parking_Management.csv

## Outputs
This project generates the following outputs:
  - SmartParkingMap.html --> An interactive Folium map showing parking availability
  
## Main Code File
The main code file for this project is smart_parking_map.py. It is responsible for:
  - Loading both datasets
  - Assigning clustering coordinates (parking structures)
  - Rendering Folium map with interactive markers (parking spots)
  - Adding capacity calculations and overlays

## Running the Code
To run this project, once all files are downloaded, from the project root directory run:
  - `pip install pandas folium`
  - `python smart_parking_map.py`
It will then download a file named SmartParkingMap.html, you will open this to view the interactive map in any browser

## Deployment
This project currently runs locally only

## License
MIT License – Free to modify and distribute.

## Contact
For any questions, issues running the code, or suggested improvements, please contact Fernando Magallon-Romero at fmagallonromer2098@sdsu.edu
GitHub: https://github.com/fernando-magallon-romero
