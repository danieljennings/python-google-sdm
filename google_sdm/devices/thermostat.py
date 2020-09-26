from .generic import SDMDevice
from ..traits import (
    SDMTraitGetter,
    DeviceConnectivityTrait,
    DeviceFanTrait,
    DeviceHumidityTrait,
    DeviceSettingsTrait,
    DeviceTemperatureTrait,
    ThermostatEcoTrait,
    ThermostatHvacTrait,
    ThermostatModeTrait,
    ThermostatTemperatureSetpointTrait,
)


class SDMThermostat(SDMDevice):
    STR_REPR = "sdm.devices.types.THERMOSTAT"

    def __repr__(self):
        return self.STR_REPR

    @SDMTraitGetter(DeviceConnectivityTrait)
    def get_connectivity(self, **kwargs) -> DeviceConnectivityTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(DeviceFanTrait)
    def get_fan(self, **kwargs) -> DeviceFanTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(DeviceHumidityTrait)
    def get_humidity(self, **kwargs) -> DeviceHumidityTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(DeviceSettingsTrait)
    def get_settings(self, **kwargs) -> DeviceSettingsTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(DeviceTemperatureTrait)
    def get_temperature(self, **kwargs) -> DeviceTemperatureTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(ThermostatEcoTrait)
    def get_thermostat_eco(self, **kwargs) -> ThermostatEcoTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(ThermostatHvacTrait)
    def get_thermostat_hvac(self, **kwargs) -> ThermostatHvacTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(ThermostatModeTrait)
    def get_thermostat_mode(self, **kwargs) -> ThermostatModeTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(ThermostatTemperatureSetpointTrait)
    def get_thermostat_temperature_setpoint(self, **kwargs) \
            -> ThermostatTemperatureSetpointTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]
