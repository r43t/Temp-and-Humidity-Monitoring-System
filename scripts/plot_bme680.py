import serial
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Change this to your actual port
PORT = "COM7"
BAUD = 115200
MAX_POINTS = 150

ser = serial.Serial(PORT, BAUD, timeout=0.2)

time_s = deque(maxlen=MAX_POINTS)
temp_c = deque(maxlen=MAX_POINTS)
humidity_pct = deque(maxlen=MAX_POINTS)
pressure_hpa = deque(maxlen=MAX_POINTS)
gas_kohm = deque(maxlen=MAX_POINTS)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

line_temp, = ax1.plot([], [], label="Temperature (°C)")
line_hum, = ax2.plot([], [], label="Humidity (%)")

latest_text = ax1.text(
    0.02, 0.95, "", transform=ax1.transAxes, verticalalignment="top"
)

ax1.set_ylabel("Temp (°C)")
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

        # Skip header line
        if raw.startswith("ms,"):
            continue

        parts = raw.split(",")
        if len(parts) != 5:
            continue

        try:
            ms = float(parts[0])
            t = float(parts[1])
            h = float(parts[2])
            p = float(parts[3])
            g = float(parts[4])
        except ValueError:
            continue

        time_s.append(ms / 1000.0)
        temp_c.append(t)
        humidity_pct.append(h)
        pressure_hpa.append(p)
        gas_kohm.append(g)

    if not time_s:
        return line_temp, line_hum, latest_text

    t0 = time_s[0]
    x = [v - t0 for v in time_s]

    line_temp.set_data(x, temp_c)
    line_hum.set_data(x, humidity_pct)

    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    latest_text.set_text(
        f"Pressure: {pressure_hpa[-1]:.1f} hPa | Gas: {gas_kohm[-1]:.1f} kΩ"
    )

    return line_temp, line_hum, latest_text

ani = FuncAnimation(fig, update, interval=200, blit=False)
plt.tight_layout()

try:
    plt.show()
finally:
    ser.close()