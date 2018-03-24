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
import codecs



class Mapper(object):
    _ask = ['wait_a_lot']
    _tell = ['start', 'mapFunction','setReducer']
    _ref = ['setReducer']

    def __init__(self, option):
        self.result = {}
        self.text = ""
        self.option = option
        print 'Mapper initialized'


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

    def start(self, text):
        print 'Mapper has started'
        self.text = text
        i=0

        if self.option == "wc":
            self.mapFunctionWC()

        elif self.option == "cw":
            self.mapFunctionCW()

        else:
            print "ERROR: incorrect option, select:\nwc - WordCount\ncw - CountingWords"
            return 1
        self.reducer.getMapperOutput(self.result)
        print "Mapper has finished"
        exit()
        os.system(exit)

class Reducer(object):
    _ask = ['wait_a_lot']
    _tell = ['start', 'reduceFunction', 'getMapperOutput']

    def __init__(self, num_mappers):
        self.result = {}
        self.mappers_output = []
        self.mappers_finished = 0
        self.num_mappers=num_mappers
        print 'Reducer initialized'

    #Word Count function
    def reduceFunction(self, k, v):
        print "Running Reduce Function"
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
        print 'Reducer started'
        for hashes in self.mappers_output:
            for key in hashes.keys():
                if key in self.result:
                    self.result[key] = self.result[key]+[hashes[key]]
                else:
                    self.result[key] = [hashes[key]]

        for word in self.result.keys():
            self.reduceFunction(word, self.result[word])
        print "Reducer has finished"
        print self.result

class max_filenames(Exception):
    pass

class Splitter(object):
    _ask = ['wait_a_lot']
    _tell = ['start', 'split']

    def __init__(self, filename, hosts, IP_webserver):
        print "Splitter initilized"
        self.filename = filename
        self.chunknum = len(hosts)
        self.hosts = hosts
        self.IP_webserver = IP_webserver

    def wait_a_lot(self):
        sleep(2)
        return 'ok'

    def split(self, chunknum):
        print "Running Split Function"
        os.system("split -n "+str(chunknum)+" "+"Out.txt") 
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
            return filenames    

    def start(self):
        print "Splitter has started"
        text = requests.get("http://"+self.IP_webserver+":8000/"+self.filename).text # Obtaining text from desired file from HTTP server
        wd = os.path.dirname(os.path.realpath(__file__)) # Obtenim working directory

        file = codecs.open(wd+'/Out.txt', 'w', 'utf-8') # Per alguna rao el working directory o es la del server directament. Pot ser per treballar en local(?)
        file.write(text) 
        file.close()
        filenames = self.split(self.chunknum) # Split file in chunknum parts
        
        i = 0
        for host in self.hosts:
            host.start(open(wd+'/'+filenames[i], 'r').read())
            i+=1

        #AUTO-CLEAN
        for name in filenames:
            os.system("rm "+name) # TODO working directory
        os.system("rm Out.txt")
        print "Splitter has finished"

        return "holi"



# Parameters:
# 1: Port used to establish the communication
# 2: Registry IP (Port is hardcoded to be 6000)
# 3: Operation to use [wc|cw]
# 4: Input file from HTTP Server
# 5: IP from web server
# TODO kill the actors
if __name__ == "__main__":
    set_context()
    if len(sys.argv) > 4:
        host = create_host('http://127.0.0.1:'+sys.argv[1]) #Create our own host TODO obtain real IP or parametrize for future testing
        remote_hosts = host.lookup_url('http://'+sys.argv[2]+':6000/regis', 'Registry','registry').get_all() # Obtaining list of servers
        remote_host = remote_hosts.pop()
        print len(remote_hosts)
        reducer = remote_host.spawn('reducer', 'client/Reducer', len(remote_hosts)-1) 
        i = 0
        hosts = ()
        remote_host = remote_hosts.pop() # deleting possible autoreference in splitter

        for host in remote_hosts:
            mapper = host.spawn('mapper'+str(i), 'client/Mapper', sys.argv[3])
            hosts = hosts + (mapper, )
            print "Mapper "+str(i)+" has been created"
            mapper.setReducer(reducer)
            i+=1

        print len(remote_hosts)
        splitter = remote_host.spawn('splitter', 'client/Splitter', sys.argv[4], hosts, sys.argv[5])  # converting one server into a splitter
        print splitter.start()

        try:
            print "fi"
            sleep(20)
            #print mapper1.wait_a_lot(timeout=1)
            #remote_host.stop_actor('mapper1')
            #mapper1.stop()
            #remote_host.shutdown()
        except TimeoutError, e:
            print e
    else:
        print "ERROR: 5 arguments needed: \n1: Port used to establish the communication\n2: Registry IP (Port is hardcoded to be 6000)\n3: Operation to use [wc|cw]\n4: Input file from HTTP Server\n5: IP from web server";

    sleep(3)
    shutdown()
