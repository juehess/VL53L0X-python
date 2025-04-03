import pytest
from unittest.mock import MagicMock, patch
from VL53L0X import (
    VL53L0X, 
    Vl53l0xAccuracyMode, 
    Vl53l0xDeviceMode,
    Vl53l0xGpioAlarmType,
    Vl53l0xInterruptPolarity,
    Vl53l0xError
)

@pytest.fixture
def mock_smbus():
    with patch('VL53L0X.smbus.SMBus') as mock:
        yield mock

@pytest.fixture
def mock_tof_library():
    with patch('VL53L0X._TOF_LIBRARY') as mock:
        yield mock

@pytest.fixture
def sensor(mock_smbus, mock_tof_library):
    return VL53L0X(i2c_bus=1, i2c_address=0x29)

def test_init(sensor):
    """Test sensor initialization."""
    assert sensor._i2c_bus == 1
    assert sensor.i2c_address == 0x29
    assert sensor._tca9548a_num == 255
    assert sensor._tca9548a_addr == 0

def test_open(sensor, mock_tof_library):
    """Test opening the sensor."""
    sensor.open()
    assert sensor._dev is not None
    mock_tof_library.initialise.assert_called_once_with(0x29, 255, 0)

def test_close(sensor):
    """Test closing the sensor."""
    sensor.open()
    sensor.close()
    assert sensor._dev is None

def test_start_ranging(sensor, mock_tof_library):
    """Test starting ranging in different modes."""
    sensor.open()
    
    # Test different accuracy modes
    modes = [
        Vl53l0xAccuracyMode.GOOD,
        Vl53l0xAccuracyMode.BETTER,
        Vl53l0xAccuracyMode.BEST,
        Vl53l0xAccuracyMode.LONG_RANGE,
        Vl53l0xAccuracyMode.HIGH_SPEED
    ]
    
    for mode in modes:
        sensor.start_ranging(mode)
        mock_tof_library.startRanging.assert_called_with(sensor._dev, mode)

def test_get_distance(sensor, mock_tof_library):
    """Test getting distance measurements."""
    sensor.open()
    mock_tof_library.getDistance.return_value = 100
    
    distance = sensor.get_distance()
    assert distance == 100
    mock_tof_library.getDistance.assert_called_once_with(sensor._dev)

def test_configure_gpio_interrupt(sensor, mock_tof_library):
    """Test GPIO interrupt configuration."""
    sensor.open()
    mock_tof_library.VL53L0X_SetGpioConfig.return_value = 0
    mock_tof_library.VL53L0X_SetInterruptThresholds.return_value = 0
    
    sensor.configure_gpio_interrupt(
        proximity_alarm_type=Vl53l0xGpioAlarmType.THRESHOLD_CROSSED_LOW,
        interrupt_polarity=Vl53l0xInterruptPolarity.HIGH,
        threshold_low_mm=250,
        threshold_high_mm=500
    )
    
    assert mock_tof_library.VL53L0X_SetGpioConfig.called
    assert mock_tof_library.VL53L0X_SetInterruptThresholds.called

def test_configure_gpio_interrupt_error(sensor, mock_tof_library):
    """Test GPIO interrupt configuration error handling."""
    sensor.open()
    mock_tof_library.VL53L0X_SetGpioConfig.return_value = 1
    
    with pytest.raises(Vl53l0xError):
        sensor.configure_gpio_interrupt()

def test_get_timing(sensor, mock_tof_library):
    """Test getting timing budget."""
    sensor.open()
    mock_tof_library.VL53L0X_GetMeasurementTimingBudgetMicroSeconds.return_value = 0
    
    timing = sensor.get_timing()
    assert timing > 0
    assert mock_tof_library.VL53L0X_GetMeasurementTimingBudgetMicroSeconds.called

def test_change_address(sensor, mock_tof_library):
    """Test changing I2C address."""
    sensor.open()
    new_address = 0x30
    sensor.change_address(new_address)
    assert sensor.i2c_address == new_address
