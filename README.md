# AMDGPU-ZERODB

A 0dB service for the `AMDGPU` kernel module.

Since the zero RPM fan mode doesn't always properly work with `AMDGPU` kernel module, even when the GPU BIOS supports it (RX580 Nitro, ROG RX580), this service manually monitors GPU temperature via `hwmon3` and manually switches fan control from automatic to zero RPM, based on your configuration.

## WARNING

Disabling fans can potentially damage your hardware depending on your GPU type, cooling requirements and your configuration.

**By using this software you take full responsibility for the potential damage caused to your hardware.**

## Configuration

Edit `/etc/amdgpu-zerodb.conf`:

```ini
[MAIN]
# Delay between checking the temperature in seconds
REFRESH_DELAY = 1

[TEMPERATURES]
# Peak temperature in C while fans are disabled
MAX_TEMP = 55
# Minimal temperature in C while fans are active (after hitting MAX_TEMP)
MIN_TEMP = 45
```

## Running

Execute `systemctl start amdgpu-zerodb.service` to start the daemon.

Optionally you can execute `systemctl enable amdgpu-zerodb.service` to automatically start the service after a reboot.

Make sure to do a test run and check logs with `journalctl --unit amdgpu-zerodb.service` before enabling the service.

## License

Copyright © 2018, [Ruben Harutyunyan](https://github.com/Vagr9K/). Released under [GPLv3 license](./LICENSE).
