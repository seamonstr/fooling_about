FROM alpine/k8s:1.24.16

# Add httpd
RUN apk update
RUN apk add busybox-extras

# Mountpoint for charts directory
RUN mkdir /charts
RUN chmod 755 /charts

# Install the cgi script
COPY index.cgi /var/www/cgi-bin/index.cgi
RUN chmod 755 /var/www/cgi-bin/index.cgi

# Create the user account - don't run as root
RUN adduser -s /bin/bash -D controller-user
USER controller-user
WORKDIR /home/controller-user

# Add the kubectl plugin system and install the ingress-rule plugin to enable
# the webapp to alter the ingress rules as it manages instances
COPY --chown=controller-user:controller-user krew-linux_amd64.tar.gz krew-linux_amd64.tar.gz
RUN tar -xzf krew-linux_amd64.tar.gz
RUN ./krew-linux_amd64 install krew
ENV PATH=$PATH:/home/controller-user/.krew/bin
RUN kubectl krew install ingress-rule 

CMD [ "httpd", "-f", "-h", "/var/www", "-p", "8080", "-vv" ]