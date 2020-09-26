import json
import logging
import os
import time
import threading
from typing import Callable, Dict, Optional, Union, List

from .devices import (
    SDMDevice,
    SDMCamera,
    SDMDisplay,
    SDMDoorbell,
    SDMThermostat,
)

from oauthlib.oauth2 import TokenExpiredError
from requests import Response
from requests_oauthlib import OAuth2Session
# from google.cloud import pubsub_v1

API_URL = "https://smartdevicemanagement.googleapis.com/v1/"
OAUTH2_AUTHORIZE_TEMPLATE = \
    "https://nestservices.google.com/partnerconnections/{}/auth"
OAUTH2_TOKEN = "https://www.googleapis.com/oauth2/v4/token"
OAUTH2_SCOPE = "https://www.googleapis.com/auth/sdm.service"
ENDPOINT_DEVICES = 'enterprises/{}/devices'
ENDPOINT_STRUCTURES = 'enterprises/{}/structures'

LOGGER = logging.getLogger("google-sdm")


class SDMError(Exception):
    pass


class SDMAPI(object):

    DEVICE_TYPES = {
        SDMCamera.STR_REPR: SDMCamera,
        SDMDisplay.STR_REPR: SDMDisplay,
        SDMDoorbell.STR_REPR: SDMDoorbell,
        SDMThermostat.STR_REPR: SDMThermostat,
    }

    def __init__(
        self,
        token: Optional[Dict[str, str]] = None,
        project_id: str = None,
        client_id: str = None,
        client_secret: str = None,
        redirect_uri: str = None,
        token_updater: Optional[Callable[[str], None]] = None,
    ):
        self.project_id = project_id
        self.oauth_authorize = OAUTH2_AUTHORIZE_TEMPLATE.format(project_id)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_updater = token_updater
        self.token = token
        self._event_thread = None
        self._update_event = threading.Event()

        extra = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        self._oauth = OAuth2Session(
            client_id=client_id,
            redirect_uri=redirect_uri,
            auto_refresh_url=OAUTH2_TOKEN,
            auto_refresh_kwargs=extra,
            token=token,
            token_updater=token_updater,
            scope=OAUTH2_SCOPE,
        )

    @property
    def update_event(self):
        return self._update_event

    def start_polling(self, callback):
        pass
        # sub_id = "projects/personalnginx/subscriptions/nest-sdm-events"
        # subscriber = pubsub_v1.SubscriberClient.from_service_account_file(
        #     '/home/reddragon/Downloads/PersonalNginx-b73893284eb5.json'
        # )
        # self._event_thread = subscriber.subscribe(sub_id, callback)

    def refresh_tokens(self) -> Dict[str, Union[str, int]]:
        """Refresh and return new tokens."""
        LOGGER.info("Refreshing tokens ...")
        token = self._oauth.refresh_token(OAUTH2_TOKEN)

        if self.token_updater is not None:
            self.token_updater(token)

        return token

    def _request(self, method: str, path: str, **kwargs) -> Response:
        """Make a request.
        We don't use the built-in token refresh mechanism of OAuth2 session
        because we want to allow overriding the token refresh logic.
        """
        url = f"{API_URL}{path}"
        LOGGER.debug(f"Request: {method} {url}")

        try:
            return getattr(self._oauth, method)(url, **kwargs)
        except TokenExpiredError:
            LOGGER.warning("Token expired.")
            self._oauth.token = self.refresh_tokens()

            return getattr(self._oauth, method)(url, **kwargs)

    def _get(self, endpoint):
        """Get data as dictionary from an endpoint."""
        res = self._request("get", endpoint)
        if not res.content:
            return {}
        try:
            res = res.json()
        except json.JSONDecodeError:
            raise ValueError("Cannot parse {} as JSON".format(res))
        if "error" in res:
            raise SDMError(res["error"])
        return res

    def _post(self, endpoint, data):
        """Get data as dictionary from an endpoint."""
        res = self._request("post", endpoint, data=json.dumps(data))
        if not res.content:
            return {}
        try:
            res = res.json()
        except json.JSONDecodeError:
            raise ValueError("Cannot parse {} as JSON".format(res))
        if "error" in res:
            if "code" in res['error'] and res['error']['code'] == 401:
                raise TokenExpiredError()
            else:
                raise SDMError(res["error"])
        return res

    def get_devices(self) -> List[SDMDevice]:
        """Return a list of `SDMDevice` instances for all
        devices."""
        devices = []
        data = self._get(ENDPOINT_DEVICES.format(self.project_id))
        for device in data["devices"]:
            if device["type"] in self.DEVICE_TYPES:
                devices.append(
                    self.DEVICE_TYPES[device["type"]](self, **device)
                )
        return devices

    def get_structures(self):
        """Return a list of `SDMStructure` instances for all
        structures."""
        data = self._get(ENDPOINT_STRUCTURES.format(self.project_id))
        return [SDMStructure(self, **app) for app in data["structures"]]

    def get_authurl(self):
        """Get the URL needed for the authorization code grant flow."""
        authorization_url, _ = self._oauth.authorization_url(
            self.oauth_authorize,
            access_type="offline",
            prompt="consent"
        )
        return authorization_url


class SDM(SDMAPI):
    """Connection to the Google Smart Device Management OAuth API."""

    def __init__(self,
                 project_id,
                 client_id,
                 client_secret="",
                 redirect_uri="",
                 token_cache=None):
        """Initialize the connection."""
        self.token_cache = token_cache or "google-sdm_oauth_token.json"

        super().__init__(
            self.token_load(),
            project_id,
            client_id,
            client_secret,
            redirect_uri,
            self.token_dump
        )

    def token_dump(self, token):
        """Dump the token to a JSON file."""
        with open(self.token_cache, "w") as f:
            json.dump(token, f)

    def token_load(self):
        """Load the token from the cache if exists it and is not expired,
        otherwise return None."""
        if not os.path.exists(self.token_cache):
            return None
        with open(self.token_cache, "r") as f:
            token = json.load(f)
        now = int(time.time())
        token["expires_in"] = token.get("expires_at", now - 1) - now
        return token

    def token_expired(self, token):
        """Check if the token is expired."""
        now = int(time.time())
        return token["expires_at"] - now < 60

    def get_token(self, authorization_response):
        """Get the token given the redirect URL obtained from the
        authorization."""
        LOGGER.info("Fetching token ...")
        token = self._oauth.fetch_token(
            OAUTH2_TOKEN,
            authorization_response=authorization_response,
            client_secret=self.client_secret,
        )
        self.token_dump(token)


class SDMObject:
    pass


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

    @staticmethod
    def json2dict(lst):
        """Turn a list of dictionaries where one key is called 'key'
        into a dictionary with the value of 'key' as key."""
        return {d.pop("key"): d for d in lst}

    def _get(self, endpoint):
        """Get data (as dictionary) from an endpoint."""
        return self.api._get(f"{self.name}{endpoint}")

    def get_rooms(self):
        """Get structure rooms."""
        data = self._get("/rooms")
        return [SDMStructure.Room(self.api, **app) for app in data["rooms"]]

    def update(self):
        """Return this structure with updated data."""
        return SDMStructure(self, **self._get(""))

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

        @staticmethod
        def json2dict(lst):
            """Turn a list of dictionaries where one key is called 'key'
            into a dictionary with the value of 'key' as key."""
            return {d.pop("key"): d for d in lst}

        def _get(self, endpoint):
            """Get data (as dictionary) from an endpoint."""
            return self.api._get(f"{self.name}{endpoint}")

        def update(self):
            """Get active programs."""
            return SDMStructure.Room(self, **self._get(""))
