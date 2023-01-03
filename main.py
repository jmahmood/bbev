import statistics
from pprint import pprint

import evdev

TOP_LEFT = 'x1'
TOP_RIGHT = 'x0'
BOTTOM_LEFT = 'y1'
BOTTOM_RIGHT = 'y0'
SAMPLES_TO_USE = 10
BALANCE_BOARD_DEVICE_LOCATION = '/dev/input/event27'


def total(input_data):
    return input_data[TOP_LEFT] + input_data[TOP_RIGHT] + input_data[BOTTOM_LEFT] + input_data[BOTTOM_RIGHT]


def calculateWeight(device: evdev.InputDevice):
    data = {
        "x1": 0,
        "x0": 0,
        "y1": 0,
        "y0": 0,
    }
    max_weight = 0
    event_data = []

    for event in device.read_loop():
        if event.code == evdev.ecodes.ABS_HAT0X:
            data[TOP_RIGHT] = event.value
        elif event.code == evdev.ecodes.ABS_HAT1X:
            data[TOP_LEFT] = event.value
        elif event.code == evdev.ecodes.ABS_HAT0Y:
            data[BOTTOM_RIGHT] = event.value
        elif event.code == evdev.ecodes.ABS_HAT1Y:
            data[BOTTOM_LEFT] = event.value
        elif event.code == evdev.ecodes.SYN_REPORT and event.value == 3:
            # disregard.
            pass
        elif event.code == evdev.ecodes.SYN_REPORT and event.value == 0:
            # We've gotten the full stream and can now calculate the outcome.
            running_total = total(data)
            event_data.append(running_total)
            if running_total > max_weight:
                max_weight = running_total

            if running_total == 0:  # Someone stepped off the balance board.
                pprint({
                    'max': max_weight,
                    'grouped_median': statistics.median_grouped(event_data, SAMPLES_TO_USE)
                })
                event_data = []
        else:
            raise IOError(f'Unexpected event {str(event)}')


if __name__ == '__main__':
    balance_board: evdev.InputDevice = evdev.InputDevice(BALANCE_BOARD_DEVICE_LOCATION)
    calculateWeight(balance_board)
