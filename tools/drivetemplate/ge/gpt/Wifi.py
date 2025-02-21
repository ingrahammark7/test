import time
import os
import subprocess

WIFI_SSID = "City Wifi"
CHECK_INTERVAL = 30  # Seconds


def is_connected():
    try:
        output = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def connect_to_wifi():
    print("Attempting to connect to WiFi...")
    os.system("termux-wifi-enable true")  # Enable WiFi
    time.sleep(5)
    os.system(f"termux-wifi-connect '{WIFI_SSID}'")  # Attempt to connect
    time.sleep(10)


def main():
    while True:
        if not is_connected():
            print("WiFi not connected. Reconnecting...")
            connect_to_wifi()
        else:
            print("WiFi is connected.")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
