
## Starts from a Debian stable Image
FROM debian:stable

MAINTAINER Gabriel Sallum version: 0.1

RUN apt-get update
RUN apt-get -y install samba samba-common libcups2 python-minimal python-simplejson supervisor

ADD ./usrpsswd.json /tmp/usrpsswd.json
ADD ./smb.conf /etc/samba/smb.conf
ADD ./supervisord.conf /etc/supervisor/supervisord.conf
ADD ./setup.py /tmp/setup.py

EXPOSE 137 138 139 445 88

RUN python /tmp/setup.py

CMD /usr/bin/supervisord -n

#CMD /usr/sbin/smbd -F

