import asyncio
from aiohttp import ClientSession
import aiohttp
from aiohttp.client_exceptions import ClientError

import logging
from typing import Dict, List, Type, TypeVar

from pytrutankless.device import Device
from pytrutankless.errors import (
    GenericHTTPError,
    InvalidCredentialsError,
    TruTanklessError,
)

BASE_URL = f"https://home.trutankless.com/"
DEVICES_URL = f"{BASE_URL}api/dashboard/devices/"
LOCATIONS_URL = f"{BASE_URL}api/dashboard/locations"
TOKEN_URL = f"{BASE_URL}api/dash-oauth/token"
HEADERS = {"Content-Type": "application/json"}
GRANT_TYPE = "password"
CLIENT_ID = "123"

_LOGGER = logging.getLogger(__name__)

ApiType = TypeVar("ApiType", bound="TruTanklessApiInterface")


class TruTanklessApiInterface:
    """API Interface object."""

    def __init__(self) -> None:
        """Create the TruTankless API interface object."""
        self._headers: str = HEADERS
        self._location_id: str
        self._user_id: str
        self._locations: List = {}
        self.devices: Dict = {}

    @classmethod
    async def login(cls: Type[ApiType], email: str, password: str) -> ApiType:
        """Create a TruTanklessApiInterface object using email and password."""
        this_class = cls()
        await this_class._authenticate(
            {
                "username": email,
                "password": password,
                "grant_type": GRANT_TYPE,
                "client_id": CLIENT_ID,
            }
        )
        return this_class

    async def _authenticate(self, payload: dict) -> None:
        async with aiohttp.ClientSession() as _session:
            try:
                async with _session.post(TOKEN_URL, data=payload) as token_resp:
                    _token_json = await token_resp.json()
                    if token_resp.status == 200:
                        _LOGGER.debug(_token_json)
                        _access_token = _token_json["access_token"]
                        _token_type = _token_json["token_type"].capitalize()
                        self._user_id = _token_json["user_id"]
                        self._headers[
                            "authorization"
                        ] = f"{_token_type} {_access_token}"
                        await _session.close()
                    elif token_resp.status == 400:
                        for error_title in _token_json.values():
                            if error_title == "invalid_grant":
                                raise InvalidCredentialsError(
                                    _token_json["error_description"]
                                )
                            else:
                                raise GenericHTTPError(_token_json["error_description"])
            except ClientError as err:
                raise err
            finally:
                await _session.close()

    async def get_devices(self) -> Dict:
        """Get a list of all the devices for this user and instantiate device objects."""
        await self._get_locations()
        for _devlist in self._locations["devices"]:
            _dev_obj = Device(_devlist, self)
            self.devices[_dev_obj.device_id] = _dev_obj
            return self.devices

    async def refresh_device(self, device: str) -> Dict:
        """Fetch updated data for a device."""

        async with ClientSession() as _refresh_session:
            _device_url = f"{DEVICES_URL}{device}"
            try:
                async with _refresh_session.get(
                    _device_url, headers=self._headers
                ) as refr:
                    if refr.status == 200:
                        _refdata = await refr.json()
                        _LOGGER.debug(f"Retrieved updated data from API: {_refdata}")
                        dev_obj = self.devices.get(_refdata.get("id", ""), None)
                        if dev_obj:
                            await dev_obj.update_device_info(_refdata)
            except ClientError as err:
                _LOGGER.error("Failed to fetch device.")
                raise err
            finally:
                await _refresh_session.close()
                return dev_obj

    async def _get_locations(self) -> Dict:
        async with ClientSession() as _location_session:
            try:
                async with _location_session.get(
                    LOCATIONS_URL, headers=self._headers
                ) as resp:
                    if resp.status == 200:
                        _json = await resp.json()
                        _LOGGER.debug(_json)
                        for _ind in _json:
                            self._locations = _ind
                    elif resp.status == 401:
                        raise InvalidCredentialsError(resp.status)
                    else:
                        raise GenericHTTPError(resp.status)
            except ClientError as err:
                raise err
            finally:
                await _location_session.close()

    @property
    def user_id(self) -> str:
        """Return the user id."""
        return self._user_id
