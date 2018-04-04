# -*- coding: utf-8 -*-
'''
MapReduce
@author: Cristofol Dauden Esmel & Aleix Marine Tena
'''
import os, sys

class Mapper(object):

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
        print "Mapper has finished"
        return self.result

class Reducer(object):

    def __init__(self):
        self.result = {}

    #Word Count function
    def reduceFunction(self):
        for hashes in self.mappers_output:
            for key in hashes.keys():
                if key in self.result:
                    self.result[key] = self.result[key]+[hashes[key]]
                else:
                    self.result[key] = [hashes[key]]

        for word in self.result.keys():
            self.result[word] = sum(self.result[word])

    def start(self, mappers_output):
        print 'Reducer started'
        self.mappers_output=mappers_output
        self.reduceFunction()
        print "Reducer has finished"
        return self.result

def split(chunknum, filename, wd):
    print "Running Split Function"
    f=open(wd+'/'+filename, 'r')
    os.system("split -n "+str(chunknum)+" "+filename)
    filenames=()
    count=0
    small_letters = map(chr, range(ord('a'), ord('z')+1))
    for i in small_letters:
        for j in small_letters:
            filenames = filenames + ('x'+str(i)+str(j),)
            count+=1
            if( chunknum == str(count) ):
                return filenames

def autoclean(filenames):
    for name in filenames:
        os.system("rm "+name) # TODO working directory
    return 0

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        mappers_output = []

        wd = os.path.dirname(os.path.realpath(__file__))
        filenames = split(sys.argv[1], sys.argv[3], wd)

        mapper = Mapper(sys.argv[2])
        print filenames
        for i in range(int(sys.argv[1])):
            text=open(wd+'/'+filenames[i],'r').read()
            mappers_output.append(mapper.start(text))
        
        reducer = Reducer()
        print reducer.start(mappers_output)

        autoclean(filenames)
    else:
        print "2 arguments nedded:\n\tNum Mappers\n\tMapper function (wc or cw)\n\tFile name"
