# dms-cas-auth-forwarder

flask app to allow login to DigitalMeasures Solutions (DMS).

DigitalMeasures portal auth documentation https://www.digitalmeasures.com/login/dm/faculty/authentication/HMACTest.do

# How it works
redirects user to cas login, cas sends them back, checks cas ticket, then redirects them to DMS with some querystring params.

# Docker config
Adapted  from https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/dockerfile

https://github.com/tiangolo/uwsgi-nginx-flask-docker

# docker run and build
docker build -t dms-cas-auth-forwarder.

docker run -it -p 80:80 dms-cas-auth-forwarder

# for production use
would need to use https and change / override the environment variables specified in the dockerfile.