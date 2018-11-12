def set_ntp_time(a_offset = 0):
    """ Set time using NTP and given offset in seconds.

    The board does not support timezones, so time.localtime() will return UTC time.
    If real local time needs to be used then a_offset should be considered (in seconds).
    """
    import ntptime
    import machine
    import utime

    t = ntptime.time() + a_offset
    tm = utime.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)

