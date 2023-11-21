import numpy as np
import matplotlib.pyplot as plt
import temperature

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

p_start = 12.5
temperature_b = 25
s_array = np.zeros([365, 1])
x = 2
y = 2
temperature_df = temperature.get_data()
days_of_year = np.arange(1, 366)
p_array = photoperiod(42.28, days_of_year)

def get_temperature(year, day_of_year):
    try:
        temperature = temperature_df[(temperature_df["year"] == year) & (temperature_df["doy"] == day_of_year)]["temperature"].values[0]
        return temperature
    except IndexError:
        print("Error: Year and/or day of year not available in queried data")
        return None

def photoperiod_func(day_of_year, version = 1):
    if version == 1:
        return(p_array[day_of_year - 1] / p_start)
    
    if version == 2:
        return(1 - (p_array[day_of_year - 1] / p_start))
    
    print("ERROR: Invalid Value")
    return -1

def rate_senescence(year, day_of_year):
    t_today = get_temperature(year, day_of_year)
    if  t_today >= temperature_b:
        return 0
    
    return (((temperature_b - t_today) ** x) * (photoperiod_func(day_of_year) ** y))

def update_senescence(year, day_of_year):
    if p_array[day_of_year - 1] >= p_start:
        s_array[day_of_year - 1] = 0

    else:
        s_array[day_of_year - 1] = s_array[day_of_year - 2] + rate_senescence(year, day_of_year)

year = 2022
printed_y90 = False
y_crit = 5160
for doy in range(170, 366):
    update_senescence(year, doy)
    # print("Updated senescence")
    if s_array[doy - 1] > y_crit and not printed_y90:
        print(doy)
        printed_y90 = True

plt.plot(s_array)
plt.show()