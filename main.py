import statistics
from pprint import pprint
import configparser
from typing import TypedDict, List

import evdev

TOP_RIGHT_CODE = evdev.ecodes.ABS_HAT0X
TOP_LEFT_CODE = evdev.ecodes.ABS_HAT1X
BOTTOM_LEFT_CODE = evdev.ecodes.ABS_HAT0Y
BOTTOM_RIGHT_CODE = evdev.ecodes.ABS_HAT1Y

SAMPLES_TO_USE = 10
THRESHOLD = 0


class WeightData(TypedDict):
    TOP_LEFT: int
    TOP_RIGHT: int
    BOTTOM_LEFT: int
    BOTTOM_RIGHT: int


class Response(TypedDict):
    max: int
    grouped_median: float


def total(input_data: WeightData) -> int:
    return input_data['TOP_LEFT'] + input_data['TOP_RIGHT'] + input_data['BOTTOM_LEFT'] + input_data['BOTTOM_RIGHT']


def calculate_weight(device: evdev.InputDevice) -> Response:
    data: WeightData = {'TOP_LEFT': 0, 'TOP_RIGHT': 0, 'BOTTOM_LEFT': 0, 'BOTTOM_RIGHT': 0}
    max_weight = 0
    event_data: List[int] = []

    for event in device.read_loop():
        if event.code == TOP_RIGHT_CODE:
            data['TOP_RIGHT'] = event.value
        elif event.code == TOP_LEFT_CODE:
            data['TOP_LEFT'] = event.value
        elif event.code == BOTTOM_LEFT_CODE:
            data['BOTTOM_LEFT'] = event.value
        elif event.code == BOTTOM_RIGHT_CODE:
            data['BOTTOM_RIGHT'] = event.value
        elif event.code == evdev.ecodes.BTN_A:
            # This only happens when you are hitting the power button in the front
            pass
        elif event.code == evdev.ecodes.SYN_REPORT and event.value == 3:
            pass
        elif event.code == evdev.ecodes.SYN_REPORT and event.value == 0:
            # We've gotten the full stream and can now calculate the outcome.
            running_total = total(data)
            event_data.append(running_total)
            if running_total > max_weight:
                max_weight = running_total

            if running_total <= THRESHOLD:  # Someone stepped off the balance board.
                return {
                    'max': max_weight,
                    'grouped_median': statistics.median_grouped(event_data, SAMPLES_TO_USE)
                }
        else:
            raise IOError(f'Unexpected event {evdev.categorize(event)}')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    balance_board: evdev.InputDevice = evdev.InputDevice(config['DEFAULT']['BalanceBoardDeviceLocation'])
    pprint(calculate_weight(balance_board))
