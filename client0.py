'''
Remote client. Client
@author: Cristofol Dauden Esmel & Aleix Marine Tena
'''
from pyactor.context import set_context, create_host, Host, sleep, shutdown, sys
from pyactor.exceptions import TimeoutError
from subprocess import call
import os, sys

'''class ReducerDecorator(Reducer):
    _ask = []

    def __init__(self):
        self.i = 0

    def getMapperOutput(self):
'''


class Mapper(object):
    _ask = ['wait_a_lot']
    _tell = ['start', 'mapFunction','setReducer']
    _ref = ['setReducer']

    def __init__(self, text):
        print 'Mapper started'
        self.result = {}
        self.text=text

    def mapFunction(self, k, v):
        # remove leading and trailing whitespace
        line = v.strip()
        # split the line into words
        words = line.split()
        # increase counters
        for word in words:
            if word in self.result:
                self.result[word] = self.result[word]+[1]
            else:
                self.result[word] = [1]
        print self.result
        return 0

    def wait_a_lot(self):
        sleep(2)
        return 'ok'

    def setReducer(self, reducer):
        self.reducer=reducer

    def start(self):
        i=0
        for line in self.text.split("\n"):
            self.mapFunction(i, line)
            i+=1
        self.reducer.getMapperOutput(self.result)



class Reducer(object):
    _ask = ['wait_a_lot']
    _tell = ['start', 'reduceFunction', 'getMapperOutput']

    def __init__(self, num_mappers):
        print 'Reducer started'
        self.result = {}
        self.mappers_output = []
        self.mappers_finished = 0
        self.num_mappers=num_mappers

    def reduceFunction(self):
        for word in self.result.keys():
            self.result[word] = sum(self.result[word])
        return 0

    def getMapperOutput(self, output):
        self.mappers_output.append(output)
        #print self.mappers_output
        self.mappers_finished+=1
        if(self.mappers_finished == self.num_mappers):
            self.start()

    def wait_a_lot(self):
        sleep(2)
        return 'ok'

    def start(self):
        for hashes in self.mappers_output:
            for key in hashes.keys():
                if key in self.result:
                    self.result[key] = self.result[key]+hashes[key]
                else:
                    self.result[key] = hashes[key]
        self.reduceFunction()
        print self.result

'''
This function splits file "filename" into "chunknum" pieces. This function returns a tuple with the output filenames.
TO-DO optimize function. Now generates charset.length ^ 2 but only chunknum is necessary
'''
def split(chunknum, filename, wd):
	f = open(wd+'/'+filename, 'r')
	os.system("split -n "+str(chunknum)+" "+filename) 
	charset = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
	filenames = ()
	for i in charset:
		for j in charset:
			filenames = filenames + ('x'+i+j,)

	return filenames[:chunknum]

if __name__ == "__main__":
	set_context()

	if len(sys.argv) >= 3:#5:
		num_mappers = len(sys.argv) - 3
		print num_mappers
		remote_hosts = ()
		mappers = ()

		wd = os.path.dirname(os.path.realpath(__file__))
		filenames = split(num_mappers, "input.txt", wd)
		host = create_host('http://127.0.0.1:'+sys.argv[1]+'/')

		#Getting the server proxy
		for x in range(0, num_mappers-1):
			remote_hosts = remote_hosts + (host.lookup_url('http://127.0.0.1:'+sys.argv[x+2]+'/', Host), )
			mappers = mappers + (remote_hosts[x].spawn('mapper'+str(x), 'client/Mapper', open(wd+'/'+filenames[x], 'r').read()), )

		remote_host3 = host.lookup_url('http://127.0.0.1:'+sys.argv[4]+'/', Host)
		print remote_host3
		reducer = remote_host3.spawn('reducer', 'client/Reducer', 2)

		for mapper in mappers:
			mapper.setReducer(reducer)

		for mapper in mappers:
			mapper.start()

		try:
			print mapper1.wait_a_lot(timeout=1)
            #remote_host.stop_actor('mapper1')
            #mapper1.stop()
            #remote_host.shutdown()
		except TimeoutError, e:
			print e
	else:
		print "ERROR: 4 arguments needed: \nMaster Port\n2 Mapper Servers Port\nReducer Server Port";

	sleep(3)
	shutdown()
