import serial
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ser = serial.Serial("COM7", 115200, timeout=0.2)

data = {"time": deque(maxlen=150), "temp": deque(maxlen=150), "hum": deque(maxlen=150), "pres": deque(maxlen=150), "gas": deque(maxlen=150)}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
plt.subplots_adjust(right=0.75)
line_temp, = ax1.plot([], [], label = "Temperature (°F)", color = "blue")
line_hum, = ax2.plot([], [], label = "Humidity (%)", color = "red")

for ax, ylabel in [(ax1, "Temperature (°F)"), (ax2, "Humidity (%)")]:
    ax.set_ylabel(ylabel)
    ax.grid(True)
    ax.legend(loc = "upper right")

ax2.set_xlabel("Time (s)")
live_box = fig.text(0.75,0.90, "",fontsize = 11,va = "top",bbox = dict(boxstyle = "round",facecolor = "white",edgecolor = "black"))

def update(_):
    while ser.in_waiting:
        try:
            raw = ser.readline().decode().strip()
            if not raw or raw.startswith("ms,"):
                continue
            ms, t_c, h, p, g = map(float, raw.split(","))
            data["time"].append(ms / 1000)
            data["temp"].append(t_c * 9/5 + 32)     # converting celsius -> fahrenheit
            data["hum"].append(h)
            data["pres"].append(p)
            data["gas"].append(g)
        except:
            continue
    if not data["time"]:
        return line_temp, line_hum, live_box
    t0 = data["time"][0]
    x = [t - t0 for t in data["time"]]
    line_temp.set_data(x, data["temp"])
    line_hum.set_data(x, data["hum"])

    for ax in (ax1, ax2):
        ax.relim()
        ax.autoscale_view()

    live_box.set_text(
        "Live Sensor Values\n"
        f"Temperature: {data['temp'][-1]:.2f} °F\n"
        f"Humidity: {data['hum'][-1]:.2f} %\n"
        f"Pressure: {data['pres'][-1]:.2f} hPa\n"
        f"Gas: {data['gas'][-1]:.2f} kΩ"
    )
    return line_temp, line_hum, live_box

ani = FuncAnimation(fig, update, interval=200)
plt.tight_layout()

try:
    plt.show()
finally:
    ser.close()