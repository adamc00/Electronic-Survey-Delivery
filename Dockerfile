FROM httpd:2.4-alpine

MAINTAINER support@strategicdata.com.au

RUN apk update && \
    apk add perl-cgi \
            perl-dbd-sqlite \
            perl-html-template \
            sqlite

# perl-app-cpanminus

COPY httpd.conf /usr/local/apache2/conf/httpd.conf

COPY app/cgi/ /usr/local/apache2/cgi-bin/
COPY app/tmpl/ /usr/local/apache2/tmpl/
COPY app/Images/ /usr/local/apache2/htdocs/images
COPY app/*.html /usr/local/apache2/htdocs/

COPY app/db/schema.sql /usr/local/apache2/db/schema.sql
COPY app/db/*.csv /usr/local/apache2/db/
RUN cd /usr/local/apache2/db && \
    sqlite3 survey.db < schema.sql && \
    rm schema.sql *.csv && \
    chown -R daemon:daemon /usr/local/apache2/db
