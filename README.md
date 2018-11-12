# UDE

It stands for **u**Python **D**evelopment **E**nvironment. It utilizes existing tools from other repositories, adds some more files to make developing software for ESP8266 in python relatively painless.

## Getting started

### Preparing environment
First of all download all submodules:
```
git submodule --init --recursive
```

This will fetch:
* `esptool` which is needed for flashing firmware,
* `micropython` which contains `pyboard.py` used for running code on the hardware, `mpy-cross` compiler, and of course the whole source code if you would like to build your own firmware (for example with some more libraries)
* `esp-open-sdk` - this is cross compiler - needed only if you want to build own firmware versions
* `micropython-lib`, `micropython-dflib` - libraries that could be used for either copying them to the board or using them for freezing them in a firmware
* `mpfshell` - a tool for handling the file system of the hardware (upload, download files, etc.)

Run
```
./bin/mpfshell.sh
```
and follow instructions to install virtual environment.

Optional:

Go to `micropython/mpy-cross` and run `make` - to get mpy-cross compiler (needed only if you want to precompile python
code).

Add `bin` to your **PATH**.

### Preparing hardware

Download the firmware from [http://micropython.org/download#esp8266].

Use `esptool.py` to flash it (I assume you have the device connected at /dev/ttyUSB0)
```
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 <firmare.bin>
```

In `src` directory call `upload.sh`. It will use `mpfshell` to copy files to the board.

# Development

Write your code in a file and save it. To run your code on the hardware use:

```
pyboard.sh <file>
```
Notice the use of `pyboard.sh` instead of `pyboard.py` - the shell version is just a wrapper which uses `/dev/ttyUSB0` as default.

If you are happy with result you can use `mpfshell` to upload it to the hardware - either under own name or rename it to `main.py` and then it will get executed automatically at boot time.

The best way to explore the board is to experiment with it on its python console, you can access via usb:
`picocom -b 115200 /dev/ttyUSB0`
```
MicroPython v1.9.4-674-g27ca9ab8b on 2018-10-24; ESP module with ESP8266
Type "help()" for more information.
>>>
```
`help()` will be a good start.

`help('modules')` shows you all modules which are frozen in the firmware, i.e. they are available to you, but they are precompiled into the firmware and not visible as files. They work faster and don't use precious RAM. If you want some module be frozen you need to build your own firmware. It is described in details here: [https://docs.micropython.org/en/latest/reference/packages.html#cross-installing-packages-with-freezing]

Temporarily you can install needed libraries using `upip` using the console:
```
import upip
upip.install('micropython-pystone_lowmem')
```
The files will be dropped in `/lib` and can be imported and used as usual:
```
>> import pystone_lowmem
>>> pystone_lowmem.main()
Pystone(1.2) time for 500 passes = 1159ms
This machine benchmarks at 431 pystones/second
```
