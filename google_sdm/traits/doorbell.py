from .trait import Trait


class DoorbellChimeTrait(Trait):
    @staticmethod
    def name():
        return "sdm.devices.traits.CameraMotion"

    def __init__(self, trait_dict):
        props = {}
        super().__init__(self, props, trait_dict)
