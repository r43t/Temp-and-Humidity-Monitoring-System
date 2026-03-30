import serial
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

PORT = "COM7"
BAUD = 115200
MAX_POINTS = 150

ser = serial.Serial(PORT, BAUD, timeout=0.2)

time_s = deque(maxlen=MAX_POINTS)
temp_f = deque(maxlen=MAX_POINTS)
humidity_pct = deque(maxlen=MAX_POINTS)
pressure_hpa = deque(maxlen=MAX_POINTS)
gas_kohm = deque(maxlen=MAX_POINTS)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
plt.subplots_adjust(right=0.75)
line_temp, = ax1.plot([], [], label="Temperature (°F)")
line_hum, = ax2.plot([], [], label="Humidity (%)")

live_box = fig.text(0.75, 0.90, "", fontsize=11, verticalalignment="top", bbox=dict(boxstyle="round", facecolor="white", edgecolor="black"))

ax1.set_ylabel("Temp (°F)")
ax2.set_ylabel("Humidity (%)")
ax2.set_xlabel("Time (s)")
ax1.legend(loc="upper right")
ax2.legend(loc="upper right")
ax1.grid(True)
ax2.grid(True)

def update(frame):
    while ser.in_waiting:
        raw = ser.readline().decode("utf-8", errors="ignore").strip()
        if not raw:
            continue
        if raw.startswith("ms,"):
            continue
        parts = raw.split(",")
        if len(parts) != 5:
            continue
        try:
            ms = float(parts[0])
            t_c = float(parts[1])
            h = float(parts[2])
            p = float(parts[3])
            g = float(parts[4])
        except ValueError:
            continue

        t_f = (t_c * 9/5) + 32      # Convert Celsius -> Fahrenheit
        time_s.append(ms / 1000.0)
        temp_f.append(t_f)
        humidity_pct.append(h)
        pressure_hpa.append(p)
        gas_kohm.append(g)

    if not time_s:
        return line_temp, line_hum, live_box

    t0 = time_s[0]
    x = [v - t0 for v in time_s]
    line_temp.set_data(x, temp_f)
    line_hum.set_data(x, humidity_pct)
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    # Update live values
    live_box.set_text(f"Live Sensor Values\n"
        f"-------------------------\n"
        f"Temperature: {temp_f[-1]:.2f} °F\n"
        f"Humidity: {humidity_pct[-1]:.2f} %\n"
        f"Pressure: {pressure_hpa[-1]:.2f} hPa\n"
        f"Gas: {gas_kohm[-1]:.2f} kΩ"
    )
    return line_temp, line_hum, live_box

ani = FuncAnimation(fig, update, interval=200, blit=False)
plt.tight_layout()

try:
    plt.show()
finally:
    ser.close()