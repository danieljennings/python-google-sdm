from .trait import Trait


class CameraEventImageTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.CameraEventImage"

    COMMANDS = {
        "GenerateImage": "sdm.devices.commands.CameraEventImage.GenerateImage",
    }

    def __init__(self, trait_dict):
        props = {}
        super().__init__(self, props, trait_dict)

    @staticmethod
    def GenerateImage(device, event_id: str):
        return device.execute_command(
            CameraEventImageTrait.COMMANDS["GenerateImage"],
            {"eventId": event_id}
        )


class CameraImageTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.CameraImage"

    def __init__(self, trait_dict):
        props = {
            "_max_image_resolution": "maxImageResolution",
        }
        super().__init__(self, props, trait_dict)


class CameraLiveStreamTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.CameraLiveStream"

    COMMANDS = {
        "GenerateRtspStream":
            "sdm.devices.commands.CameraLiveStream.GenerateRtspStream",
        "ExtendRtspStream":
            "sdm.devices.commands.CameraLiveStream.ExtendRtspStream",
        "StopRtspStream":
            "sdm.devices.commands.CameraLiveStream.StopRtspStream",
    }

    def __init__(self, trait_dict):
        props = {
            "_max_video_resolution": "maxVideoResolution",
            "_video_codecs": "videoCodecs",
            "_audio_codecs": "audioCodecs",
        }
        super().__init__(self, props, trait_dict)

    @staticmethod
    def GenerateRtspStream(device):
        return device.execute_command(
            CameraLiveStreamTrait.COMMANDS["GenerateRtspStream"],
            {}
        )

    @staticmethod
    def ExtendRtspStream(device, stream_extension_token: str):
        return device.execute_command(
            CameraLiveStreamTrait.COMMANDS["ExtendRtspStream"],
            {"streamExtensionToken": stream_extension_token}
        )

    @staticmethod
    def StopRtspStream(device, stream_extension_token: str):
        return device.execute_command(
            CameraLiveStreamTrait.COMMANDS["StopRtspStream"],
            {"streamExtensionToken": stream_extension_token}
        )


class CameraMotionTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.CameraMotion"

    def __init__(self, trait_dict):
        props = {}
        super().__init__(self, props, trait_dict)


class CameraPersonTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.CameraPerson"

    def __init__(self, trait_dict):
        props = {}
        super().__init__(self, props, trait_dict)


class CameraSoundTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.CameraSound"

    def __init__(self, trait_dict):
        props = {}
        super().__init__(self, props, trait_dict)
