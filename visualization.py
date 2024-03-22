import threading
import time
import random

import requests
import json
import os

from utils.api import get_api_key_and_auth


def stream_devices(log_file, stream, device_positions, device_lock):
    colors = 'rgbyc'
    for line in stream.iter_lines():
        if line:
            # decodes payload into usable format
            decoded_line = line.decode('utf-8')
            event = json.loads(decoded_line)

            # writes every event to the logs.json in readable format
            log_file.write(str(json.dumps(json.loads(line), indent=4, sort_keys=True)))

            print(event['eventType'])

            if event['eventType'] == 'DEVICE_LOCATION_UPDATE':
                device_lock.acquire()
                device_id = event['deviceLocationUpdate']['device']['deviceId']
                xPos = event["deviceLocationUpdate"]["xPos"]
                yPos = event["deviceLocationUpdate"]["yPos"]
                color = random.choice(colors) if device_id not in device_positions.keys() else \
                    device_positions[device_id][2]
                device_positions[device_id] = (xPos, yPos, color)
                print(f'Device {device_id}, xPos {xPos}, yPos {yPos}')
                device_lock.release()


def update_plot(device_positions, device_lock):
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    # Setup plot
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    while True:
        ax.clear()
        ax.set_xlim(0, 1000)
        ax.set_ylim(0, 1000)
        device_lock.acquire()
        for _, position in device_positions.items():
            ax.plot(position[0], position[1], f'{position[2]}o')
        device_lock.release()
        plt.pause(0.1)
        plt.show()


def get_api_key():
    # Tests to see if we already have an API Key
    try:
        if os.stat("API_KEY.txt").st_size > 0:
            # If we do, lets use it
            f = open("API_KEY.txt")
            return f.read()
        else:
            # If not, lets get user to create one
            return get_api_key_and_auth()
    except:
        return get_api_key_and_auth()


def main():
    # url = get_api_url()
    api_key = get_api_key()

    # overwrite previous log file
    log_file = open("logs.json", 'r+')
    log_file.truncate(0)

    # Opens a new HTTP session that we can use to terminate firehose onto
    s = requests.Session()
    s.headers = {'X-API-Key': api_key}
    stream = s.get(
        'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)  # Change this to .io if needed

    device_positions = {}
    device_lock = threading.Lock()

    # Thread for simulating incoming data
    print("Starting stream thread")
    data_thread = threading.Thread(target=stream_devices, args=(log_file, stream, device_positions, device_lock))
    data_thread.daemon = True
    data_thread.start()

    # Thread for updating the plot
    print("Starting plot thread")
    plot_thread = threading.Thread(target=update_plot, args=(device_positions, device_lock))
    plot_thread.daemon = True
    plot_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(10)


if __name__ == '__main__':
    main()
