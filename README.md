# bbev
The Wii Balanceboard is extremely easy to access with Linux's evdev driver system!

# How to Use
Edit the config.ini file and add the correct location for "BALANCE_BOARD_DEVICE_LOCATION".

After that, run `python ./bbev/bbev.py` to start the process.  It will calculate your weight when you get on, and output something like this:

```
{'grouped_median': 1264.0, 'max': 1791, 'samples': 1000}
```

Alternatively, you can import this into your script.

```python3
import bbev
import configparser
import evdev

config = configparser.ConfigParser()
balance_board: evdev.InputDevice = evdev.InputDevice(
    config['DEFAULT']['BalanceBoardDeviceLocation'],
)

data = bbev.calculate_weight(
        balance_board,
        0,
        10,
)
# ...
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
