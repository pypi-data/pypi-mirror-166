# pytrutankless

Python interface for TRUTANKLESS branded water heaters

## Installation

```
pip install pytrutankless
```

## Usage

```python
from pytrutankles.api import TruTanklessApiInterface

email = "your_email"
password = "your_password"

api = await TruTanklessApiInterface.login(email, password)
```

### Methods

### `login(email, password)`

```
api.login(email, password)
```

Given email and password, logs into service and retrieves `access_token`

### `get_devices()`

```
api.get_devices()
```

Updates list of locations and devices. Returns dictionary of device objects.

### `refresh_device(device_id)`

```
api.refresh_device(device_id)
```

Given `device_id`, updates usage data for that device.
