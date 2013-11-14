#!/usr/bin/env python
# mpyd.py
# 2013-11-11 jasoncg
#
# A very simple web-based MPD client.  
# For usage,
# $ python mpyd.py -h		
#
# Web server commands:
# /				Display current playlist
# /status/currentsong		Display current song
# /control/play?ID		Play the specified song (ID is the index into the current playlist)
# /control/pause		Toggle pause
# /control/next				Go to next song
# /control/previous		Go to previous song
#
# Possible future todo:
#		Better code organization
#		Update database
#		Playlist select
#		Playlist manipulation
#		File browser
#

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#from http.server import BaseHTTPRequestHandler, HTTPServer
import os, sys, mpd, argparse, base64
from pprint import pprint

args=None
mpdclient=None

#Create custom HTTPRequestHandler class
class MpydHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_HEAD(self):
		print("send header")
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_AUTHHEAD(self):
		print("send header")
		self.send_response(401)
		self.send_header('WWW-Authenticate', 'Basic realm=\"Login Required\"')
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def sendResponse(self, text):
		#send code 200 response
		self.send_response(200)
		#send header first
		self.send_header('Content-type','text/html')
		self.end_headers()
		#send file content to client
		self.wfile.write('<html><body>')
		self.wfile.write(text)
		print(text)

	#handle GET command
	def do_GET(self):
			global args
			#global mpdclient
			#Attempt to connect to MPD server
			try:
				print('Connect to MPD Server: '+args.mpdhost+':'+args.mpdport)
				mpdclient = mpd.MPDClient(use_unicode=True)
				mpdclient.connect(args.mpdhost, int(args.mpdport))
			except:
				print("Unexpected error:", sys.exc_info()[0])
				self.sendResponse('Unable to connect to MPD.  MPD Server may be offline.')
				return
			
			#if(self.headers.getheader('Authorization')!=None):
			#	print('Auth: '+self.headers.getheader('Authorization'))

			if(args.user!=None):
				if self.headers.getheader('Authorization')==('Basic '+base64.b64encode(args.user+':'+args.password)):
						#self.do_HEAD()
						print('auth OK')
				else: #self.headers.getheader('Authorization')==None:
						self.do_AUTHHEAD()
						self.wfile.write('no auth header')
						return
						
			#else:
			#		self.do_HEAD()

			print('Get Request')
			#pprint(self)

			pprint(self.path.split('?'))

			getPath=self.path.split('?')

			if getPath[0]=='/':
				self.sendResponse('Index')		
				self.wfile.write('<ol>')
				count=1
				for song in mpdclient.playlistinfo():
						self.wfile.write('<li>')
#						print(count+' '+mpdclient.currentsong()['id'])
						if((count-1)==int(mpdclient.currentsong()['id'])):
								self.wfile.write('*** ')

						songTitle=(song['album']+' - '+song['title'])
						#.encode('utf-8').strip()

						url='<a href="/control/play?'+str(count)+'">'+songTitle+'</a>'
						#+'['+song['time']+']' #+song["file"]

						self.wfile.write(url.encode('utf-8').strip())
						self.wfile.write('</li>')
						count+=1
				self.wfile.write('</ol>')		

				#for entry in mpdclient.lsinfo("/"):
				#		self.wfile.write("%s" % entry)
				#for key, value in mpdclient.status().items():
				#		self.wfile.write("%s: %s" % (key, value))
			elif getPath[0]=='/status/currentsong':
				c=mpdclient.currentsong()
				self.sendResponse(c)
			elif getPath[0]=='/control/play':
				if(len(getPath)>1):
						self.sendResponse('play '+getPath[1])
						mpdclient.play((int(getPath[1])-1))
				else:
						#send file content to client
						self.sendResponse('play')
						mpdclient.play()
			elif getPath[0]=='/control/pause':
				self.sendResponse('pause')
				mpdclient.pause()
			elif getPath[0]=='/control/next':
				self.sendResponse('next')
				mpdclient.next()
			elif getPath[0]=='/control/previous':
				self.sendResponse('previous')
				mpdclient.previous()
			else:
				self.send_response(404)
				self.send_header('Content-type','text-html')
				self.end_headers()
				#send file content to client
				self.wfile.write("NOT Handled: Requested "+self.path)

			mpdclient.close()
			mpdclient.disconnect()

def main(argv):
		global mpdclient
		global args

		parser = argparse.ArgumentParser(description='Simple web-based MPD controller')
		#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')
		parser.add_argument('--mpdhost', dest='mpdhost', default='localhost', help='MPD server host or IP')
		parser.add_argument('--mpdport', dest='mpdport', default=6600, help='MPD server port')

		parser.add_argument('--httpdhost', dest='httpdhost', default='0.0.0.0', help='Web server interface/IP')
		parser.add_argument('--httpdport', dest='httpdport', default=8000, help='Web server port')

		parser.add_argument('--user', dest='user', default=None, help='Username for basic authentication')
		parser.add_argument('--pass', dest='password', default='', help='Password for basic authentication')

		args = parser.parse_args()

		try:
			print('Testing connection to MPD Server: '+args.mpdhost+':'+args.mpdport)
			mpdclient = mpd.MPDClient(use_unicode=True)
			mpdclient.connect(args.mpdhost, int(args.mpdport))

			mpdclient.close()
			mpdclient.disconnect()
		except:
			print('Unable to connect to MPD server')
			return
			
		print('http server is starting on '+args.httpdhost+':'+args.httpdport+' ...')

		httpd = HTTPServer((args.httpdhost, int(args.httpdport)), MpydHTTPRequestHandler)
		print('http server is running...')
		httpd.serve_forever()
	
if __name__ == '__main__':
	main(sys.argv[1:])
