import statistics
from logging import Logger
from typing import List, Optional

import evdev

from .bbgenerator import balanceboard_generator, CANCEL
from .bbtypes import DefaultResponse


def calculate_weight(
            device: evdev.InputDevice, threshold: int = 0, interval: int = 10, logger: Optional[Logger] = None
        ) -> DefaultResponse:
    """
    Quick and dirty method to get weight data from your Wii Balanceboard.
i
    :param device:
    :param threshold:
    :param interval:
    :param logger:
    :return:
    """
    max_weight = 0
    event_data: List[int] = []

    for weight in balanceboard_generator(device, threshold, logger):
        if weight == CANCEL:
            print("Cancelling")
            return {
                'max': 0,
                'grouped_median': 0,
                'samples': 0
            }
        elif weight is not None:
            if weight > threshold:
                event_data.append(weight)
            if weight > max_weight:
                max_weight = weight

    if len(event_data) == 0:
        return {
            'max': 0,
            'grouped_median': 0,
            'samples': 0
        }
    return {
        'max': max_weight,
        'grouped_median': statistics.median_grouped(event_data, interval),
        'samples': len(event_data)
    }