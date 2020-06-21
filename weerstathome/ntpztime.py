"""
Custom time keeping methods with timezone support
"""

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct


# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600


def time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    # https://docs.python.org/3/library/socket.html
    addr = socket.getaddrinfo("pool.ntp.org", 123)[0][-1]  # Can't fail?
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Can't fail?
    val = NTP_DELTA  # create a valid return value
    try:
        s.settimeout(1)
        s.sendto(NTP_QUERY, addr)  # critical point of failure
        msg = s.recv(48)
        val = struct.unpack("!I", msg[40:44])[0]  # must be inside try as well, if above fails
    except Exception as e:
        print(e)
    finally:
        s.close()
    return val - NTP_DELTA


# There's currently no timezone support in MicroPython, so
# utime.localtime() will return UTC time (as if it was .gmtime())
def settime(zs):
    print("Setting time...")
    t = time()
    if t != 0:  # catch if time was successful
        print("time success")
        import machine
        import utime
        tm = utime.localtime(t + zs)
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
        return True
    else:
        print("time failed")
        return False
