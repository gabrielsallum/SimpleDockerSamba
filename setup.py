#!/bin/python


import os, commands, subprocess
import simplejson as json
from pwd import getpwnam

filename = "/tmp/usrpsswd.json"
systempath = "/opt/samba"
sambapath= "/opt/samba/share"
sambaConfig = "/tmp/smb.conf"
supervisorCnfFile="/supervisord.conf"

def execute(cmd, msgtrue, msgfalse=None):

    print "executing cmd : %s \n" %cmd

    try:
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            raise RuntimeError("the external command has failed")
    except:
        raise RuntimeError(msgfalse + "\n" + "Command: " + cmd)
    print msgtrue

    return status

def main():
    os.mkdir(systempath)
    os.mkdir(sambapath)

    f = open(filename, 'r')

    config = str(f.read())

    f.close()

    try:
        ser = json.loads(config)
    except:
        raise RuntimeError("Please run the setup.py script to generate the configuration and re-build the container" + "\n")

    command = "useradd -d /dev/null -G sambashare -p %s " + ser["user"]

    #command2 = 'smbpasswd -a %s' % ser["user"]

    execute(command, "user '%s' was correctly added" % ser["user"],
                     "user '%s' was **NOT** added" % ser["user"])

    #execute(command2, "Adding user %s to smb server complete successfully" % ser["user"]
    #    "Adding user %s to smb server **DID NOT** complete successfully" % ser["user"],)


    p1 = subprocess.Popen(["echo", "-e", ser["password"]])

    p2 = subprocess.Popen(["echo", "-e", ser["password"]], stdin=p1.stdout)

    p3 = subprocess.Popen(['smbpasswd', '-s', '-a', ser["user"]], stdin=p2.stdout, stdout=subprocess.PIPE)

    print "** " + p3.communicate()[0]

    os.chown(sambapath, getpwnam(ser["user"]).pw_uid, getpwnam(ser["user"]).pw_gid)

    os.chmod(sambapath, 0770)

if __name__ == "__main__":
    main()