import pandas as pd


class TwoDLayout():
    def __init__(self):
        self.current_devices = pd.DataFrame(columns=['mac_address', 'x_pos', 'y_pos', 'floor'])

    def location_update(self, mac_address, x_pos, y_pos, floor):
        # TODO
        print(f"Location Update {[mac_address, x_pos, y_pos, floor]}")

    def device_exit(self, mac_address):
        # TODO
        print(f"Device Exit {[mac_address]}")

    def device_entry(self, mac_address):
        # TODO
        print(f"Device Entry {[mac_address]}")
