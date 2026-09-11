# meross-ble

Python library for [Meross](https://www.meross.com/) Bluetooth devices. Protocol, advertisement parsing, and GATT helpers live here so Home Assistant (and other projects) only deal with entities and coordinators.

This package has **no Home Assistant dependency**.

Install name: `meross-ble`. Import name: `meross_ble`.

## Supported models

| Model | Connection | Notes |
|-------|------------|--------|
| MS120 | Bluetooth | Temperature and humidity |
| MS220 | Bluetooth | Door / window, vibration, doorbell / button |
| MS700 | Bluetooth | Multi-button remote, temperature and humidity |
| MS420 | Bluetooth | Water leak / rain |

## Install

```bash
pip install meross-ble
```

Until published to PyPI:

```bash
pip install -e D:\workspace\meross-ble
```

Home Assistant custom component (`meross_rpc`) should use:

```bash
hass --skip-pip-packages meross_ble
```

after an editable install.

## Usage

```python
from meross_ble import (
    MerossModel,
    create_device,
    parse_advertisement_data,
)

adv = parse_advertisement_data(ble_device, advertisement_data)
if adv is None:
    return

device = create_device(ble_device, adv.model)
device.update_from_advertisement(adv)

device.bind_runtime(
    refresh_ble_device=lambda: ble_device,
    gatt_lock=gatt_lock,
    wait_advertisement=wait_next_advertisement,
    inspect_ble_cache=optional_host_cache_dump,
)
await device.identify()
```

## GATT recovery (v0.2)

Matches the latest `meross_rpc` BLE path:

- settle `GATT_POST_CONNECT_SETTLE` after connect
- same-connection rediscover (`GATT_REDISCOVER_SETTLE`) before `RemoveDevice`
- at most one BlueZ `clear_cache` per identify/history operation
- `GATT_NOTIFY_TIMEOUT` for Notify ACKs

## Layout

| Module | Role |
|--------|------|
| `meross_ble.parser` | BLE advertisement parse |
| `meross_ble.protocol` | TLV frames, CRC, history decode |
| `meross_ble.device` | Device state + GATT Identify / heartbeat / history |
| `meross_ble.psychrometrics` | Dew point, absolute humidity, VPD |

## Publish to PyPI

1. Create a PyPI project and GitHub Trusted Publisher for this repo
2. Tag a release: `git tag v0.2.0 && git push --tags`
3. The `publish` workflow uploads sdist + wheel
