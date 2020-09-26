import json
import logging
import os
import time
from typing import Callable, Dict, Optional, Union, List

from .devices import (
    SDMDevice,
    SDMCamera,
    SDMDisplay,
    SDMDoorbell,
    SDMThermostat,
)

from .structure import (
    SDMStructure,
)

from oauthlib.oauth2 import TokenExpiredError
from requests import Response
from requests_oauthlib import OAuth2Session
from google.cloud import pubsub_v1

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
        pubsub_subscription: str = None,
        pubsub_auth_path: str = None,
        token_updater: Optional[Callable[[str], None]] = None,
    ):
        self.project_id = project_id
        self.oauth_authorize = OAUTH2_AUTHORIZE_TEMPLATE.format(project_id)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_updater = token_updater
        self.token = token
        self._pubsub_subscription = pubsub_subscription
        self._pubsub_auth_path = pubsub_auth_path
        self._devices = []
        self._structures = []
        self._event_thread = None

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

    def listen_events(self):
        if self._event_thread is None:
            subscriber = pubsub_v1.SubscriberClient.from_service_account_file(
                self._pubsub_auth_path
            )

            def generate_callback():
                if not self._devices:
                    self.get_devices()
                if not self._structures:
                    self.get_structures()

                def handle_message(message):
                    msg = json.loads(message.data.decode())
                    event_id = msg["eventId"]
                    LOGGER.info(f"Received pubsub message: {event_id}")
                    LOGGER.debug(f"Received pubsub message: {msg}")
                    relevant_device = None
                    if "relationUpdate" in msg:
                        LOGGER.debug(
                            "Relation update, updating devices and structures"
                        )
                        self.get_devices(refresh=True)
                        self.get_structures(refresh=True)
                    elif "resourceUpdate" in msg:
                        for device in self._devices:
                            if msg["resourceUpdate"]["name"] == device.name:
                                relevant_device = device
                        if not relevant_device:
                            LOGGER.error(
                                f"Nacking pubsub message: {event_id}: "
                                + "No relevant device"
                            )
                            message.nack()
                            return
                        try:
                            relevant_device.event_callback(msg)
                            LOGGER.debug(f"Acking pubsub message: {event_id}")
                            message.ack()
                        except Exception as e:
                            LOGGER.error(
                                f"Nacking pubsub message: {event_id}: "
                                + f"{e}"
                            )
                            message.nack()
                    else:
                        LOGGER.error(
                            f"Nacking pubsub message: {event_id}: "
                            + "No processable events"
                        )
                        message.nack()
                return handle_message

            self._event_thread = subscriber.subscribe(
                self._pubsub_subscription,
                generate_callback()
            )

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

    def get_devices(self, refresh=False) -> List[SDMDevice]:
        """Return a list of `SDMDevice` instances for all
        devices."""
        if not self._devices or refresh:
            data = self._get(ENDPOINT_DEVICES.format(self.project_id))
            for device in data["devices"]:
                if device["type"] in self.DEVICE_TYPES:
                    self._devices.append(
                        self.DEVICE_TYPES[device["type"]](self, **device)
                    )
        return self._devices

    def get_structures(self, refresh=False) -> List[SDMStructure]:
        """Return a list of `SDMStructure` instances for all
        structures."""
        if not self._structures or refresh:
            data = self._get(ENDPOINT_STRUCTURES.format(self.project_id))
            for structure in data["structures"]:
                self._structures.append(
                    SDMStructure(self, **structure)
                )
        return self._structures

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
                 pubsub_subscription="",
                 pubsub_auth_path="",
                 token_cache=None):
        """Initialize the connection."""
        self.token_cache = token_cache or "google-sdm_oauth_token.json"

        super().__init__(
            self.token_load(),
            project_id,
            client_id,
            client_secret,
            redirect_uri,
            pubsub_subscription,
            pubsub_auth_path,
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
