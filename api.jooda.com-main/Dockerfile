############################################################
# Dockerfile to run a Django-based fooiy RESTful SEVER
# Based on an AMI
############################################################

# Set base image
FROM ubuntu:20.04

# Set maintainer
LABEL name="jooda"

# Directory in container for all project files
ENV JOODA_DOCKER_SRVHOME=/srv
# Local directory with project source
ENV JOODA_DOCKER_SRC=repo
# Directory in container for project source files
ENV JOODA_DOCKER_SRVPROJ=$JOODA_DOCKER_SRVHOME/$JOODA_DOCKER_SRC

# Set TImezone
ENV TZ='Asia/Seoul'
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set apt packages
RUN apt-get -y update
RUN apt-get install -y python3-pip python3-dev
RUN apt-get install -y apt-utils
RUN apt-get install -y tzdata
RUN cd /usr/local/bin
RUN ln -s /usr/bin/python3 python
RUN pip3 install --upgrade pip
RUN apt-get install -y libssl-dev
RUN apt-get install -y mysql-server
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y nginx
RUN apt-get install --reinstall -y systemd
RUN pip3 install gunicorn
RUN pip3 install gevent

# SET Locale
RUN apt-get install -y language-pack-ko
RUN locale-gen ko_KR.UTF-8

# Create application LogDir
WORKDIR $JOODA_DOCKER_SRVHOME
RUN mkdir logs
# Log Mount
VOLUME ["$JOODA_DOCKER_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $JOODA_DOCKER_SRC/requirements.txt $JOODA_DOCKER_SRVPROJ/requirements.txt

# Install Python dependencies
RUN pip3 install -r $JOODA_DOCKER_SRVPROJ/requirements.txt

#COPY 
COPY $JOODA_DOCKER_SRC/manage.py $JOODA_DOCKER_SRVPROJ/manage.py
COPY $JOODA_DOCKER_SRC/common $JOODA_DOCKER_SRVPROJ/common
COPY $JOODA_DOCKER_SRC/templates $JOODA_DOCKER_SRVPROJ/templates
COPY $JOODA_DOCKER_SRC/static $JOODA_DOCKER_SRVPROJ/static
# COPY $JOODA_DOCKER_SRC/firebase_service_account_key.json $JOODA_DOCKER_SRVPROJ/firebase_service_account_key.json

# Port to expose
EXPOSE 80

WORKDIR $JOODA_DOCKER_SRVPROJ
COPY ./django_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Run Server
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]