#!/bin/python

# mkdir -p /opt/samba
# mkdir -p /opt/samba/share


import os, commands, shutil
import simplejson as json
from pwd import getpwnam

filename = "/tmp/usrpsswd.json"
systempath = "/opt/samba"
sambapath= "/opt/samba/share"
sambaConfig = "/tmp/smb.cnf"
supervisorCnfFile="/supervisord.conf"

def execute(cmd, msgtrue, msgfalse=None):

    status, output = commands.getstatusoutput(cmd)

    if status is 0:
        print msgtrue
    else:
        raise RuntimeError(msgfalse + "\n" + output)


def main():
    os.mkdir(systempath)
    os.mkdir(sambapath)

    f = open(filename, 'r')

    config = str(f.read())

    f.close()

    ser = json.loads(config)

    command = "useradd -d /dev/null " + ser["user"]

    command2 = "usermod --pass=%s %s " % (ser["password"], ser["user"])

    execute(command, "user '%s' was correctly added" % ser["user"],
                     "user '%s' was **NOT** added" % ser["user"])

    execute(command2, "user '%s' password was correctly added" % ser["user"],
                      "Password for user '%s' was **NOT** added" % ser["user"] )

    os.chown(sambapath, getpwnam(ser["user"]).pw_uid, getpwnam(ser["user"]).pw_gid)

    os.chmod(sambapath, 0770)

    shutil.move(sambaConfig, '/etc/samba/smb.conf')

    sprvrd = "[supervisord] \
              nodaemon=true\
              [program:smbd]\
              command=/usr/sbin/smbd \
              [program:smbd] \
              command=/usr/sbin/nmbd"
    print sprvrd

    f = open(supervisorCnfFile, 'w')

    f.write(sprvrd)

    f.close()

    execute("/usr/bin/supervisord -n -c " + supervisorCnfFile, "Cool", "Not Cool")


if __name__ == "__main__":
    main()