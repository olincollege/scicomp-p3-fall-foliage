import numpy as np

def sind(angle_deg):
    return(np.sin(np.radians(angle_deg)))

def cosd(angle_deg):
    return(np.cos(np.radians(angle_deg)))

def tand(angle_deg):
    return(np.tan(np.radians(angle_deg)))

def arcsind(val):
    return(np.arcsin(val) * (180 / np.pi))

def declination_angle(day_of_year):
    return arcsind(sind(-23.44) * cosd((360/365) * (day_of_year + 10)))

def photoperiod(latitude, day_of_year=np.arange(1, 366)):
    return((24/np.pi) * np.arccos(-tand(latitude) * tand(declination_angle(day_of_year))))

def scale_color(value, fallen, show_fall = True):
    # Green
    color_start = (100, 150, 20)
    # Yellow
    color_middle = (220, 170, 60)
    # Red
    color_end = (160, 40, 40)
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
    
    alpha = 255

    if show_fall:
        alpha = (1 - fallen) * 255

    return r, g, b, alpha