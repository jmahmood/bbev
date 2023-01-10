# bbev
The Wii Balanceboard is extremely easy to access with Linux's evdev driver system!

# How to Use
Run `python ./bbev/bbev.py` to start the process.  It will calculate your weight when you get on, and output something like this:

```
{'grouped_median': 1264.0, 'max': 1791, 'samples': 1000}
```

Alternatively, you can import this into your script.

```python3
from bbev import calculate_weight
import evdev
import configparser

config = configparser.ConfigParser()
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
device_path = (device.path for device in devices if device.name == 'Nintendo Wii Remote Balance Board').__next__()
balance_board: evdev.InputDevice = evdev.InputDevice(device_path)

data = calculate_weight(
        balance_board,
        int(config['DEFAULT']['threshold']),
        int(config['DEFAULT']['interval']),
)
print(data)
# ...
```

You may also want to do more statistical analysis.
```python3
import evdev
from bbev import calculate_weight_with_statistics

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
device_path = (device.path for device in devices if device.name == 'Nintendo Wii Remote Balance Board').__next__()
balance_board: evdev.InputDevice = evdev.InputDevice(
    device_path,
)
weight_data = calculate_weight_with_statistics(
    balance_board,
    100,
)

stats = weight_data.statistics()
trimmed_stats = weight_data.trimmed_statistics(30)

print(f"""
Stats:
    Median: {stats['median']}
    Mean: {stats['mean']}
    Stdev: {stats['stdev']}
""")

print(f"""
Trimmed Stats: (To get rid of outliers, like getting onto the board
    Median: {trimmed_stats['median']}
    Mean: {trimmed_stats['mean']}
    Stdev: {trimmed_stats['stdev']}
""")
```

Finally, you can also reuse the generator as well, if you want to get into the weeds.

```python3
import evdev
from bbev import balanceboard_generator

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
device_path = (device.path for device in devices if device.name == 'Nintendo Wii Remote Balance Board').__next__()
balance_board: evdev.InputDevice = evdev.InputDevice(
    device_path,
)
threshold = 10
logger = ...

for weight in balanceboard_generator(balance_board, threshold, logger):
    # do whatever you want
    pass
```

# Why?
A lot of the current Wii Balanceboard data implementations rely on Python2, pybluez and connecting directly to the Bluetooth signal from your Wii Balanceboard.  This involved flipping your board upside down and triggering the bluetooth connection.

However, the balanceboard's driver is now part of the Linux kernel; you can connect to it permanently, and as such, we can extract the data directly from /dev/input

## Notes
### Data
The weights being returned appear to be in kilograms.  

### Precision / Accuracy
From what I can see, the data is not accurate, but the grouped median was precise when the weight is greater than 20 kg, for weight changes as little as 0.1 kg.

## Helpful Sources

- [Balance Board tech specs / The Wiibrew Wiki](http://wiibrew.org/wiki/Wii_Balance_Board)
- [Wiimote tech specs / The Wiibrew Wiki](http://wiibrew.org/wiki/Wiimote)
- [pyevdev Documentation](https://python-evdev.readthedocs.io/en/latest/index.html)

:wave: Salaam
