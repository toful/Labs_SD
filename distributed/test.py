'''
Testing project file, it will call the proves.sh script
'''

import os

if __name__ == "__main__":
	os.system("./proves.sh 1234 127.0.0.1 wc HTTPServer/big.txt 127.0.0.1 127.0.0.1 4")
