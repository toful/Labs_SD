'''
Remote client. Client
@author: Cristofol Dauden Esmel & Aleix Marine Tena
'''
from pyactor.context import set_context, create_host, Host, sleep, shutdown, sys
from pyactor.exceptions import TimeoutError

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


if __name__ == "__main__":
    set_context()

    text_example="sijbd nsaocn ee ckkcmmc ee cmdkscmkjds m skd mskld\n m  msdkm ee m lmsmm msl mdlm msdm lmdsz dslmld"

    if len(sys.argv) >= 4:#5:

        host = create_host('http://127.0.0.1:'+sys.argv[1]+'/')

        remote_host = host.lookup_url('http://127.0.0.1:'+sys.argv[2]+'/', Host)
        print remote_host
        mapper1 = remote_host.spawn('mapper1', 'client/Mapper', text_example)

        remote_host2 = host.lookup_url('http://127.0.0.1:'+sys.argv[3]+'/', Host)
        print remote_host2
        mapper2 = remote_host2.spawn('mapper2', 'client/Mapper', text_example)

        remote_host3 = host.lookup_url('http://127.0.0.1:'+sys.argv[4]+'/', Host)
        print remote_host3
        reducer = remote_host3.spawn('reducer', 'client/Reducer', 2)

        mapper1.setReducer(reducer)
        mapper2.setReducer(reducer)
        mapper1.start()
        mapper2.start()


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
