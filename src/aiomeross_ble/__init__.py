"""Python library for Meross Bluetooth devices."""

from .const import (
    BATTERY_LOW_THRESHOLD,
    CONNECTABLE_MODELS,
    DEFAULT_RETRY_COUNT,
    MEROSS_GATT_SERVICE,
    MEROSS_SERVICE_DATA_UUID,
    MODEL_FRIENDLY_NAME,
    MS220_EVENT_BUTTON_DOUBLE,
    MS220_EVENT_BUTTON_SINGLE,
    MS220_EVENT_DOORBELL,
    MS700_BUTTON_COUNT,
    PASSIVE_MODELS,
    MerossModel,
    ms220_alarm_feature_enabled,
    ms700_button_enabled,
    ms700_default_button_name,
    ms700_logical_button,
)
from .device import MerossBLEDevice, MerossBLEError, create_device
from .parser import MerossAdvertisement, is_meross_device, parse_advertisement_data
from .protocol import HistorySample
from .psychrometrics import (
    absolute_humidity_gm3,
    dew_point_celsius,
    vapor_pressure_deficit_kpa,
)

__all__ = [
    "BATTERY_LOW_THRESHOLD",
    "CONNECTABLE_MODELS",
    "DEFAULT_RETRY_COUNT",
    "MEROSS_GATT_SERVICE",
    "MEROSS_SERVICE_DATA_UUID",
    "MODEL_FRIENDLY_NAME",
    "MS220_EVENT_BUTTON_DOUBLE",
    "MS220_EVENT_BUTTON_SINGLE",
    "MS220_EVENT_DOORBELL",
    "MS700_BUTTON_COUNT",
    "PASSIVE_MODELS",
    "HistorySample",
    "MerossAdvertisement",
    "MerossBLEDevice",
    "MerossBLEError",
    "MerossModel",
    "absolute_humidity_gm3",
    "create_device",
    "dew_point_celsius",
    "is_meross_device",
    "ms220_alarm_feature_enabled",
    "ms700_button_enabled",
    "ms700_default_button_name",
    "ms700_logical_button",
    "parse_advertisement_data",
    "vapor_pressure_deficit_kpa",
]
