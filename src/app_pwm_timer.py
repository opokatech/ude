from machine import PWM, Timer, Pin
import hwconfig
import time

# led = Pin(hwconfig.LED_BLUE, Pin.OUT, value=1)
led = Pin(hwconfig.D7, Pin.OUT, value=1)
led_pwm = PWM(led)

led_duty = 0
delta = 64
timer = None

def update_led(a_timer):
    global led_duty, delta
    led_duty += delta

    if led_duty >= 1024:
        delta = -delta
        led_duty = 1023
    elif led_duty < 0:
        delta = -delta
        led_duty = 0

    # print("duty: {}".format(led_duty))
    led_pwm.duty(led_duty)


def main():
    global timer
    timer = Timer(-1)
    timer.init(period=50, mode=Timer.PERIODIC, callback=update_led)

    print("when you are done wathing LED fade in/out - call finish from this module")
    while True:
        time.sleep(2)


def finish():
    if timer is not None:
        timer.deinit()

    led_pwm.deinit()
    led.off()


if __name__ == "__main__":
    main()


