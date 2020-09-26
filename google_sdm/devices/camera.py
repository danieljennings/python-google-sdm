from .generic import SDMDevice


class SDMCamera(SDMDevice):
    STR_REPR = "sdm.devices.types.CAMERA"

    def __repr__(self):
        return self.STR_REPR
