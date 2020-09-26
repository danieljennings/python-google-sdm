
from .generic import SDMDevice


class SDMDisplay(SDMDevice):
    STR_REPR = "sdm.devices.types.DISPLAY"

    def __repr__(self):
        return self.STR_REPR
