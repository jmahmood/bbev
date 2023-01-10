import statistics
from logging import Logger

import evdev
from typing import List, Optional

from bbtypes import BasicStats
from bbgenerator import balanceboard_generator, CANCEL


class StatisticsResponse:
    _sorted_samples: List[int]
    _normal_distribution: statistics.NormalDist

    def __init__(self, samples: List[int]):
        self._sorted_samples = sorted(samples)
        self._normal_distribution = statistics.NormalDist.from_samples(samples)

    def max(self):
        return self._sorted_samples[-1]

    def min(self):
        return self._sorted_samples[0]

    def statistics(self) -> BasicStats:
        return {
            "mean": statistics.mean(self._sorted_samples),
            "median": statistics.median(self._sorted_samples),
            "stdev": statistics.stdev(self._sorted_samples),
            "samples": len(self._sorted_samples)
        }

    def normal_distribution(self):
        return self._normal_distribution

    def trimmed_normal_distribution(self, removal_percentage: int) -> statistics.NormalDist:
        samples = self.trimmed_samples(removal_percentage)
        return statistics.NormalDist.from_samples(samples)

    def trimmed_statistics(self, removal_percentage: int) -> BasicStats:
        trimmed_samples = self.trimmed_samples(removal_percentage)
        return {
            "mean": statistics.mean(trimmed_samples),
            "median": statistics.median(trimmed_samples),
            "stdev": statistics.stdev(trimmed_samples),
            "samples": len(trimmed_samples)
        }

    def trimmed_samples(self, removal_percentage):
        to_remove = int(((removal_percentage/100) * len(self._sorted_samples))/2)
        return self._sorted_samples[to_remove: -1 * to_remove]

    def samples(self):
        return self._sorted_samples

    def count(self):
        return len(self._sorted_samples)


def calculate_weight_with_statistics(
        device: evdev.InputDevice, threshold: int = 0, logger: Optional[Logger] = None) -> Optional[StatisticsResponse]:
    samples = []
    for weight in balanceboard_generator(device, threshold, logger):
        if weight == CANCEL:
            return None
        elif weight is not None and weight > threshold:
            samples.append(weight)

    return StatisticsResponse(samples)
