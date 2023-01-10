from logging import Logger
from typing import Optional

import evdev

from bbconstants import TOP_LEFT_CODE, TOP_RIGHT_CODE, BOTTOM_LEFT_CODE, BOTTOM_RIGHT_CODE
from bbtypes import WeightData, total

CANCEL = -1


def balanceboard_generator(device: evdev.InputDevice, threshold=0, logger: Optional[Logger] = None):
    data: WeightData = {'TOP_LEFT': 0, 'TOP_RIGHT': 0, 'BOTTOM_LEFT': 0, 'BOTTOM_RIGHT': 0}
    step_on = False
    if logger is not None:
        logger.debug("Starting generator")

    while True:
        event = device.read_one()
        if event is None:
            pass
        else:
            if event.code == TOP_LEFT_CODE:
                data['TOP_LEFT'] = 0 if event.value < threshold else event.value
            elif event.code == TOP_RIGHT_CODE:
                data['TOP_RIGHT'] = 0 if event.value < threshold else event.value
            elif event.code == BOTTOM_LEFT_CODE:
                data['BOTTOM_LEFT'] = 0 if event.value < threshold else event.value
            elif event.code == BOTTOM_RIGHT_CODE:
                data['BOTTOM_RIGHT'] = 0 if event.value < threshold else event.value
            elif event.code == evdev.ecodes.BTN_A:
                # This only happens when you are hitting the power button in the front
                device.close()
                yield CANCEL
                return None
            elif event.code == evdev.ecodes.SYN_DROPPED:
                pass
            elif event.code == evdev.ecodes.SYN_REPORT and event.value == 3:
                pass
            elif event.code == evdev.ecodes.SYN_REPORT and event.value == 0:
                # We've gotten the full stream and can now calculate the outcome.
                weight_total = total(data)
                if weight_total > 0 and step_on is False:
                    if logger is not None:
                        logger.debug("Stepped on")
                    step_on = True

                if weight_total <= threshold and step_on:
                    # Someone stepped off the balance board & we measured something.
                    if logger is not None:
                        logger.debug("Stepped off")
                    device.close()
                    return None
                else:
                    yield weight_total
            else:
                device.close()
                logger.exception(f'Unexpected event {evdev.categorize(event)}')
                raise IOError(f'Unexpected event {evdev.categorize(event)}')
