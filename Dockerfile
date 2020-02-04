FROM httpd:2.4-alpine

MAINTAINER support@strategicdata.com.au

# RUN apk update &&
#     apk add curl jq

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

COPY app/cgi/ /usr/local/apache2/cgi-bin/
COPY app/tmpl/ /usr/local/apache2/tmpl/

COPY app/Images/ /usr/local/apache2/htdocs/images
COPY app/*.html /usr/local/apache2/htdocs/
