About
=====

Tiny python script to change NetworkManager DNS servers via the DBus interface.

Example
-------

    $ sudo ./nm_change_dns.py 127.0.0.1
    Current configuration:
    8.8.8.8
    8.8.4.4
    New configuration:
    127.0.0.1
    Apply change? [y/N] y
    
    $ dbus-send --system --print-reply --dest=org.freedesktop.NetworkManager \
      /org/freedesktop/NetworkManager/Settings/0 \
      org.freedesktop.NetworkManager.Settings.Connection.GetSettings | \
      grep dns -B1 -A5
    
            dict entry(
               string "dns"
               variant                   array [
                     uint32 16777343
                  ]
            )
    
    $ export X=16777343
    $ echo "$((X%256)).$(((X>>8)%256)).$(((X>>16)%256)).$((X>>24))"
    127.0.0.1


Credits
-------

Derived from this article's code:
http://www.kernelcrash.com/blog/updating-networkmanager-via-the-command-line/2012/04/01/
