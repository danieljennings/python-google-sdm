from .decorators import SDMTraitGetter
from .device import (
    DeviceConnectivityTrait,
    DeviceFanTrait,
    DeviceInfoTrait,
    DeviceHumidityTrait,
    DeviceSettingsTrait,
    DeviceTemperatureTrait,
)
from .trait import Trait
from .thermostat import (
    ThermostatEcoTrait,
    ThermostatHvacTrait,
    ThermostatModeTrait,
    ThermostatTemperatureSetpointTrait,
)

from .camera import (
    CameraEventImageTrait,
    CameraImageTrait,
    CameraLiveStreamTrait,
    CameraMotionTrait,
    CameraPersonTrait,
    CameraSoundTrait,
)