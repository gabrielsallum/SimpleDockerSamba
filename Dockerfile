
## Starts from a Debian stable Image
FROM debian:stable

MAINTAINER Gabriel Sallum version: 0.1

RUN apt-get update
RUN apt-get -y install samba samba-common libcups2 python-minimal python-simplejson supervisor


ADD ./usrpsswd.json /tmp/usrpsswd.json
ADD ./smb.cnf /tmp/smb.cnf
ADD ./setup.py /tmp/setup.py

EXPOSE  139 445

CMD ["python", "/tmp/setup.py"]





