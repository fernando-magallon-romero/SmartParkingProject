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
