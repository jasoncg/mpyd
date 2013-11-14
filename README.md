mpyd
====

mpyd is a simple web interface for controlling MPD.  
Access can be protected with a username and password, but please note it is NOT encrypted!

Web server commands:

    /                             Display current playlist
    /status/currentsong           Display current song
    /control/play?ID              Play the specified song (ID is the index into t$
    /control/pause                Toggle pause
    /control/next                 Go to next song
    /control/previous             Go to previous song


Running

    usage: mpyd.py [-h] [--mpdhost MPDHOST] [--mpdport MPDPORT]
                   [--httpdhost HTTPDHOST] [--httpdport HTTPDPORT] [--user USER]
                   [--pass PASSWORD]

    Simple web-based MPD controller

    optional arguments:
      -h, --help            show this help message and exit
      --mpdhost MPDHOST     MPD server host or IP
      --mpdport MPDPORT     MPD server port
      --httpdhost HTTPDHOST Web server interface/IP
      --httpdport HTTPDPORT Web server port
      --user USER           Username for basic authentication
      --pass PASSWORD       Password for basic authentication

Example Usage

    # MPD server on same system, port 6600.  Run web server on port 8000 with username "william" and password "spam"
    $ ./mpyd.py --mpdhost 127.0.0.1 --mpdport 6600 --httpdhost 0.0.0.0 --httpdport 8000 --user william --pass spam

    # MPD server on 192.168.0.5 port 6600.  Run web server only locally (not available to other hosts on the network)
    $ ./mpyd.py --mpdhost 192.168.0.5 --mpdport 6600 --httpdhost 127.0.0.1 --httpdport 8000
    
