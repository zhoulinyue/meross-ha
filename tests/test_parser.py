"""Advertisement parser tests."""

from __future__ import annotations

from types import SimpleNamespace

from meross_ble import MerossModel, parse_advertisement_data
from meross_ble.const import MEROSS_SERVICE_DATA_UUID, SUBDEV_MS120, SUBDEV_MS220
from meross_ble.psychrometrics import dew_point_celsius


def _device(address: str = "AA:BB:CC:DD:EE:FF", name: str = "Meross-MS120-EEFF"):
    return SimpleNamespace(address=address, name=name)


def _adv(*, service_data: dict, rssi: int = -50, local_name: str | None = None, service_uuids: list | None = None):
    return SimpleNamespace(
        local_name=local_name,
        rssi=rssi,
        service_data=service_data,
        service_uuids=service_uuids or [],
        manufacturer_data={},
    )


def test_parse_ms120_temperature_humidity() -> None:
    payload = bytes(
        [
            0x01,
            SUBDEV_MS120,
            0x00,
            0x00,
            80,
            0x02,
            0x00,
            0x00,
            0x09,
            0xC4,  # 25.00 C
            0x13,
            0x88,  # 50.00 %
        ]
    )
    adv = parse_advertisement_data(
        _device(),
        _adv(service_data={MEROSS_SERVICE_DATA_UUID: payload}, local_name="Meross-MS120-EEFF"),
    )
    assert adv is not None
    assert adv.model is MerossModel.MS120
    assert adv.data["temperature"] == 25.0
    assert adv.data["humidity"] == 50.0
    assert adv.data["battery"] == 80
    assert adv.data["dew_point"] == dew_point_celsius(25.0, 50.0)
    assert adv.events == []


def test_parse_ms220_door_open() -> None:
    payload = bytes(
        [
            0x01,
            SUBDEV_MS220,
            0x01,  # door open
            0x00,
            90,
            0x01,
            0x00,
            0x00,
            0x07,  # alarm enable all
        ]
    )
    adv = parse_advertisement_data(
        _device(name="Meross-MS220-EEFF"),
        _adv(service_data={MEROSS_SERVICE_DATA_UUID: payload}),
    )
    assert adv is not None
    assert adv.model is MerossModel.MS220
    assert adv.data["door_open"] is True
    assert adv.data["alarm_enable_door_open_long"] is True


def test_ignore_unrelated_advertisement() -> None:
    adv = parse_advertisement_data(
        _device(name="Other"),
        _adv(service_data={"0000180f-0000-1000-8000-00805f9b34fb": b"\x64"}),
    )
    assert adv is None
