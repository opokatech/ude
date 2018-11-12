def main():
    from machine import Pin, Signal
    import time
    import hwconfig

    def toggle(aPin):
        aPin.value(not aPin.value())

    red = Signal(hwconfig.LED_RED, Pin.OUT, value=1, invert=True)
    blue = Signal(hwconfig.LED_BLUE, Pin.OUT, invert=True)

    do_measure = Signal(hwconfig.D5, Pin.IN, Pin.PULL_UP, invert=True)

    last_time = time.ticks_ms()
    cnt = 0

    print("If D5 is off then it just toggles 2 leds.")
    print("If D5 is on then it toggles 2 leds as fast as it can and measures time")
    while True:
        toggle(red)
        toggle(blue)

        if do_measure.value():
            cnt += 1
            now = time.ticks_ms()
            delta = time.ticks_diff(now, last_time)
            if delta > 1000:
                print("toggled 2 pins: {}/s".format(cnt * 1000 / delta))
                cnt = 0
                last_time = time.ticks_ms()
        else:
            time.sleep_ms(50)


def finish():
    from machine import Pin, Signal
    import hwconfig

    red = Signal(hwconfig.LED_RED, Pin.OUT, invert=True)
    blue = Signal(hwconfig.LED_BLUE, Pin.OUT, invert=True)


if __name__ == "__main__":
    main()
