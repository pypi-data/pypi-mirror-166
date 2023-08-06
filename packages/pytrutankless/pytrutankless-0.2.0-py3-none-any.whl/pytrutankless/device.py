"""Define a TruTankless water heater device."""
import logging

_LOGGER = logging.getLogger(__name__)


class Device:
    """Define a device."""

    def __init__(self, device_info: dict, api_interface) -> None:
        self._api = api_interface
        self._device_info = device_info

    async def update_device_info(self, update: dict):
        """Take a dict and update the stored _device_info based on the present dict fields."""
        if update.get("id") == self.device_id:
            for key, value in update.items():
                _LOGGER.debug("Before update %s : %s", key, self._device_info.get(key))
                try:
                    if self._device_info[key] is not None:
                        self._device_info[key] = value
                        _LOGGER.debug("Updating [%s] = %s", key, value)
                        return self._device_info
                except Exception:
                    _LOGGER.error("Failed to update with message: %s", update)
                _LOGGER.debug("After update %s : %s", key, self._device_info.get(key))
        else:
            _LOGGER.debug("Invalid update for device: %s", update)

    @property
    def device_id(self) -> str:
        """Return the device id."""
        return self._device_info["id"]

    @property
    def device_status(self) -> str:
        """Return device status."""
        return self._device_info["device_status"]

    @property
    def label(self) -> str:
        """Return device label."""
        return self._device_info["label"]

    @property
    def location_id(self) -> str:
        """Return the location id."""
        return self._device_info["location_id"]

    @property
    def model(self) -> str:
        """Return device model."""
        return self._device_info["model"]

    @property
    def serial_number(self) -> str:
        """Return device serial number."""
        return self._device_info["serial_number"]

    @property
    def inlet_temperature(self) -> str:
        """Return device inlet temperature."""
        in_temp = float(self._device_info["current_data"]["inlet_temperature"])
        return in_temp

    @property
    def outlet_temperature(self) -> str:
        """Return device outlet temperature."""
        out_temp = float(self._device_info["current_data"]["outlet_temperature"])
        return out_temp

    @property
    def temperature_set_point(self) -> str:
        """Return device temperature set point."""
        temp_set = round(
            float(self._device_info["current_data"]["temperature_set_point"]), 2
        )
        return temp_set

    @property
    def pending_temperature_set_point(self) -> str:
        """Return device pending temperature set point."""
        pend_temp = round(
            float(self._device_info["current_data"]["pending_temperature_set_point"]), 2
        )
        return pend_temp

    @property
    def error_code(self) -> str:
        """Return device error code."""
        return self._device_info["current_data"]["error_code"]

    @property
    def error_message(self) -> str:
        """Return device error message."""
        return self._device_info["current_data"]["error_message"]

    @property
    def pcb_temp(self) -> str:
        """Return the pcb temperature of the device."""
        board_temp = float(self._device_info["current_data"]["pcb_temp"])
        return board_temp

    @property
    def power_percentage(self) -> str:
        """Return device power percentage."""
        pow_perc = float(self._device_info["current_data"]["power_percentage"])
        return pow_perc

    @property
    def total_flow(self) -> str:
        """Return device total_flow."""
        return self._device_info["current_data"]["total_flow"]

    @property
    def total_watt_seconds(self) -> str:
        """Return device total watt in seconds."""
        return self._device_info["current_data"]["total_watt_seconds"]

    @property
    def incoming_voltage(self) -> str:
        """Return device incoming voltage."""
        return self._device_info["current_data"]["incoming_voltage"]

    @property
    def eco_setting(self) -> str:
        """Return device eco setting."""
        return self._device_info["current_data"]["eco_setting"]

    @property
    def pending_eco_setting(self) -> str:
        """Return device pending eco setting."""
        return self._device_info["current_data"]["pending_eco_setting"]

    @property
    def vacation_setting(self) -> str:
        """Return device vacation setting."""
        return self._device_info["current_data"]["vacation_setting"]

    @property
    def pending_vacation_setting(self) -> str:
        """Return device pending vacation setting."""
        return self._device_info["current_data"]["pending_vacation_setting"]
