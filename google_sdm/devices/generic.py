from ..traits import SDMTraitGetter, DeviceInfoTrait


class SDMDevice():
    """Class representing a single SDM device."""

    def __init__(
        self,
        api,
        type,
        assignee=None,
        traits=None,
        parentRelations=None,
        name=None,
        connected=False,
    ):
        self.api = api
        self.type = type
        self.assignee = assignee or ""
        self.traits = traits or {}
        self.parentRelations = parentRelations or [{}]
        self.name = name or ""
        self.connected = connected
        self.status = {}

    def __repr__(self):
        rep = "SDMDevice("
        rep += "api, type='{}', assignee='{}', traits='{}', "
        rep += "parentRelations='{}', name='{}', connected='{}'"
        rep += ")"

        return rep.format(
            self.type,
            self.assignee,
            self.traits,
            self.parentRelations,
            self.name,
            self.connected,
        )

    def _get(self, endpoint):
        """Get data (as dictionary) from an endpoint."""
        return self.api._get(f"{self.name}{endpoint}")

    def _post(self, endpoint, data):
        """Post data (as json) to an endpoint."""
        return self.api._post(f"{self.name}{endpoint}", data)

    def execute_command(self, command, params):
        """Uses the :executeCommand endpoint."""
        return self._post(
            ":executeCommand",
            {"command": command, "params": params},
        )

    @SDMTraitGetter(DeviceInfoTrait)
    def get_info(self, **kwargs):
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]
