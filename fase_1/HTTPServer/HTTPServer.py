#!/usr/bin/python

import SimpleHTTPServer
import os

if __name__ == '__main__':
	#os.system("cd HTTPServer")
	os.system("python -m SimpleHTTPServer 8000")
	serve_forever()

