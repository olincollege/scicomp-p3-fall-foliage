import numpy as np
import matplotlib.pyplot as plt

def linear_interpolation_color(value, color_start, color_middle, color_end):

    # Determine the interpolation ranges
    if value <= 0.5:
        t = value * 2  # Scale the value for the first half (0 to 0.5)
        r = int((1 - t) * color_start[0] + t * color_middle[0])
        g = int((1 - t) * color_start[1] + t * color_middle[1])
        b = int((1 - t) * color_start[2] + t * color_middle[2])
    elif value <= 1:
        t = (value - 0.5) * 2  # Scale the value for the second half (0.5 to 1)
        r = int((1 - t) * color_middle[0] + t * color_end[0])
        g = int((1 - t) * color_middle[1] + t * color_end[1])
        b = int((1 - t) * color_middle[2] + t * color_end[2])
    
    else:
        raise ValueError("Color scaled down outside of range")
    
    return r, g, b

# Define the RGB values for green, yellow, orange, and red
green_color = (100, 150, 20)
yellow_color = (220, 170, 60)
red_color = (160, 40, 40)

# Generate colors for a range of values
num_points = 100
values = np.linspace(0, 1, num_points)
colors = [linear_interpolation_color(value, green_color, yellow_color, red_color) for value in values]

# Plot the colors
fig, ax = plt.subplots(figsize=(10, 1))
ax.imshow([colors], aspect='auto', extent=(0, 1, 0, 1))
ax.set_axis_off()
plt.show()
