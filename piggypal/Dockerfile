FROM python:3

ADD ./src/main/Run.py /

RUN pip install cherrypy
RUN pip install requests requests_oauthlib


CMD ["python", "./src/main/Run.py"]

EXPOSE 4710
