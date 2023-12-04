"""
Helper functions for photoperiod calculation and color scaling
"""
import numpy as np

def sind(angle_deg):
    """
    Calculate sine of angle provided in degrees

    Args:
        angle_deg (float): angle in degrees

    Returns:
        float sine value between -1 and 1
    """
    return(np.sin(np.radians(angle_deg)))

def cosd(angle_deg):
    """
    Calculate cosine of angle provided in degrees

    Args:
        angle_deg (float): angle in degrees

    Returns:
        float cosine value between -1 and 1
    """
    return(np.cos(np.radians(angle_deg)))

def tand(angle_deg):
    """
    Calculate tan of angle provided in degrees

    Args:
        angle_deg (float): angle in degrees

    Returns:
        float tan value between -1 and 1
    """
    return(np.tan(np.radians(angle_deg)))

def arcsind(val):
    """
    Calculate arcsin and return in degrees

    Args:
        val (float): between -1 and 1

    Returns:
        float angle in degrees
    """
    return(np.arcsin(val) * (180 / np.pi))

def declination_angle(day_of_year):
    """
    Calculate the solar declination angle (in degrees) for a given day of the year

    Args:
        day_of_year (int): between 1 and 365 to calculate declination angle for

    Returns:
        Float angle in degrees
    """
    return arcsind(sind(-23.44) * cosd((360/365) * (day_of_year + 10)))

def photoperiod(latitude, day_of_year=np.arange(1, 366)):
    """
    Calculate the photoperiod at a specified latitude

    Photoperiod is the number of hours of daylight

    Args:
        latitude (int): angle in degrees between -90 and 90
        day_of_year (numpy array): by default containing a numpy array of integers from 1 to 365

    Returns:
        A numpy array containing the daily photoperiod for the provided days of the year
    """
    return((24/np.pi) * np.arccos(-tand(latitude) * tand(declination_angle(day_of_year))))

def scale_color(value, fallen, show_fall = True):
    """
    Map a value onto a color scale, and calculate alpha

    Args:
        value (float): between 0 and 1 that indicates percnt of colored of leaves
        fallen (float): between 0 and 1 that indicates percent of fallen leaves
        show_fall (bool): optional keyword argument to consider leaf falling or not

    Returns:
        A tuple with the RGBA value indicating the color of a tree
    """
    # Green
    color_start = (100, 150, 20)
    # Yellow
    color_middle = (220, 170, 60)
    # Red
    color_end = (160, 40, 40)

    # Scale the value for the first half (0 to 0.5)
    if value <= 0.5:
        t_1 = value * 2
        red = int((1 - t_1) * color_start[0] + t_1 * color_middle[0])
        green = int((1 - t_1) * color_start[1] + t_1 * color_middle[1])
        blue = int((1 - t_1) * color_start[2] + t_1 * color_middle[2])

    # Scale the value for the second half (0.5 to 1)
    elif value <= 1:
        t_2 = (value - 0.5) * 2
        red = int((1 - t_2) * color_middle[0] + t_2 * color_end[0])
        green = int((1 - t_2) * color_middle[1] + t_2 * color_end[1])
        blue = int((1 - t_2) * color_middle[2] + t_2 * color_end[2])

    else:
        raise ValueError("Color scaled down outside of range")

    # Default alpha value
    alpha = 255

    # Reassign alpha value if leaf fall is shown
    if show_fall:
        alpha = (1 - fallen) * 255

    return red, green, blue, alpha
