#!/usr/bin/env python3
import json
import viena
import subprocess
import sys
import os
import argparse

commandstring = '';
if(sys.argv[1]=="--configure"):
    if(not os.path.isdir(os.path.expanduser('~/.viena'))):
        os.mkdir(os.path.expanduser('~/.viena'))
    val = input("Enter_API_key: ")
    f = open(os.path.expanduser('~/.viena/credentials'), "w")
    f.write("polygon_API_key:"+val)
    f.close()
else:
    for arg in sys.argv:
        if ' ' in arg:
            commandstring += '"{}"  '.format(arg);
        else:
            commandstring+="{}  ".format(arg);

    commandstring=commandstring.replace("/usr/local/bin/viena" ,"python3 -m viena")
    print(commandstring)
    subprocess.call(commandstring, shell=True,cwd=os.path.dirname(viena.__file__))
