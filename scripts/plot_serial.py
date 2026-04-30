import serial
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# connect to ESP32 via serial port
ser = serial.Serial("COM7", 115200, timeout=0.2)
# buffer to store sensor data (older data is discarded when max length is reached)
data = {"time": deque(maxlen=150), 
    "temp": deque(maxlen=150), 
    "hum": deque(maxlen=150), 
    "pres": deque(maxlen=150), 
    "gas": deque(maxlen=150)
}
# creating 2 plots vertically that share the same x-axis (time)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
plt.subplots_adjust(right=0.75)
# initialize 2 line objects that will be "live" (update dynamically)
line_temp, = ax1.plot([], [], label = "Temperature (°F)", color = "blue")
line_hum, = ax2.plot([], [], label = "Humidity (%)", color = "red")
# configure axis labels and grids
for ax, ylabel in [(ax1, "Temperature (°F)"), (ax2, "Humidity (%)")]:
    ax.set_ylabel(ylabel)
    ax.grid(True)
    ax.legend(loc = "upper right")

ax2.set_xlabel("Time (s)")  # shared x axis label
# Text box to display sensor values in real time
live_box = fig.text(0.75,0.90,"",fontsize=11,va="top",bbox=dict(boxstyle="round",facecolor="white",edgecolor="black"))

# function to update animation of live graph
def update(_):
    while ser.in_waiting:   # read available serial data
        try:
            raw = ser.readline().decode().strip()   # read one line from serial
            if not raw:
                continue    # skip empty lines
            ms, t_c, h, p, g = map(float, raw.split(","))   # parse values using comma delimiter
            data["time"].append(ms / 1000)          # store values 
            data["temp"].append(t_c * 9/5 + 32)     # converting celsius -> fahrenheit
            data["hum"].append(h)
            data["pres"].append(p)
            data["gas"].append(g)
        except:
            continue    # ignore incomplete serial lines
    if not data["time"]:
        return line_temp, line_hum, live_box    # if no data yet, dont update plot
    # fix time axis to start at 0 on live graph
    t0 = data["time"][0]
    x = [t - t0 for t in data["time"]]
    # update plotted data
    line_temp.set_data(x, data["temp"])
    line_hum.set_data(x, data["hum"])
    # recalculate axis limits based on new data
    for ax in (ax1, ax2):
        ax.relim()
        ax.autoscale_view()
    # update text box of live data
    live_box.set_text(
        "Live Sensor Values\n"
        f"Temperature: {data['temp'][-1]:.2f} °F\n"
        f"Humidity: {data['hum'][-1]:.2f} %\n"
        f"Pressure: {data['pres'][-1]:.2f} hPa\n"
        f"Gas: {data['gas'][-1]:.2f} kΩ"
    )
    return line_temp, line_hum, live_box
# create live graph and update every 200 milliseconds
ani = FuncAnimation(fig, update, interval=200)
plt.tight_layout()  # adjust layout to prevent overlap of figures

try:
    plt.show()      # start animation of live graph
finally:
    ser.close()     # close serial port when exiting