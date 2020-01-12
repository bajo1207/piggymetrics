import cherrypy
from utils import SRC_DIR
from opencensus.trace.tracer import Tracer
from opencensus.trace import time_event as time_event_module
from opencensus.ext.zipkin.trace_exporter import ZipkinExporter
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.status import Status

ze = ZipkinExporter(service_name="login-button",
                                host_name='localhost',
                                port=9411,
                                endpoint='/api/v2/spans')
tracer = Tracer(exporter=ze, sampler=AlwaysOnSampler())

class Login_button(object):
    @cherrypy.expose
    def index(self):
        """
        Returns the "connect with paypal"-button as valid HTML.
        Acts as Index page to piggypal
        """
        with tracer.span(name="login-button-request") as span:
            span.status = Status(0, "Returning login.html")
            return open(SRC_DIR + "/Views/login.html")
