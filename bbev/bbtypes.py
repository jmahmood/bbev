from typing import TypedDict


class BasicStats(TypedDict):
    mean: float
    median: int
    stdev: float
    samples: int


class WeightData(TypedDict):
    TOP_LEFT: int
    TOP_RIGHT: int
    BOTTOM_LEFT: int
    BOTTOM_RIGHT: int


class DefaultResponse(TypedDict):
    max: int
    grouped_median: float
    samples: int


def total(input_data: WeightData) -> int:
    return input_data['TOP_LEFT'] + input_data['TOP_RIGHT'] + input_data['BOTTOM_LEFT'] + input_data['BOTTOM_RIGHT']
