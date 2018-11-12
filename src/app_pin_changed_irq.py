def main():
    from machine import Pin
    import hwconfig
    import micropython

    def do_something(p):
        print("pin changed -> {}".format(p.value()))

    def callback(p):
        micropython.schedule(do_something, p)
        # print("pin changed", p)

    print("Any change of D5 will trigger a callback")
    p = Pin(hwconfig.D5, Pin.IN, Pin.PULL_UP)
    p.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)


if __name__ == "__main__":
    main()
