from .generic import SDMDevice

from ..traits import (
    SDMTraitGetter,
    CameraImageTrait,
    CameraLiveStreamTrait,
)


class SDMDoorbell(SDMDevice):
    STR_REPR = "sdm.devices.types.DOORBELL"

    def __repr__(self):
        return self.STR_REPR

    @SDMTraitGetter(CameraImageTrait)
    def get_camera_image_trait(self, **kwargs) \
            -> CameraImageTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    @SDMTraitGetter(CameraLiveStreamTrait)
    def get_camera_live_stream_trait(self, **kwargs) \
            -> CameraLiveStreamTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]
