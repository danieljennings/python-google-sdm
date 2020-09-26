# Google SDM (Smart Device Management) API

## Rough TODO

- Ability to get parent SDMStructure/Room from SDMDevice object
- Tests
- Finish this readme with docs on setup
- Home Assistant integration (in testing) after this API completes

## Example usage

```python
import time

from google_sdm.api import SDM
from google_sdm.devices import (
    SDMCamera,
    SDMDisplay,
    SDMDoorbell,
    SDMThermostat,
)
from google_sdm.traits import (
    DeviceFanTrait,
    ThermostatEcoTrait,
    ThermostatModeTrait,
    ThermostatTemperatureSetpointTrait,
)

PROJECT_ID = "aaaaaa-bbbb-cccc-dddd-eeeeeeeeeee"
CLIENT_ID = \
    "fffffff-ggggggggggggggggggggggg.apps.googleusercontent.com"
CLIENT_SECRET = "hhhhhhhhhhhhhhhhhhhh"

if __name__ == "__main__":
    api = SDM(
        PROJECT_ID,
        CLIENT_ID,
        CLIENT_SECRET,
        redirect_uri="https://www.google.com"
    )

    # Handle Auth
    if not api.token_load():
        auth_url = api.get_authurl()
        api.get_token(
            input(f"{auth_url}\nEnter the URL you are redirected to: ")
        )
    api.refresh_tokens()

    # Use the API
    devices = api.get_devices()
    for device in devices:
        print(device)
        print(device.get_info())
        if isinstance(device, SDMCamera):
            print(device)
        elif isinstance(device, SDMDisplay):
            print(device)
        elif isinstance(device, SDMDoorbell):
            print(device)
        elif isinstance(device, SDMThermostat):
            # Device methods
            print(device.get_connectivity())
            print(device.get_fan())
            # SetTimer command
            DeviceFanTrait.SetTimer(
                device,
                timer_mode=DeviceFanTrait.TIMER_MODE_ON,
                duration_seconds=120
            )
            print(device.get_fan())
            print(device.get_humidity())
            print(device.get_settings())
            print(device.get_temperature())

            # Thermostat methods
            print(device.get_thermostat_eco())
            print(device.get_thermostat_hvac())
            print(device.get_thermostat_mode())
            print(device.get_thermostat_temperature_setpoint())

            # Eco
            ThermostatEcoTrait.SetMode(
                device,
                mode=ThermostatEcoTrait.ECO_MODE_ON
            )
            time.sleep(5)
            ThermostatEcoTrait.SetMode(
                device,
                mode=ThermostatEcoTrait.ECO_MODE_OFF
            )

            # Cool
            ThermostatTemperatureSetpointTrait.SetCool(
                device,
                cool_celsius=18.72716
            )
            time.sleep(5)
            ThermostatTemperatureSetpointTrait.SetCool(
                device,
                cool_celsius=19.72716
            )

            # HeatCool
            ThermostatModeTrait.SetMode(
                device,
                mode=ThermostatModeTrait.THERMOSTAT_MODE_HEATCOOL
            )
            time.sleep(5)
            ThermostatTemperatureSetpointTrait.SetRange(
                device,
                cool_celsius=18.72716,
                heat_celsius=21.72716,
            )
            time.sleep(5)
            ThermostatTemperatureSetpointTrait.SetRange(
                device,
                cool_celsius=19.72716,
                heat_celsius=20.72716,
            )
            time.sleep(5)

            # Heat
            ThermostatModeTrait.SetMode(
                device,
                mode=ThermostatModeTrait.THERMOSTAT_MODE_HEAT
            )
            time.sleep(5)
            ThermostatTemperatureSetpointTrait.SetHeat(
                device,
                heat_celsius=21.72716,
            )
            time.sleep(5)
            ThermostatTemperatureSetpointTrait.SetHeat(
                device,
                heat_celsius=20.72716,
            )
            time.sleep(5)

            # Back to cool
            ThermostatModeTrait.SetMode(
                device,
                mode=ThermostatModeTrait.THERMOSTAT_MODE_COOL
            )

        else:
            raise NotImplementedError
```
