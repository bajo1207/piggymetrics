FROM python:3

ADD ./src/Run.py /

RUN pip install cherrypy
RUN pip install requests requests_oauthlib


CMD ["python", "./src/Run.py"]

EXPOSE 4710
