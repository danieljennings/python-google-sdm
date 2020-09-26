from .trait import Trait


class ThermostatEcoTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.ThermostatEco"

    COMMANDS = {
        "SetMode": "sdm.devices.commands.ThermostatEco.SetMode",
    }

    def __init__(self, trait_dict):
        props = {
            "_available_modes": "availableModes",
            "_mode": "mode",
            "_heat_celsius": "heatCelsius",
            "_cool_celsius": "coolCelsius",
        }
        super().__init__(self, props, trait_dict)

    ECO_MODE_ON = "MANUAL_ECO"
    ECO_MODE_OFF = "OFF"

    @staticmethod
    def SetMode(device, mode: str):
        return device.execute_command(ThermostatEcoTrait.COMMANDS["SetMode"], {
            "mode": mode,
        })


class ThermostatHvacTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.ThermostatHvac"

    def __init__(self, trait_dict):
        props = {"_status": "status"}
        super().__init__(self, props, trait_dict)


class ThermostatModeTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.ThermostatMode"

    COMMANDS = {
        "SetMode": "sdm.devices.commands.ThermostatMode.SetMode",
    }

    def __init__(self, trait_dict):
        props = {
            "_available_modes": "availableModes",
            "_mode": "mode",
        }
        super().__init__(self, props, trait_dict)

    THERMOSTAT_MODE_HEAT = "HEAT"
    THERMOSTAT_MODE_COOL = "COOL"
    THERMOSTAT_MODE_HEATCOOL = "HEATCOOL"
    THERMOSTAT_MODE_OFF = "OFF"

    @staticmethod
    def SetMode(device, mode: str):
        return device.execute_command(
            ThermostatModeTrait.COMMANDS["SetMode"],
            {"mode": mode}
        )


class ThermostatTemperatureSetpointTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.ThermostatTemperatureSetpoint"

    COMMANDS = {
        "SetHeat":
            "sdm.devices.commands.ThermostatTemperatureSetpoint.SetHeat",
        "SetCool":
            "sdm.devices.commands.ThermostatTemperatureSetpoint.SetCool",
        "SetRange":
            "sdm.devices.commands.ThermostatTemperatureSetpoint.SetRange",
    }

    def __init__(self, trait_dict):
        props = {
            "_heat_celsius": "heatCelsius",
            "_cool_celsius": "coolCelsius",
        }
        super().__init__(self, props, trait_dict)

    @staticmethod
    def SetHeat(device, heat_celsius: float):
        return device.execute_command(
            ThermostatTemperatureSetpointTrait.COMMANDS["SetHeat"], {
                "heatCelsius": heat_celsius,
            })

    @staticmethod
    def SetCool(device, cool_celsius: float):
        return device.execute_command(
            ThermostatTemperatureSetpointTrait.COMMANDS["SetCool"], {
                "coolCelsius": cool_celsius,
            })

    @staticmethod
    def SetRange(device, cool_celsius: float, heat_celsius: float):
        return device.execute_command(
            ThermostatTemperatureSetpointTrait.COMMANDS["SetRange"], {
                "coolCelsius": cool_celsius,
                "heatCelsius": heat_celsius,
            })
