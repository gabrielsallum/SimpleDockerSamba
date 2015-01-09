__author__ = 'sallumg1'

## The idea here is that this program creates the
## configuration file that setup.py will consume, once
## Running iside of the container

import simplejson as json
import os, sys

filename = "usrpsswd.json"

def main(user, password):

    ser = json.dumps \
                ({
                    "user": user,
                    "password": password,
                })


    f = open(filename, 'w')

    f.write(ser)

    f.close()


if __name__ == "__main__":
     if len(sys.argv) > 2:
         main (sys.argv[1],sys.argv[2])
     else:
         print "Program operation: %s, <username> <password> <enter>" % sys.argv[0]