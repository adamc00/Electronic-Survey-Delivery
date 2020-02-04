FROM httpd:2.4-alpine

MAINTAINER support@strategicdata.com.au

RUN apk update && \
    apk add perl-cgi \
            perl-dbd-sqlite \
            perl-html-template

# perl-app-cpanminus

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

COPY app/cgi/ /usr/local/apache2/cgi-bin/
COPY app/tmpl/ /usr/local/apache2/tmpl/

COPY app/db/survey.db /usr/local/apache2/db/survey.db
RUN chown daemon:daemon /usr/local/apache2/db/survey.db

COPY app/Images/ /usr/local/apache2/htdocs/images
COPY app/*.html /usr/local/apache2/htdocs/
