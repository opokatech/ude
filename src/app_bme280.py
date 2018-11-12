from BME280 import BME280
from machine import I2C, Pin, Signal
import hwconfig
import time

try:
    import usocket as socket
except:
    import socket

try:
    import ussl as ssl
except:
    import ssl


def upload_to_thingspeak(a_data, a_led):
    """ Upload a dictionary to thingspeak.com.
    """

    HOST = "api.thingspeak.com"
    PORT = 443

    # content = b"&".join([b"{}={}".format(k, v) for (k, v) in a_data.items()])
    # print(content)
    # it seems that api_key must be first...
    content = "&".join(["{}={}".format(k, a_data[k]) for k in sorted(a_data.keys())])
    msg = """\
POST /update.json HTTP/1.1\r\n\
Host: {}\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Content-Length: {}\r\n\r\n\
{}""".format(HOST, len(content), content)

    #print(msg)
    #return

    a_led.on()

    ai = socket.getaddrinfo(HOST, PORT)
    addr = ai[0][-1]

    s = socket.socket()
    s.connect(addr)

    s = ssl.wrap_socket(s)
    s.write(msg)
    print("request sent...")

    # read the headers
    # b'Status: 200 OK\r\n'
    while True:
        h = s.readline()
        if h == b"" or h == b"\r\n":
            break

        status_prefix = b"Status: "
        if h.startswith(status_prefix):
            fields = h.split(b" ")
            if len(fields) > 2 and fields[1] == b"200":
                print("transfer OK")

        # print(h)

    # print(s.read(4096))

    s.close()
    a_led.off()


def main():
    # prepare bme device
    i2c = I2C(scl=Pin(hwconfig.D1),sda=Pin(hwconfig.D2))
    bme = BME280(i2c=i2c)

    # inputs
    switch_name = "D5"
    button = Signal(hwconfig.BTN_USER, Pin.IN, invert=True)
    switch = Signal(eval("hwconfig." + switch_name), Pin.IN, Pin.PULL_UP, invert=True)

    # outputs
    led = Signal(hwconfig.LED_BLUE, Pin.OUT, invert=True)

    # load thingspeak api key
    thingspeak_cfg = "thingspeak.cfg"

    try:
        f = open(thingspeak_cfg, "r")
        api_key = f.read()
        api_key = api_key.strip()
        f.close()
    except:
        print("error reading api key from {}".format(thingspeak_cfg))
        api_key = None

    print("Press USER button to see values. Press {} to upload to thingspeak.com".format(switch_name))

    upload_interval_s = 1
    last_upload_time = 0

    while True:
        t, h, p = (bme.temperature, bme.humidity, bme.pressure)
        tv = float(t.replace("C", ""))
        hv = float(h.replace("%", ""))
        pv = float(p.replace("hPa", ""))

        if button.value():
            print(t, p, h)

        now = time.time()
        if switch.value():
            print(t, p, h)
            if api_key is not None:
                if now - last_upload_time > upload_interval_s:
                    print("uploading...")
                    data = { "api_key": api_key, "field1": tv, "field2": hv, "field3": pv}
                    upload_to_thingspeak(data, led)

                    last_upload_time = now
                else:
                    print("you are too quick...")
            else:
                print("not uploading. Save api key in {}".format(thingspeak_cfg))

        time.sleep_ms(100)


if __name__ == "__main__":
    main()
