# Temperature and Humidity Sensing System

## Overview
This project implements a real-time temperature and humidity sensing system using an ESP32-WROOM-32D module and a BME680 sensor. The system collects environmental data and provides visualization through Python scripts.

## Hardware Requirements
- ESP32-WROOM-32D microcontroller module (or any equivalent 38-pin ESP32 module)
- USB cable to connect ESP32 to a PC (may be USB-C or micro-USB depending on what ports your ESP32 and PC have)
- BME680 environmental sensor (measures temperature, humidity, pressure, and air quality)
- Jumper wires

## Software Requirements
- PlatformIO IDE (if you have Arduino IDE, copy paste the main.cpp file into the .ino sketch file and run the python script separately in a terminal)
- Python 3.x (for data visualization scripts)
- Required Python libraries:
  - matplotlib
  - pyserial

## Project Structure
```
RTOS-Final-Project/
├── platformio.ini          # PlatformIO configuration
├── src/
│   └── main.cpp           # Main ESP32 firmware
├── scripts/
│   └── plot_serial.py     # Python script for plotting BME680 data
├── include/               # Header files (empty)
├── lib/                   # Libraries (empty)
└── test/                  # Test files (empty)
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
     pip install matplotlib pyserial
     ```
     or just use the requirements.txt file in this repository:
     ```
     pip install -r requirements.txt
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
3. **NOTE: make sure the COM port of your ESP32 matches the one on the python script.** Mine was COM7 but yours may be different.
4. The scripts will generate plots for temperature, humidity, and other sensor readings

## Features
- Real-time temperature and humidity monitoring
- BME680 sensor integration for comprehensive environmental sensing
- RTOS-based multitasking for efficient data collection
- Python-based data visualization
- PlatformIO for easy development and deployment

## License
This project is licensed under the terms specified in the LICENSE file.
