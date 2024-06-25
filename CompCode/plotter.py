import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import pandas as pd
import time

downloads_dir = "C:/Users/chinghta/Downloads/RcCar/session_1719316614.9470584"

# Use a specific style (optional)
plt.style.use("fivethirtyeight")

# Read the CSV file initially
df = pd.read_csv(os.path.join(downloads_dir, "telemetry.csv"))

# Setup the figure and subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))  # 2 rows, 1 column

# Function to update the plots in each animation frame
def animate(i):
    # Read the updated CSV data into DataFrame
    df = pd.read_csv(os.path.join(downloads_dir, "telemetry.csv"))
    
    # Calculate current time and limit data to last 30 seconds
    current_time = time.time()
    min_time = current_time - 30  # Last 30 seconds
    df_recent = df[df["timestamp"] >= min_time]
    
    # Clear the previous plots
    ax1.clear()
    ax2.clear()
    
    # Plot speed on the first subplot
    ax1.plot(df_recent["timestamp"], df_recent["speed"], label="Speed", linewidth=0.8)
    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("Speed")
    ax1.set_title("Speed vs. Timestamp (Last 30 Seconds)")
    ax1.legend()
    
    # Plot heading on the second subplot
    ax2.plot(df_recent["timestamp"], df_recent["heading"], label="Heading", linewidth=0.8, linestyle="--", color="orange")
    ax2.set_xlabel("Timestamp")
    ax2.set_ylabel("Heading")
    ax2.set_title("Heading vs. Timestamp (Last 30 Seconds)")
    ax2.legend()

# Initialize the animation with some initial data
animate(1)

# Start the animation loop with an interval of 100 milliseconds
ani = animation.FuncAnimation(fig, animate, interval=100)

# Adjust layout to prevent overlapping
plt.tight_layout()

# Show the animated plot
plt.show()
