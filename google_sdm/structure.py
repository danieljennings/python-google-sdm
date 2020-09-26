from .traits import (
    SDMTraitGetter,
    StructureInfoTrait,
    StructureRoomInfoTrait,
)


class SDMStructure:
    """Class representing a single SDM structure."""

    def __init__(
        self,
        api,
        name,
        traits=None,
    ):
        self.api = api
        self.name = name
        self.traits = traits or {}

    def __repr__(self):
        rep = "SDMStructure("
        rep += "api, name='{}', traits='{}'"
        rep += ")"

        return rep.format(
            self.name,
            self.traits,
        )

    def _get(self, endpoint):
        """Get data (as dictionary) from an endpoint."""
        return self.api._get(f"{self.name}{endpoint}")

    def get_rooms(self):
        """Get structure rooms."""
        data = self._get("/rooms")
        return [SDMStructure.Room(self.api, **app) for app in data["rooms"]]

    @SDMTraitGetter(StructureInfoTrait)
    def get_info(self, **kwargs) \
            -> StructureInfoTrait:
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    StructureRoomInfoTrait

    class Room:
        """Class representing a single SDM structure's room."""

        def __init__(
            self,
            api,
            name,
            traits=None,
        ):
            self.api = api
            self.name = name
            self.traits = traits or {}

        def __repr__(self):
            rep = "SDMStructure.Room("
            rep += "api, name='{}', traits='{}'"
            rep += ")"

            return rep.format(
                self.name,
                self.traits,
            )

        def _get(self, endpoint):
            """Get data (as dictionary) from an endpoint."""
            return self.api._get(f"{self.name}{endpoint}")

        @SDMTraitGetter(StructureRoomInfoTrait)
        def get_info(self, **kwargs) \
                -> StructureRoomInfoTrait:
            if "trait" not in kwargs:
                return None
            return kwargs["trait"]
