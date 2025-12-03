# Smart Parking IoT Simulation – SDSU Parking MVP 

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

## Inputs
Ensure the two input CSV files are located in the same folder as `smart_parking_map.py`:
  - LADOT_Parking_Meter_Occupancy.csv
  - IIoT_Smart_Parking_Management.csv

## Outputs
This project generates the following outputs:
  - `SmartParkingMap.html` --> An interactive Folium map showing parking availability
  
## Main Code File
The main code file for this project is `smart_parking_map.py`. It is responsible for:
  - Loading both datasets
  - Assigning clustering coordinates (parking structures)
  - Rendering Folium map with interactive markers (parking spots)
  - Adding capacity calculations and overlays

## Running the Code
To run this project, once all files are downloaded, go to the project root directory then run:
  - `pip install pandas folium`
  - `python smart_parking_map.py`

It will then download a file named `SmartParkingMap.html`, you will open this to view the interactive map in any browser

## Deployment
This project currently runs locally only

## License
MIT License - Free to modify and distribute

## Contact
For any questions, issues running the code, or suggested improvements, please contact Fernando Magallon-Romero at fmagallonromer2098@sdsu.edu

GitHub: https://github.com/fernando-magallon-romero
