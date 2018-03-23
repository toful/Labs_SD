#!/usr/bin/python

import resquests.sys

def iniServer(port, wd):
	os.chdir(wd)
	os.system("python -m SimpleHTTPServer")

if __name__ == '__main__':
	iniServer(sys.argv[1], "Input_Files")
	print 'Started httpserver on port ' , sys.argv[1]
