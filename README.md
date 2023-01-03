# bbev
The Wii Balanceboard is extremely easy to access with Linux's evdev driver system!

# How to Use
There isn't much here right now.  Edit "BALANCE_BOARD_DEVICE_LOCATION" and run `python main.py` to start the process.  It will calculate your weight when you get on, and output something like this:

```python3
{'grouped_median': 1264.0, 'max': 1791}
{'grouped_median': 811.0, 'max': 1791}
{'grouped_median': 9545.0, 'max': 11798}
```

# Why?
A lot of the current Wii Balanceboard data implementations rely on Python2, pybluez and connecting directly to the Bluetooth signal from your Wii Balanceboard.  This involved flipping your board upside down and triggering the bluetooth connection.

However, the balanceboard's driver is now part of the Linux kernel; you can connect to it permanently, and as such, we can extract the data directly from /dev/input

## Notes
### Data
The weights being returned appear to be in kilograms.  

### Precision / Accuracy
From what I can see, the data is not precise, but the grouped median was accurate when the weight is greater than 20 kg, for weights as little as 0.1 kg.

## Helpful Sources

[Balance Board tech specs / The Wiibrew Wiki](http://wiibrew.org/wiki/Wii_Balance_Board)
[Wiimote tech specs / The Wiibrew Wiki](http://wiibrew.org/wiki/Wiimote)
[pyevdev Documentation](https://python-evdev.readthedocs.io/en/latest/index.html)

:wave: Salaam
