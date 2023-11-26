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

def photoperiod(latitude, day_of_year):
    return((24/np.pi) * np.arccos(-tand(latitude) * tand(declination_angle(day_of_year))))