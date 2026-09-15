"""MS700 button mapping and advertisement event tests."""

from types import SimpleNamespace

from meross_ble.const import (
    ms700_button_enabled,
    ms700_default_button_name,
    ms700_logical_button,
)
from meross_ble.device import MerossBLEDevice
from meross_ble.parser import MerossAdvertisement
from meross_ble.const import MerossModel


def test_ms700_logical_button() -> None:
    # screen 1 button 1
    assert ms700_logical_button(0b0001_01) == 1
    # packed as (screen << 2) | button
    assert ms700_logical_button((1 << 2) | 1) == 1
    assert ms700_logical_button((2 << 2) | 3) == 6
    assert ms700_logical_button((3 << 2) | 3) == 9
    assert ms700_logical_button(0x10) is None


def test_ms700_screen_enable() -> None:
    assert ms700_button_enabled(1, 0b001) is True
    assert ms700_button_enabled(4, 0b001) is False
    assert ms700_button_enabled(4, 0b011) is True
    assert ms700_default_button_name(5) == "screen2-button2"


def _ble_device(address: str = "AA:BB:CC:DD:EE:FF"):
    return SimpleNamespace(address=address, name="Meross-MS700-EEFF")


def _adv(
    *,
    events: list[tuple[int, int]],
    data: dict | None = None,
) -> MerossAdvertisement:
    device = _ble_device()
    return MerossAdvertisement(
        address=device.address,
        device=device,  # type: ignore[arg-type]
        rssi=-50,
        model=MerossModel.MS700,
        data=data or {"status": 0, "alarm_status": 0, "screen_enable": 0x07},
        events=events,
    )


def test_ms700_long_press_does_not_block_short_press() -> None:
    """Long-press / reserved-bit events must not advance last_accepted.

    Matches meross_rpc master fix: after a local-only long-press UI event,
    a following short press (same or next req_id) must still fire.
    """
    device = MerossBLEDevice(_ble_device(), MerossModel.MS700)  # type: ignore[arg-type]
    short = (1 << 2) | 1  # screen1 button1
    long_press = 0x11  # high nibble set → unmapped

    assert device.update_from_advertisement(_adv(events=[(1, short)])) == []
    assert device._last_accepted_req_id == 1

    assert device.update_from_advertisement(_adv(events=[(2, long_press)])) == []
    assert device._last_accepted_req_id == 1

    accepted = device.update_from_advertisement(_adv(events=[(2, short)]))
    assert accepted == [(2, short)]
    assert device._last_accepted_req_id == 2
