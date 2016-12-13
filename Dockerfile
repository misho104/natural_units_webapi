FROM nginx:latest

MAINTAINER Misho <contact@misho-web.com>

LABEL Vendor="Misho" \
      Version="0.1" \
	    Description="nginx server for natural units calculation"

WORKDIR /home

# Thanks to https://github.com/hwestphal/docker-nginx-fcgi/blob/master/Dockerfile
RUN apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests -y units wget spawn-fcgi fcgiwrap libjson-perl \
  && rm -rf /var/lib/apt/lists/* \
  && sed -i 's/^\(user .*\)$/user root;/' /etc/nginx/nginx.conf

RUN wget https://raw.githubusercontent.com/misho104/natural_units/master/natural.units

ADD index.cgi /usr/share/nginx/html/index.cgi
ADD nginx_default.conf /etc/nginx/conf.d/default.conf
RUN chmod 755 /usr/share/nginx/html/index.cgi

EXPOSE 80

CMD spawn-fcgi -s /var/run/fcgiwrap.sock /usr/sbin/fcgiwrap && nginx -g "daemon off;"

