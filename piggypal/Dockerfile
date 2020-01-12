FROM ubuntu:18.04

RUN apt update -y &&\
    apt install -y python3-pip python3-dev

RUN python3 -m pip install --upgrade cherrypy \
                                     requests \
                                     requests_oauthlib \
                                     opencensus \
                                     opencensus-ext-zipkin \
                                     prometheus-client \
                                     opencensus-ext-prometheus

COPY ./src/main /

ENTRYPOINT [ "python3" ]

CMD ["./Run.py"]

EXPOSE 4710