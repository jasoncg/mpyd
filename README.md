mpyd
====

mpyd is a simple web interface for controlling MPD.

Web server commands:
/                             Display current playlist
/status/currentsong           Display current song
/control/play?ID              Play the specified song (ID is the index into t$
/control/pause                Toggle pause
/control/next                 Go to next song
/control/previous             Go to previous song

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
