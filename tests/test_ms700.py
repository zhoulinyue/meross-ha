"""MS700 button mapping tests."""

from aiomeross_ble.const import (
    ms700_button_enabled,
    ms700_default_button_name,
    ms700_logical_button,
)


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
