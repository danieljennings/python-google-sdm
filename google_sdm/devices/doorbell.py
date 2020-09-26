from .generic import SDMDevice


class SDMDoorbell(SDMDevice):
    STR_REPR = "sdm.devices.types.DOORBELL"

    def __repr__(self):
        return self.STR_REPR
