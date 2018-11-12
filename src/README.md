# Scripts

This directory contains example applications (`app_*`) and some utility files (`hwconfig.py`, `ude/*`).

Use 'upload.sh` for uploading either applications or ude files or a single files.

## ude.network

Use can use it like so:

```
>>> import ude.network

>>> w = ude.network.Wifi()
>>> w.setup_ap('esp8266', 'demopassword') # saves parameters for access point (name, password)
Configuring WIFI AP
Saving name and password for AP
Configuration for AP saved

>>> w.setup_sta(None, None) # saves parameters for wifi client
Configuring WIFI STA
Clearing name and password for STA
Configuration for STA saved

>>> w.get_configuration()
{'ap': {'name': 'esp8266', 'password': 'demopassword'}, 'sta': {}}

>>> w.connect()
Configured access point esp8266
#21 ets_task(4020f4ac, 29, 3fff8c70, 10)
Disabled wifi client

>>> w.ap_if.ifconfig()
('192.168.4.1', '255.255.255.0', '192.168.4.1', '195.34.133.21')

# Now we can access the device at access point 'esp8266' with the password above.

>>> w.setup_sta('mynet', 'mypass')
Configuring WIFI STA
Saving name and password for STA
Configuration for STA saved

>>> w.connect()
Configured access point esp8266
Configured wifi client for mynet
#22 ets_task(4020f474, 28, 3fff9190, 10)
connecting to wifi 'mynet' ...
status: connecting
status: got IP
DONE (finished in 6185 ms)
('10.201.111.52', '255.255.255.0', '10.201.111.1', '195.34.133.21')

```

## ude.apps

This is used from `main.py` to scan for installed applications and allow user (interactively) to select one to run.
This was made for the presentation only - not for production.

```
>>> import ude.apps

>>> ude.apps.main()
Found 7 application(s):
1 -> app_ivb.py
2 -> app_pin_changed_irq.py
3 -> app_toggle_pin.py
4 -> app_http_status.py
5 -> app_chat.py
6 -> app_bme280.py
7 -> app_pwm_timer.py
To make an app automatically started - save its name to default_app.txt
To turn off automatic start of an app - remove default_app.txt
Select application (by number) to run or 0 to skip:
Your choice >
```

An application should have `main()` which gets executed. It may optionally have `finish()` which gets executed when user
presses `CTRL-C`.

You may want to set some app to start automatically:
```
>>> ude.apps.set_default('app_pwm_timer.py')
Default app saved
```

Next time the `ude.apps.main()` gets called - it will executed what was set as default.
To clear the default use
```
>>> ude.apps.remove_default()
Default app starting - removed
```

## ude.utils

Examples:
```
>>> import time
>>> import ude.utils
>>> time.localtime()
(2000, 1, 1, 0, 0, 23, 5, 1)
>>> ude.utils.set_ntp_time(3600) # timezone offset given in seconds - if not given it is 0 and then localtime will be in UTC
>>> time.localtime()
(2018, 11, 12, 11, 37, 7, 0, 316)
```


