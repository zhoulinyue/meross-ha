"""Protocol frame tests."""

from __future__ import annotations

from datetime import UTC, datetime

from aiomeross_ble.const import (
    FRAME_HEAD,
    FRAME_TAIL,
    SUBDEV_MS120,
    TAG_SPECIAL,
    TAG_TEMP_HISTORY_COUNT,
    TAG_TEMP_HISTORY_DATA,
)
from aiomeross_ble.protocol import (
    build_identify_frame,
    build_temp_history_count_frame,
    crc16_ccitt_false,
    iter_tlvs,
    parse_history_count,
    parse_history_samples,
)


def test_crc16_empty() -> None:
    assert crc16_ccitt_false(b"") == 0xFFFF


def test_identify_frame_structure() -> None:
    frame = build_identify_frame(SUBDEV_MS120, msg_id=1)
    assert frame[:2] == FRAME_HEAD
    assert frame[-2:] == FRAME_TAIL
    assert frame[2] == SUBDEV_MS120
    tags = iter_tlvs(frame)
    assert tags == [(TAG_SPECIAL, bytes([0x05]))]


def test_parse_history_count_roundtrip() -> None:
    frame = build_temp_history_count_frame(SUBDEV_MS120, msg_id=1)
    # Count query has empty TLV value; simulate a response by rebuilding.
    from aiomeross_ble.protocol import build_meross_frame, build_tlv

    response = build_meross_frame(
        SUBDEV_MS120, 1, build_tlv(TAG_TEMP_HISTORY_COUNT, (12).to_bytes(2, "big"))
    )
    assert parse_history_count(response, TAG_TEMP_HISTORY_COUNT) == 12
    assert parse_history_count(frame, TAG_TEMP_HISTORY_COUNT) is None


def test_parse_history_samples() -> None:
    ts = int(datetime(2026, 1, 1, tzinfo=UTC).timestamp())
    record = (
        (3).to_bytes(2, "big")
        + ts.to_bytes(4, "big")
        + (2500).to_bytes(2, "big", signed=True)  # 25.00 C
    )
    from aiomeross_ble.protocol import build_meross_frame, build_tlv

    payload = build_meross_frame(
        SUBDEV_MS120, 1, build_tlv(TAG_TEMP_HISTORY_DATA, record)
    )
    samples = parse_history_samples(payload, TAG_TEMP_HISTORY_DATA, scale=100.0)
    assert len(samples) == 1
    assert samples[0].index == 3
    assert samples[0].value == 25.0
    assert samples[0].timestamp == datetime.fromtimestamp(ts, tz=UTC)
