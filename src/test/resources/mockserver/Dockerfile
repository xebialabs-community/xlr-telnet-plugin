FROM fedora:25

MAINTAINER Rick Broker <rbroker@xebialabs.com>

RUN dnf -y install procps net-tools pcre pcre-static python && \
    dnf clean all 
RUN pip install --upgrade pip
RUN pip install flask
RUN mkdir /mockserver

ENV FLASK_APP=/mockserver/app.py
ENV FLASK_ENV=development

COPY app /mockserver

VOLUME /mockserver

EXPOSE 5000

CMD flask run --host=0.0.0.0

