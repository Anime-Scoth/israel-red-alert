import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL to the remote JSON file
URL = 'https://www.mako.co.il/Collab/amudanan/alerts.json'

# List of regions
TRIGGER_PHRASES = ["region1", "region2"]

# Store previous data to detect changes
previous_data = []

def main():
    global previous_data

    response = requests.get(URL, verify=False)
    if response.status_code == 200:
        content = response.json()
        
        # Remove duplicates while preserving order
        current_data = list(dict.fromkeys(content.get('data', [])))

        # Check for trigger phrases
        if any(any(phrase in item.lower() for phrase in TRIGGER_PHRASES) for item in current_data):
            print("warning")
            return

        differences = [item for item in current_data if item not in previous_data]

        if differences and current_data:
            print('\n'.join(differences))
            previous_data = current_data.copy()

    else:
        print(f"Error: Received status code {response.status_code}")


if __name__ == '__main__':
    while True:
        try:
            main()
            time.sleep(1)
        except Exception as e:
            print(f"Error occurred: {e}. Restarting in 5 seconds...")
            time.sleep(5)
