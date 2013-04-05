#!/usr/bin/python
#
# Cleaned up Apr 2013 by Conrad Meyer
#
# My modifications are released under the terms of the MIT license
#
# Derived from
# http://www.kernelcrash.com/blog/updating-networkmanager-via-the-command-line/2012/04/01/
# with no explicit license (but I would guess from the tone of the content that
# use and modification is permitted). If you are the author of this article and
# deny modification, re-use, distribution, etc, please let me know and I will
# destroy this and all copies as soon as possible -CEM.

import dbus
import socket
import struct
import sys

# XXX: Apparently NM stores IPs little-endian, or else python's socket library
# does that.

def dottedQuadToNum(ip):
    "convert decimal dotted quad string to long integer"
    return struct.unpack('<L', socket.inet_aton(ip))[0]


def uintToDottedQuad(uip):
    "convert uint32 to string ip"
    return socket.inet_ntoa(struct.pack('<L', int(uip)))


def main():
    if len(sys.argv) < 2:
        sys.exit("Must supply ip address(es) for dns; eg. 192.168.0.1 [...]")

    xs = [dottedQuadToNum(x) for x in sys.argv[1:]]
    bus = dbus.SystemBus()

    # XXX hardcoded. If your settings is a different one you may have to change
    # this
    proxy = bus.get_object("org.freedesktop.NetworkManager",
            "/org/freedesktop/NetworkManager/Settings/0")
    
    settings = dbus.Interface(proxy,
            "org.freedesktop.NetworkManager.Settings.Connection")
    
    config = settings.GetSettings()
    s_ipv4 = config['ipv4']

    print "Current configuration:"
    for curdns in s_ipv4['dns']:
        print uintToDottedQuad(int(curdns))

    print "New configuration:"
    for x in sys.argv[1:]:
        print x

    cont = raw_input("Apply change? [y/N] ")
    if not cont.lower().startswith("y"):
        print "Aborting"
        sys.exit(0)

    s_ipv4['dns'] = dbus.Array([dbus.UInt32(x) for x in xs],
            signature=dbus.Signature('u'), variant_level=1)
    settings.Update(config)
    
if __name__ == "__main__":
    main()
