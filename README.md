# aiomeross-ble

Python library for [Meross](https://www.meross.com/) Bluetooth devices. Protocol, advertisement parsing, and GATT helpers live here so Home Assistant (and other projects) only deal with entities and coordinators.

This package has **no Home Assistant dependency**.

## Supported models

| Model | Connection | Notes |
|-------|------------|--------|
| MS120 | Bluetooth | Temperature and humidity |
| MS220 | Bluetooth | Door / window, vibration, doorbell / button |
| MS700 | Bluetooth | Multi-button remote, temperature and humidity |
| MS420 | Bluetooth | Water leak / rain |

## Install

```bash
pip install aiomeross-ble
```

Until this is published to PyPI, install from the repo:

```bash
pip install -e D:\workspace\meross-ha
```

Home Assistant custom component (`meross_rpc`) should be started with:

```bash
hass --skip-pip-packages aiomeross-ble
```

after an editable install, so HA does not overwrite the local checkout.

## Usage

```python
from aiomeross_ble import (
    MerossModel,
    create_device,
    parse_advertisement_data,
)

adv = parse_advertisement_data(ble_device, advertisement_data)
if adv is None:
    return

device = create_device(ble_device, adv.model)
device.update_from_advertisement(adv)
print(device.data)

# Optional: host supplies BLEDevice refresh + shared GATT lock
device.bind_runtime(
    refresh_ble_device=lambda: ble_device,
    gatt_lock=gatt_lock,
    wait_advertisement=wait_next_advertisement,
)
await device.identify()
```

## Layout

| Module | Role |
|--------|------|
| `aiomeross_ble.parser` | BLE advertisement parse |
| `aiomeross_ble.protocol` | TLV frames, CRC, history decode |
| `aiomeross_ble.device` | Device state + GATT Identify / heartbeat / history |
| `aiomeross_ble.psychrometrics` | Dew point, absolute humidity, VPD |

## Publish to PyPI

1. Create a PyPI project and GitHub Trusted Publisher for this repo
2. Tag a release: `git tag v0.1.0 && git push --tags`
3. The `publish` workflow uploads sdist + wheel

Home Assistant Core requires source distributions, OSI license, issue tracker, and automated PyPI publishing.
