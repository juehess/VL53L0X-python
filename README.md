# VL53L0X Python interface

This project provides a simplified Python interface to the ST VL53L0X API (ST Microelectronics) for distance sensing. It's particularly useful for robotics applications like the inverted pendulum project.

This is a fork of [pimoroni/VL53L0X-python](https://github.com/pimoroni/VL53L0X-python), modernized with current Python packaging standards and additional features.

## Features

- Simple Python interface to VL53L0X sensor
- Support for multiple sensors on the same bus
- TCA9548A I2C Multiplexer support
- Comprehensive test suite
- Modern Python packaging

## Installation

### Using pip

```bash
pip install git+ssh://git@github.com/juehess/VL53L0X-python.git
```

### Development Setup

1. Clone the repository:
```bash
git clone git@github.com:juehess/VL53L0X-python.git
cd VL53L0X-python
```

2. Create and activate the conda environment:
```bash
mamba env create -f environment.yml
mamba activate vl53l0x
```

3. Install in development mode:
```bash
pip install -e .
```

### Building from Source

First, ensure you have the required build tools:
```bash
sudo apt-get install build-essential python-dev
```

Then compile the C library:
```bash
make
```

## Development

### Running Tests
```bash
make test
```

### Code Quality
```bash
make quality
```

### Building Documentation
```bash
make docs
```

## Usage Examples

### Basic Usage
```python
import VL53L0X

# Create a VL53L0X object
tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)

# Start ranging
tof.open()
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

# Get distance
distance = tof.get_distance()
print(f"Distance: {distance}mm")

# Stop ranging
tof.stop_ranging()
tof.close()
```

### Multiple Sensors
The library supports multiple sensors through:
1. Address changes (volatile)
2. TCA9548A I2C Multiplexer support

For detailed examples, see the `examples` directory.

## Hardware Setup

### Single Sensor
- Connect VCC to 3.3V
- Connect GND to Ground
- Connect SCL to SCL (GPIO 3)
- Connect SDA to SDA (GPIO 2)

### Multiple Sensors
When using multiple sensors, you can either:
1. Use separate GPIO pins for each sensor's XSHUT pin
2. Use a TCA9548A I2C Multiplexer

See the examples directory for detailed wiring diagrams.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests (`make test`)
5. Run quality checks (`make quality`)
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Version History

### 1.0.4
- Modernized Python packaging
- Added comprehensive test suite
- Added development tools (black, isort, flake8)
- Added documentation

[Previous versions...]

## Notes

- Address changes are volatile - setting the shutdown pin low or removing power will reset the address to the default 0x29
- When using multiple sensors directly on the I2C bus, the number of devices is limited by the combined pull-up resistors
- TCA9548A Multiplexer is recommended for multiple sensor setups

