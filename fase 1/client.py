'''
Remote client. Client
@author: Cristofol Dauden Esmel & Aleix Marine Tena
'''
from pyactor.context import set_context, create_host, Host, sleep, shutdown, sys
from pyactor.exceptions import TimeoutError
from subprocess import call
import os, sys

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

    text_example="sijbd nsaocn ee ckkcmmc ee cmdkscmkjds m skd mskld\n m  msdkm ee m lmsmm msl mdlm msdm lmdsz dslmld"

    if len(sys.argv) >= 1:

        host = create_host('http://127.0.0.1:'+sys.argv[1]+'/')
        wd = os.path.dirname(os.path.realpath(__file__)) # Obtenim working directory

        #Getting the server proxy
        registry = host.lookup_url('http://127.0.0.1:6000/regis', 'Registry','registry')
        remote_hosts = registry.get_all()
        split(len(remote_hosts)- 1, "input.txt", wd)
        remote_host = remote_hosts.pop()
        reducer = remote_host.spawn('reducer', 'client/Reducer', len(remote_hosts))
        i = 0
        for remote_host in remote_hosts:
            mapper = remote_host.spawn('mapper'+str(i), 'client/Mapper', text_example)
            mapper.setReducer(reducer)
            mapper.start()
            i+=1
        try:
            print "fi"
            #print mapper1.wait_a_lot(timeout=1)
            #remote_host.stop_actor('mapper1')
            #mapper1.stop()
            #remote_host.shutdown()
        except TimeoutError, e:
            print e
    else:
        print "ERROR: 4 arguments needed: \nMaster Port\n2 Mapper Servers Port\nReducer Server Port";

    sleep(3)
    shutdown()
