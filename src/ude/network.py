from machine import Pin, Signal
import network
import time
import ujson
import uos

class Wifi:
    WIFI_CFG_FILE = "wifi.cfg"
    AP = "ap"
    STA = "sta"

    def __init__(self):
        self.ap_if = network.WLAN(network.AP_IF)
        self.sta_if = network.WLAN(network.STA_IF)


    def remove_wifi_setup(self):
        """ Remove configuration file.
        """
        try:
            uos.remove(self.WIFI_CFG_FILE)
            print("WIFI configuration removed")
        except:
            print("File {} not found".format(self.WIFI_CFG_FILE))


    def get_configuration(self):
        """ Gets the configuration as a dict.
        It makes sure that it always gets AP and STA fields even if not configuration file
        was found or the name or password were not found.
        """
        f = None
        try:
            f = open(self.WIFI_CFG_FILE, "r")
            content = ujson.load(f)
        except:
            # print("Can't open {} for reading".format(self.WIFI_CFG_FILE))
            content = ujson.loads('{}')

        if f is not None:
            f.close()

        # sanitize json
        for what in (self.AP, self.STA):
            if what in content:
                # if either name or password are not there or empty - then remove it completely
                if not content[what].get("name") or not content[what].get("password"):
                    content[what] = {}
            else:
                content[what] = {}

        return content


    def setup_sta(self, a_name, a_password):
        """ Sets up WIFI STA interface with a name and a password.
        If either a_name or a_password is None - then STA interface will be disabled.
        """
        self._setup(self.STA, a_name, a_password)


    def setup_ap(self, a_name, a_password):
        """ Sets up WIFI AP interface with a name and a password.
        If either a_name or a_password is None - then AP interface will be disabled.
        """
        self._setup(self.AP, a_name, a_password)


    def _setup(self, a_what, a_name, a_password):

        if a_what in (self.AP, self.STA):
            what = a_what.upper()
            print("Configuring WIFI {}".format(what))

            content = self.get_configuration()

            try:
                f = open(self.WIFI_CFG_FILE, "w")
            except:
                print("Can't open file {} for writing - exiting".format(WIFI_CFG_FILE))
                return

            if a_name is not None and a_password is not None:
                print("Saving name and password for {}".format(what))
                content[a_what]["name"] = a_name
                content[a_what]["password"] = a_password
            else:
                print("Clearing name and password for {}".format(what))
                content[a_what] = {}

            try:
                ujson.dump(content, f)
                print("Configuration for {} saved".format(what))
            except:
                print("Error dumping json to file")
            finally:
                f.close()
        else:
            print("Unknown action {}".format(a_what))


    def connect(self):
        """
        Sets up the networking using wifi configuration file.
        """

        # it should be already in sanitized form - so values are there if configured
        cfg = self.get_configuration()
        cfg_ap = cfg[self.AP]
        cfg_sta = cfg[self.STA]

        if cfg_ap:
            print("Configured access point {}".format(cfg_ap["name"]))
            try:
                self.ap_if.config(essid=cfg_ap["name"], authmode=network.AUTH_WPA_WPA2_PSK, password=cfg_ap["password"])
                self.ap_if.active(True)
            except:
                print("Configuring AP failed - maybe password is too short")
                self.ap_if.active(False)
        else:
            print("Disabled access point")
            self.ap_if.active(False)

        if cfg_sta:
            print("Configured wifi client for {}".format(cfg_sta["name"]))

            self.sta_if.active(True)
            self.sta_if.connect(cfg_sta["name"], cfg_sta["password"])
            self._wait_for_sta_connection(cfg_sta["name"])
        else:
            print("Disabled wifi client")
            self.sta_if.active(False)


    def _if_status_string(self, a_status):
        if a_status == network.STAT_CONNECTING:
            return "connecting"
        elif a_status == network.STAT_WRONG_PASSWORD:
            return "wrong password"
        elif a_status == network.STAT_NO_AP_FOUND:
            return "network not found"
        elif a_status == network.STAT_CONNECT_FAIL:
            return "connection failed"
        elif a_status == network.STAT_GOT_IP:
            return "got IP"


    def _connecting_finished(self, a_status):
        return a_status in (network.STAT_WRONG_PASSWORD, network.STAT_NO_AP_FOUND, network.STAT_CONNECT_FAIL,
                network.STAT_GOT_IP)


    def _wait_for_sta_connection(self, a_sta_name):
        status_led = Signal(Pin(2, Pin.OUT), invert=True)

        MAX_CONNECT_TIME_MS = 20000
        start = time.ticks_ms()
        deadline = start + MAX_CONNECT_TIME_MS

        now = start
        print("connecting to wifi '{}' ...".format(a_sta_name))
        status = 0
        while now < deadline:
            new_status = self.sta_if.status()
            if new_status != status:
                status = new_status
                print("status: {}".format(self._if_status_string(status)))

                if self._connecting_finished(status):
                    break

            time.sleep_ms(50)
            now = time.ticks_ms()
            status_led.value(not status_led.value())

        if self.sta_if.isconnected():
            print("DONE (finished in {} ms)".format(now-start))
            print(self.sta_if.ifconfig())
            status_led.on()
            time.sleep_ms(500)
        else:
            print("FAILED (finished in {} ms)".format(now-start))

        status_led.off()


def connect():
    w = Wifi()
    w.connect()

