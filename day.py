import network
import ntptime
import utime
import machine
import random
from machine import Pin
import neopixel
import urequests

SCRIPT_URL = "https://raw.githubusercontent.com/alvera-syed/ABday/refs/heads/main/main.py?token=GHSAT0AAAAAACYZ5MYCMYV4RIEIAYMMJ7RYZYRD4RQ"
# Wi-Fi credential
WIFI_SSID = "FPS-Guest"
WIFI_PASSWORD = ""

# NTP server for time synchronization
NTP_SERVER = "pool.ntp.org"

# NeoPixel configuration
PIXEL_PIN = 13  # GPIO pin connected to the NeoPixel data line
NUM_PIXELS = 64  # 8x8 grid = 64 pixels

# A and B day lists
aDays = [
    "09-03-2024", "09-04-2024", "09-06-2024", "09-10-2024", "09-12-2024", 
    "09-16-2024", "09-18-2024", "09-20-2024", "09-24-2024", "09-26-2024", 
    "10-01-2024", "10-11-2024", "10-03-2024", "10-07-2024", "10-09-2024",
    "10-17-2024", "10-21-2024", "10-23-2024", "10-28-2024", "10-15-2024",
    "10-30-2024", "11-01-2024", "11-05-2024", "11-07-2024", "11-11-2024", 
    "11-13-2024", "11-15-2024", "11-19-2024", "11-21-2024", "11-25-2024", 
    "12-03-2024", "12-05-2024", "12-09-2024", "12-11-2024", "12-13-2024", 
    "12-17-2024", "12-19-2024", "01-02-2025", "01-06-2025", "01-08-2025", 
    "01-10-2025", "01-14-2025", "01-16-2025", "01-22-2025", "01-24-2025", 
    "01-28-2025", "01-30-2025", "02-03-2025", "02-05-2025", "02-07-2025", 
    "02-11-2025", "02-13-2025", "02-17-2025", "02-19-2025", "02-21-2025", 
    "02-25-2025", "02-27-2025", "03-04-2025", "03-06-2025", "03-10-2025", 
    "03-12-2025", "03-14-2025", "03-18-2025", "03-20-2025", "03-31-2025", 
    "04-02-2025", "04-04-2025", "04-08-2025", "04-10-2025", "04-14-2025", 
    "04-16-2025", "04-22-2025", "04-24-2025", "04-28-2025", "04-30-2025", 
    "05-02-2025", "05-06-2025", "05-08-2025", "05-12-2025", "05-14-2025", 
    "05-16-2025", "05-20-2025", "05-22-2025", "05-27-2025", "05-29-2025", 
    "06-02-2025", "06-04-2025", "06-06-2025"
]

bDays = [
    "09-05-2024", "09-09-2024", "09-11-2024", "09-13-2024", "09-17-2024", 
    "09-19-2024", "09-23-2024", "09-25-2024", "09-27-2024", "10-02-2024", 
    "10-04-2024", "10-08-2024", "10-10-2024", "10-14-2024", "10-16-2024", 
    "10-18-2024", "10-22-2024", "10-24-2024", "10-29-2024", "10-31-2024", 
    "11-04-2024", "11-06-2024", "11-08-2024", "11-12-2024", "11-14-2024", 
    "11-18-2024", "11-20-2024", "11-22-2024", "11-26-2024", "12-02-2024", 
    "12-04-2024", "12-06-2024", "12-10-2024", "12-12-2024", "12-16-2024", 
    "12-18-2024", "12-20-2024", "01-03-2025", "01-07-2025", "01-09-2025", 
    "01-13-2025", "01-15-2025", "01-17-2025", "01-23-2025", "01-27-2025", 
    "01-29-2025", "01-31-2025", "02-04-2025", "02-06-2025", "02-10-2025", 
    "02-12-2025", "02-14-2025", "02-18-2025", "02-20-2025", "02-24-2025", 
    "02-26-2025", "03-03-2025", "03-05-2025", "03-07-2025", "03-11-2025", 
    "03-13-2025", "03-17-2025", "03-19-2025", "03-21-2025", "04-01-2025", 
    "04-03-2025", "04-07-2025", "04-09-2025", "04-11-2025", "04-15-2025", 
    "04-17-2025", "04-23-2025", "04-25-2025", "04-29-2025", "05-01-2025", 
    "05-05-2025", "05-07-2025", "05-09-2025", "05-13-2025", "05-15-2025", 
    "05-19-2025", "05-21-2025", "05-23-2025", "05-28-2025", "05-30-2025", 
    "06-03-2025", "06-05-2025", "06-09-2025"
]

# LED patterns for 'A' and 'B'
PATTERN_A = [
    0, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 1, 0, 0, 1, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
]

PATTERN_B = [
    0, 0, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
    0, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 0, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 0, 0,
]

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print('WiFi connected')

def sync_time():
    ntptime.host = NTP_SERVER
    ntptime.settime()
    print('Time synchronized')

def get_day_type(current_date):
    if current_date in aDays:
        return 'A'
    elif current_date in bDays:
        return 'B'
    else:
        return 'N'  # Neither A nor B day

def log_time_to_file(current_date_time):
    with open('log.txt', 'a') as f:
        f.write(current_date_time + '\n')
        
        

def gradient(np, pattern, color_start, color_end, steps=30):
    for step in range(steps):
        r = int(color_start[0] + (color_end[0] - color_start[0]) * (step / steps))
        g = int(color_start[1] + (color_end[1] - color_start[1]) * (step / steps))
        b = int(color_start[2] + (color_end[2] - color_start[2]) * (step / steps))

        for i in range(NUM_PIXELS):
            if pattern[i]:  # Only light up pixels that are part of the pattern
                np[i] = (r, g, b)
            else:
                np[i] = (0, 0, 0)  # Ensure off for non-pattern pixels
        np.write()
        utime.sleep(0.1)  # Adjust speed of gradient

def display_full_color(np, pattern, color):
    for i in range(NUM_PIXELS):
        if pattern[i]:  # Only light up pixels that are part of the pattern
            np[i] = color
        else:
            np[i] = (0, 0, 0)  # Ensure off for non-pattern pixels
    np.write()

def light_up_pattern(np, pattern, color, delay=0.2):
    for i in range(NUM_PIXELS):
        if pattern[i]:  # Only light up pixels that are part of the pattern
            np[i] = color
            np.write()
            utime.sleep(delay)  # Delay between lighting each LED


def get_cd_time():
    # Get current UTC time
    current_time = utime.localtime()
    
    # Adjust for Central Daylight Time (CDT)
    # CDT is UTC-5
    # Note: If you want to handle daylight saving time, you would need additional logic
    offset_hours = -5
    adjusted_time = (
        current_time[0],  # Year
        current_time[1],  # Month
        current_time[2],  # Day
        (current_time[3] + offset_hours) % 24,  # Hour
        current_time[4],  # Minutes
        current_time[5]   # Seconds
    )
    return adjusted_time

#wifi updating remote
def download_script(url):
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print("Failed to download script")
    except Exception as e:
        print(f"Error during download: {e}")
    return None

def execute_script(script):
    exec(script)
    

def main():
    # Connect to WiFi and sync time
    connect_wifi()
    sync_time()

    # Initialize NeoPixel strip
    np = neopixel.NeoPixel(machine.Pin(PIXEL_PIN), NUM_PIXELS)

    while True:
        #Wifi remote updating part
        new_script = download_script(SCRIPT_URL)
        if new_script:
            print("New script downloaded, executing...")
            execute_script(new_script)
        
        # Get current time and date in CDT
        current_time = get_cd_time()
        current_date = "{:02d}-{:02d}-{:04d}".format(current_time[1], current_time[2], current_time[0])
        current_time_str = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
        current_date_time = f"{current_date} {current_time_str}"

        # Log the current date and time to the file
        log_time_to_file(current_date_time)

        day_type = get_day_type(current_date)

        print(f"Current date: {current_date}, Time: {current_time_str}, Day type: {day_type}")

        if day_type == 'A':
            # Light up A pattern one by one with a gradient
            for i in range(NUM_PIXELS):
                light_up_pattern(np, PATTERN_A, (200, 0, 0))
                gradient(np, PATTERN_A, (120, 1, 0), (200, 0, 40), steps=30)
                np.write()
                utime.sleep(0.2)

            # Hold full color for a few seconds
            utime.sleep(5)

        elif day_type == 'B':
            # Light up B pattern one by one with a gradient
            for i in range(NUM_PIXELS):
                light_up_pattern(np, PATTERN_B, (0, 32, 32))
                gradient(np, PATTERN_B, (0, 0, 32), (32, 0, 32), steps=30)
                np.write()
                utime.sleep(0.2)

            # Hold full color for a few seconds
            utime.sleep(5)
        else:
            # Set a dark color instead of turning off
            dark_color = (1, 1, 1)  # Very low brightness
            np.fill(dark_color)
            np.write()
            utime.sleep(5)

       

if __name__ == "__main__":
    main()

