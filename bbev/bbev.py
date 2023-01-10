import logging

import evdev

from bbdefault import calculate_weight

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()  # or RotatingFileHandler
    handler.setFormatter(logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    device_path = (device.path for device in devices if device.name == 'Nintendo Wii Remote Balance Board').__next__()
    balance_board: evdev.InputDevice = evdev.InputDevice(
        device_path,
    )
    print(calculate_weight(
        balance_board,
        100,
        10,
        logger
    ))
    # trimmed_stats = responseData.trimmed_statistics(30)
    # trimmed_samples = responseData.trimmed_samples(30)
    # stats = responseData.statistics()
    #
    # print(trimmed_samples)
    #
    # print(f"""
    # Trimmed Stats:
    #     Mean: {trimmed_stats.mean}
    #     Median: {trimmed_stats.median}
    #     STDEV: {trimmed_stats.stdev}
    #     Median_grouped: {statistics.median_grouped(trimmed_samples)}
    #     Median: {statistics.median(trimmed_samples)}
    #     Stdev: {statistics.stdev(trimmed_samples)}
    #     Mean: {statistics.mean(trimmed_samples)}
    #
    # Untrimmed Stats:
    #     Mean: {stats.mean}
    #     Median: {stats.median}
    #     STDEV: {stats.stdev}
    # """)
