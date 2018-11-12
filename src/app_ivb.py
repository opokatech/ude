

def get_ivb_xml(a_params):
    try:
        import usocket as socket
    except:
        import socket

    try:
        import ussl as ssl
    except:
        import ssl

    host = "www.ivb.at"
    port = 443
    script = "/smartinfo/ivb_smartinfo_kernel.php"

    content = "&".join(["{}={}".format(k, v) for (k, v) in a_params.items()])
    #print(content)

    msg = """\
POST {}?{} HTTP/1.1\r\n\
Host: {}\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Content-Length: 0\r\n\
Connection: close\r\n\
User-Agent: esp8266\r\n\r\n""".format(script, content, host)

    # print(msg)

    ai = socket.getaddrinfo(host, port)
    addr = ai[0][-1]

    s = socket.socket()
    s.connect(addr)

    s = ssl.wrap_socket(s)
    s.write(msg)
    # print("request sent...")

    # read the headers
    # s = s.makefile()
    while True:
        h = s.readline()
        if h == b"" or h == b"\r\n":
            break
        # print(h)

    # read the rest - assuming it will be less than 4096

    content = s.read(4096)
    s.close()
    # print(content)
    return content


def extract_bus_plan(a_xml):
    import xmltok
    import uio

    smart_info = []
    stack = []
    si_tmp = {}

    c = uio.StringIO(a_xml)
    g = xmltok.tokenize(c)

    # somehow "for token in g:" is not working (exception StopIteration stops the execution)
    while True:
        try:
            token = next(g)
        except:
            break

        # print(token)
        if len(token) < 2:
            continue

        token_type = token[0]
        token_value = token[1]
        if token_type == "START_TAG":
            token_name = token_value[1]
            stack.append(token_name)
            if token_name == 'smartinfo':
                # print("starting", token)
                si_tmp = {}
        elif token_type == "TEXT":
            if len(stack) > 2:
                # print("text", token)
                token_name = stack[-1]
                si_tmp[token_name] = token_value
        elif token_type == "END_TAG":
            closing_tag = stack.pop()
            if closing_tag == 'smartinfo':
                # print("closing", token)
                # print(si_tmp)
                smart_info.append(si_tmp)

    return smart_info


def main():
    from machine import Signal, Pin, freq
    import hwconfig
    import time
    import gc

    btn_fetch = Signal(hwconfig.D6, Pin.IN, Pin.PULL_UP, invert=True)
    btn_turbo = Signal(hwconfig.D5, Pin.IN, Pin.PULL_UP, invert=True)
    blue_led = Signal(hwconfig.LED_BLUE, Pin.OUT, invert=True)
    red_led = Signal(hwconfig.LED_RED, Pin.OUT, invert=True)

    print("Connect D6 to GND to fetch data")
    print("Keep D5 pressed to speed up clock")
    while True:
        if btn_fetch.value():
            print("fetching")
            params = {
                "stopId": "Technik",
                "optDir": -1,
                "nRows": 4,
                "showArrivals": "n",
                "optTime": "now",
                "allLines": "y"
            }

            red_led.on()
            time_fetch = time.ticks_ms()
            xml = get_ivb_xml(params)
            time_fetch = time.ticks_diff(time.ticks_ms(), time_fetch)
            red_led.off()

            gc.collect()

            blue_led.on()
            speed_up = btn_turbo.value()
            if speed_up:
                freq(160000000)
                print("speeding up")
            time_parse = time.ticks_ms()
            smart_info = extract_bus_plan(xml)
            time_parse = time.ticks_diff(time.ticks_ms(), time_parse)
            if speed_up:
                freq(80000000)
            blue_led.off()

            gc.collect()
            print(smart_info)
            print("fetched in {} ms, parsed in {} ms".format(time_fetch, time_parse))

        gc.collect()
        time.sleep_ms(100)


if __name__ == "__main__":
    main()

    # print("getting xml...")

    #params = {
    #    "stopId": "Technik",
    #    "optDir": -1,
    #    "nRows": 4,
    #    "showArrivals": "n",
    #    "optTime": "now",
    #    "allLines": "y"
    #}

    #xml = get_ivb_xml(params)

    #print(xml)

    # used for debug
    # content='<?xml version="1.0" encoding="utf-8"?><ivbsmartinfo output="timetable" version="Compatibity Version 1.0"><smartinfo><route>T</route><direction>Völs EKZ Cyta</direction><time>0 min</time></smartinfo><smartinfo><route>O</route><direction>J. Kerschb. Str.</direction><time>1 min</time></smartinfo><smartinfo><route>T</route><direction>Rum Kaplanstraße</direction><time>2 min</time></smartinfo><smartinfo><route>3</route><direction>Peerhofsiedlung</direction><time>3 min</time></smartinfo><linedirections route="3" direction="Peerhofsiedlung" dirforrequest="Peerhofsiedlung"/><linedirections route="O" direction="J. Kerschb. Str." dirforrequest="J.*Kerschb.*Str."/><linedirections route="T" direction="Völs EKZ Cyta" dirforrequest="V*o*ls*EKZ*Cyta"/><linedirections route="T" direction="Rum Kaplanstraße" dirforrequest="Rum*Kaplanstra*s*e"/><stopidname>Technik</stopidname></ivbsmartinfo>'

    #print("parsing xml")
    #smart_info = extract_bus_plan(xml)
    #print(smart_info)
