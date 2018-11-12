try:
    import usocket as socket
except:
    import socket

try:
    import ujson as json
except:
    import json

from machine import Pin, Signal
import hwconfig
import gc
import sys


class Demo:
    def __init__(self):
        """ Creates pins for use later."""
        # pins to use - just names from hwconfig
        self.pins_pullup = ["D{}".format(i) for i in (5, 6, 7)] # pin supporting pull up (connect to GND for change)
        self.pins_out = ["LED_RED", "LED_BLUE"]

        # objects to use
        self.pv_pullup = [(name, Signal(eval("hwconfig.{}".format(name)), Pin.IN, Pin.PULL_UP, invert=True)) for name in self.pins_pullup]
        self.pv_in = []
        self.pv_out = [(name, Signal(eval("hwconfig.{}".format(name)), Pin.OUT, invert=True)) for name in self.pins_out]


    def build_response(self):
        """ Creates full http answer (including content type).
        """
        status = {}
        status["pins"] = {}
        status["pins"]["pullup"] = [{"name": e[0], "value": e[1].value()} for e in self.pv_pullup]
        status["pins"]["in"] = [{"name": e[0], "value": e[1].value()} for e in self.pv_in]
        status["pins"]["out"] = [{"name": e[0], "value": e[1].value()} for e in self.pv_out]
        status["gc"] = {"enabled": gc.isenabled(), "mem_free": gc.mem_free() }
        status["sys"] = {}
        status["sys"] = {
            "platform": sys.platform,
            "implementation": sys.implementation[0],
            "version": sys.version
        }

        output = b"""\
HTTP/1.0 200 OK
Server: esp8266
Content-type: application/json;charset=utf-8

"""
        output += json.dumps(status)

        return output


    def get_query_params(self, a_req):
        """
        Returns a dictionary with params passed as query string.
        Subsequent use of value overwrites previous one.
        """

        req_words = a_req.split(b' ')

        if len(req_words) < 3:
            return {}

        url = req_words[1]
        qm_pos = url.find(b"?")

        if qm_pos == -1:
            return {}

        qs = url[qm_pos + 1:]

        result = {}
        params = qs.split(b"&")
        for param in qs.split(b"&"):
            key_value = param.split(b"=")
            if len(key_value) == 2:
                result[key_value[0]] = key_value[1]

        # print(b'query params', result)
        return result


    def set_outputs(self, a_params):
        """ It processes parameters given as a dictionary of "output_name": "value".
        "output_name" must exist in self.pins_out and "value" must be either 0 or 1.
        """

        for output, value in a_params.items():
            if output.decode() in self.pins_out and value.decode() in ("0", "1"):
                pin = Signal(eval("hwconfig." + output.decode()), Pin.OUT, invert=True)
                pin.value(int(value))
            else:
                print("not using {}={}".format(output, value))


    def main(self):
        s = socket.socket()

        ai = socket.getaddrinfo("0.0.0.0", 80)
        print("Bind address info:", ai)
        addr = ai[0][-1]

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)

        while True:
            res = s.accept()
            client_sock = res[0]
            client_addr = res[1]
            print("Client address:", client_addr)
            print("Client socket:", client_sock)

            client_stream = client_sock

            print("Request:")
            req = client_stream.readline()
            print(req)
            if req.lower().startswith(b"get /"):
                params = self.get_query_params(req)

                print("params", params)
                self.set_outputs(params)

            # read the headers
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(h)


            # send answer
            client_stream.write(self.build_response())

            client_stream.close()
            client_sock.close()
            print()


def main():
    d = Demo()
    d.main()

if __name__ == "__main__":
    main()
