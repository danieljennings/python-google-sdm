from .trait import Trait


class StructureInfoTrait(Trait):
    @staticmethod
    def name():
        return "sdm.structures.traits.Info"

    def __init__(self, trait_dict):
        props = {"_custom_name": "customName"}
        super().__init__(self, props, trait_dict)


class StructureRoomInfoTrait(Trait):
    @staticmethod
    def name():
        return "sdm.structures.traits.RoomInfo"

    def __init__(self, trait_dict):
        props = {"_custom_name": "customName"}
        super().__init__(self, props, trait_dict)
