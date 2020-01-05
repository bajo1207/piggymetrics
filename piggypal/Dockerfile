FROM python:3

ADD ./src/Run.py /

RUN pip install cherrypy
RUN pip install jinja2

CMD ["python", "./src/Run.py"]

EXPOSE 4710
