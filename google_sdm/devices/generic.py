from abc import ABC
from datetime import timezone, datetime

from ..traits import SDMTraitGetter, DeviceInfoTrait
from ..utils import deep_merge


class SDMDevice(ABC):
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
        self.last_updated = datetime.now(tz=timezone.utc)
        self._update_listeners = []
        self._event_listeners = []

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

    def register_update_listener(self, update_listener):
        self._update_listeners.append(update_listener)

    def register_event_listener(self, event_listener):
        self._event_listeners.append(event_listener)

    @SDMTraitGetter(DeviceInfoTrait)
    def get_info(self, **kwargs):
        if "trait" not in kwargs:
            return None
        return kwargs["trait"]

    def event_callback(self, message):
        timestamp = datetime.strptime(
            message["timestamp"],
            '%Y-%m-%dT%H:%M:%S.%f%z'
        )
        if timestamp > self.last_updated:
            self.last_updated = timestamp
            if "events" in message["resourceUpdate"]:
                for event_listener in self._event_listeners:
                    event_listener(message["resourceUpdate"]["events"])
            elif "traits" in message["resourceUpdate"]:
                self.traits = deep_merge(
                    self.traits,
                    message["resourceUpdate"]["traits"]
                )
                for update_listener in self._update_listeners:
                    update_listener(message["resourceUpdate"]["traits"])
            else:
                raise Exception(
                    f"Unable to handle event for device {self.name}"
                )
