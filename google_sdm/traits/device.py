from .trait import Trait


class DeviceInfoTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.Info"

    def __init__(self, trait_dict):
        props = {"_custom_name": "customName"}
        super().__init__(self, props, trait_dict)


class DeviceConnectivityTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.Connectivity"

    def __init__(self, trait_dict):
        props = {"_status": "status"}
        super().__init__(self, props, trait_dict)


class DeviceFanTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.Fan"

    COMMANDS = {
        "SetTimer": "sdm.devices.commands.Fan.SetTimer",
    }

    def __init__(self, trait_dict):
        props = {
            "_timer_mode": "timerMode",
            "_timer_timeout": "timerTimeout",
        }
        super().__init__(self, props, trait_dict)

    TIMER_MODE_ON = "ON"
    TIMER_MODE_OFF = "OFF"

    @staticmethod
    def SetTimer(device, timer_mode: str, duration_seconds: int):
        return device.execute_command(DeviceFanTrait.COMMANDS["SetTimer"], {
            "timerMode": timer_mode,
            "duration": f"{duration_seconds}s"
        })


class DeviceHumidityTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.Humidity"

    def __init__(self, trait_dict):
        props = {"_ambient_humidity_percent": "ambientHumidityPercent"}
        super().__init__(self, props, trait_dict)


class DeviceSettingsTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.Settings"

    def __init__(self, trait_dict):
        props = {"_temperature_scale": "temperatureScale"}
        super().__init__(self, props, trait_dict)


class DeviceTemperatureTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.Temperature"

    def __init__(self, trait_dict):
        props = {"_ambient_temperature_celsius": "ambientTemperatureCelsius"}
        super().__init__(self, props, trait_dict)
