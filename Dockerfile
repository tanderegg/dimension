FROM centos
MAINTAINER Tim Anderegg, timothy.anderegg@gmail.com

ENV PYTHONUNBUFFERED 1

RUN umask 022 \
  && yum -y install epel-release \
  && yum clean all \
  && yum -y install python34 \
  python34-devel \
  python34-pip \
  gcc \
  postgresql-devel

ADD requirements.txt
RUN pip3 install -r requirements.txt

ADD src/ .

RUN otree collectstatic

EXPOSE 8000
