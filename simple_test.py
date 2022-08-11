# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Modified to work with Micropython
# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
from time import sleep_ms,ticks_ms,gmtime
from machine import Pin,I2C
import adafruit_gps

i2c = I2C(0, sda=Pin(21), scl=Pin(22))

gps = adafruit_gps.GPS_GtopI2C(i2c)

# Turn on the basic GGA and RMC info
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")

last_print = ticks_ms()
while True:
    gps.update()
    
    current = ticks_ms()
    if current - last_print >= 1000:
        last_print = current
        if not gps.has_fix:
            print("Waiting for fix...")
            continue
        print("=" * 40)  # Print a separator line.
        utc = gmtime(gps.datetime)
        print(f'Timestamp: {utc[2]}/{utc[1]}/{utc[0]} {utc[3]}:{utc[4]}:{utc[5]} UTC')
        print(f'Latitude: {gps.latitude:.6f} degrees')
        print(f'Longitude: {gps.longitude:.6f} degrees')
        print(f'Precise Latitude: {gps.latitude_degrees:2.}{gps.latitude_minutes:2.4f} degrees')
        print(f'Precise Longitude: {gps.longitude_degrees:2.}{gps.longitude_minutes:2.4f} degrees')
        print("Fix quality: {}".format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and datetime are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print(f'# satellites: {gps.satellites}')
        if gps.altitude_m is not None:
            print(f'Altitude: {gps.altitude_m} meters')
        if gps.speed_knots is not None:
            print(f'Speed: {gps.speed_knots} knots')
        if gps.track_angle_deg is not None:
            print(f'Track angle: {gps.track_angle_deg} degrees')
        if gps.horizontal_dilution is not None:
            rating = 'Excellent' if gps.horizontal_dilution < 2.0 else 'Bad'
            print(f'Horizontal dilution: {gps.horizontal_dilution} {rating}')
        if gps.height_geoid is not None:
            print(f'Height geoid: {gps.height_geoid} meters')