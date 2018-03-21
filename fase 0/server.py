'''
Remote server. SERVER
@author: Cristofol Dauden Esmel & Aleix Marine Tena
'''
from pyactor.context import set_context, create_host, serve_forever, sys, shutdown

if __name__ == "__main__":
	set_context()

	if len(sys.argv) >= 2:
		host = create_host('http://127.0.0.1:'+sys.argv[1]+'/')
		print 'host listening at port', sys.argv[1]
		serve_forever()
	else:
		print "ERROR: Port as a parameter needed";

	shutdown()