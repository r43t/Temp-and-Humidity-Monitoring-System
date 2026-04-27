# RTOS Final Project: Temperature and Humidity Sensing System

## Overview
This project implements a real-time temperature and humidity sensing system using an ESP32-WROOM-32D module and a BME680 sensor. The system collects environmental data and provides visualization through Python scripts.

## Hardware Requirements
- ESP32-WROOM-32D microcontroller module
- BME680 environmental sensor (measures temperature, humidity, pressure, and air quality)
- Appropriate power supply (3.3V for ESP32)
- Connecting wires and breadboard (for prototyping)

## Software Requirements
- PlatformIO IDE or VS Code with PlatformIO extension
- Python 3.x (for data visualization scripts)
- Required Python libraries:
  - matplotlib
  - numpy
  - pandas (if needed for data processing)

## Project Structure
```
RTOS-Final-Project/
├── platformio.ini          # PlatformIO configuration
├── src/
│   └── main.cpp           # Main ESP32 firmware
├── scripts/
│   └── plot_serial.py     # Python script for plotting BME680 data
├── include/               # Header files
├── lib/                   # Libraries
└── test/                  # Test files
```

## Setup Instructions

### 1. Hardware Setup
1. Connect the BME680 sensor to the ESP32:
   - VCC to 3.3V
   - GND to GND
   - SDA to GPIO 21 (I2C data)
   - SCL to GPIO 22 (I2C clock)
2. Ensure proper power supply to the ESP32 module.

### 2. Software Setup
1. Install PlatformIO:
   - Download and install VS Code
   - Install the PlatformIO extension

2. Clone or download this repository:
   ```
   git clone https://github.com/r43t/RTOS-Final-Project.git
   cd RTOS-Final-Project
   ```

3. Open the project in PlatformIO:
   - Open VS Code
   - Open the project folder
   - PlatformIO should automatically detect the project

4. Install dependencies:
   - PlatformIO will handle ESP32 framework and library dependencies
   - For Python scripts, install required libraries:
     ```
     pip install matplotlib numpy pandas
     ```

### 3. Build and Upload
1. Connect the ESP32 to your computer via USB
2. In PlatformIO, select the correct board (ESP32 Dev Module)
3. Build the project: Click the build button or use `Ctrl+Alt+B`
4. Upload to ESP32: Click the upload button or use `Ctrl+Alt+U`

## Usage

### Running the ESP32 Firmware
1. After uploading, the ESP32 will start collecting sensor data
2. The system uses RTOS tasks to handle sensor readings and data transmission
3. Sensor data is output via serial monitor or can be configured for wireless transmission

### Data Visualization
1. Run the Python scripts to visualize collected data: 
   ```
   python scripts/plot_serial.py
   ```
   for fahrenheit readings.
3. Ensure sensor data is saved in a compatible format (CSV or similar)
4. The scripts will generate plots for temperature, humidity, and other sensor readings

## Features
- Real-time temperature and humidity monitoring
- BME680 sensor integration for comprehensive environmental sensing
- RTOS-based multitasking for efficient data collection
- Python-based data visualization
- PlatformIO for easy development and deployment

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License
This project is licensed under the terms specified in the LICENSE file.
