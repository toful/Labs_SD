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