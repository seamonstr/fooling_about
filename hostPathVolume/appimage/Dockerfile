FROM busybox:latest

COPY index.cgi /var/www/cgi-bin/index.cgi
RUN chmod 755 /var/www/cgi-bin/index.cgi

CMD [ "httpd", "-f", "-h", "/var/www", "-vv" ]