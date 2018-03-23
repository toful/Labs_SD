# -*- coding: utf-8 -*-
'''
Remote client. Client
@author: Cristofol Dauden Esmel & Aleix Marine Tena
'''
from pyactor.context import set_context, create_host, Host, sleep, shutdown, sys
from pyactor.exceptions import TimeoutError
from subprocess import call
import os, sys
import requests
import re


class Mapper(object):
    _ask = ['wait_a_lot']
    _tell = ['start', 'mapFunction','setReducer']
    _ref = ['setReducer']

    def __init__(self, text, option):
        print 'Mapper started'
        self.result = {}
        self.text = text
        self.option = option

    def mapFunctionWC(self):
        # remove leading and trailing whitespace
        # line = v.strip() Aquesta linia es reundant si fem word.strip() a cada paraula
        # split the line into words
        print "Running Word Count"
        self.text = self.text.translate(None, "-?.!,;:()\"").lower() # deleting trash characters
        #self.text = re.sub(r'[.(),:;?"!-\\\']', "", self.text) # deleting trash characters TODO
        for line in self.text.split("\n"):
            for word in line.strip().split():  
                if word in self.result:
                    self.result[word] = self.result.get(word)+1
                else:
                    self.result[word] = 1
        
        return 0

    def mapFunctionCW(self):
        print "Running Counting Words"
        self.result={"counter":0}
        for line in self.text.split("\n"):
            for word in line.strip().split():  # aqui no fa falta eliminar caracters brossa ja que nomes comptem ocurrencies
                self.result["counter"] = self.result["counter"]+1
        
        return 0

    def wait_a_lot(self):
        sleep(2)
        return 'ok'

    def setReducer(self, reducer):
        self.reducer=reducer

    def start(self):
        i=0

        if self.option == "wc":
            self.mapFunctionWC()

        elif self.option == "cw":
            self.mapFunctionCW()

        else:
            print "ERROR: incorrect option, select:\nwc - WordCount\ncw - CountingWords"
            return 1
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

    #Word Count function
    def reduceFunction(self, k, v):
        self.result[k] = sum(v)

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
                    self.result[key] = self.result[key]+[hashes[key]]
                else:
                    self.result[key] = [hashes[key]]

        for word in self.result.keys():
            self.reduceFunction(word, self.result[word])
        print self.result
        #stop_actor(self, self)

'''class split(chunknum, filename, wd, Exception): pass
    
    _ask = ['wait_a_lot']
    _tell = ['start', 'reduceFunction', 'getMapperOutput']

    def __init__(self, num_mappers):'''
class max_filenames(Exception):
    pass

def split(chunknum, filename):
    os.system("split -n "+str(chunknum)+" "+filename) 
    filenames = ()
    count = 0
    small_letters = map(chr, range(ord('a'), ord('z')+1))
    try:
        for i in small_letters:
            for j in small_letters:
                filenames = filenames + ('x'+str(i)+str(j),)
                count+=1
                if (chunknum == count):
                    raise max_filenames('Escaping from loop')
        
    except max_filenames:
        print ""

    return filenames
# Parameters:
# 1: Port used to establish the communication
# 2: Registry IP (Port is hardcoded to be 6000)
# 3: Operation to use [wc|cw]
if __name__ == "__main__":
    set_context()
    if len(sys.argv) > 2:
        host = create_host('http://127.0.0.1:'+sys.argv[1]+'/')
        wd = os.path.dirname(os.path.realpath(__file__)) # Obtenim working directory

        #Getting the server proxy
        registry = host.lookup_url('http://'+sys.argv[2]+':6000/regis', 'Registry','registry')
        remote_hosts = registry.get_all()
        remote_host = remote_hosts.pop()
        files = split(len(remote_hosts), "sherlock.txt")
        reducer = remote_host.spawn('reducer', 'client/Reducer', len(remote_hosts))
        i = 0
        for remote_host in remote_hosts:
            mapper = remote_host.spawn('mapper'+str(i), 'client/Mapper', open(wd+'/'+files[i], 'r').read(), sys.argv[3])
            print "Mapper "+str(i)+" has been created"
            mapper.setReducer(reducer)
            mapper.start()
            i+=1
        os.system("rm x*")  # TODO ficar al HTTPServer que sera el que sofrira la particio del fitxer

        try:
            print "fi"
            #print mapper1.wait_a_lot(timeout=1)
            #remote_host.stop_actor('mapper1')
            #mapper1.stop()
            #remote_host.shutdown()
        except TimeoutError, e:
            print e
    else:
        print "ERROR: 3 arguments needed: \nMaster Port\nNumber of Mappers\nOperation: (wc or cw)";

    sleep(3)
    shutdown()
