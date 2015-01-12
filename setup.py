#!/bin/python

# mkdir -p /opt/samba
# mkdir -p /opt/samba/share


import os, commands, subprocess
import simplejson as json
from pwd import getpwnam

filename = "/tmp/usrpsswd.json"
systempath = "/opt/samba"
sambapath= "/opt/samba/share"
sambaConfig = "/tmp/smb.conf"
supervisorCnfFile="/supervisord.conf"

def execute(cmd, msgtrue, msgfalse=None):

    try:
        status = subprocess.call(cmd)
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
        raise RuntimeError("Please run the %s script to generate the configuration and re-build the container" + "\n")

    command = ["useradd", "-d", "/dev/null ", ser["user"]]

    command2 = ["usermod", " --pass=%s %s " % (ser["password"], ser["user"])]

    command3 = [ 'smbpasswd', '-a', ser["user"], ser["password"]]

    execute(command, "user '%s' was correctly added" % ser["user"],
                     "user '%s' was **NOT** added" % ser["user"])

    execute(command2, "user '%s' password was correctly added" % ser["user"],
                      "Password for user '%s' was **NOT** added" % ser["user"] )

    execute(command3, "Adding user %s to smb server complete successfully" % ser["user"],
                      "Adding user %s to smb server **DID NOT** complete successfully" % ser["user"],)

    os.chown(sambapath, getpwnam(ser["user"]).pw_uid, getpwnam(ser["user"]).pw_gid)

    os.chmod(sambapath, 0770)

if __name__ == "__main__":
    main()