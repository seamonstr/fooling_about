FROM alpine/k8s:1.24.16

# Add httpd
RUN apk update
RUN apk add busybox-extras

# Mountpoint for charts directory
RUN mkdir /charts
RUN chmod 755 /charts

COPY index.cgi /var/www/cgi-bin/index.cgi
RUN chmod 755 /var/www/cgi-bin/index.cgi



CMD [ "httpd", "-f", "-h", "/var/www", "-vv" ]