import inspect
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os

class BaseController:
    def get_template(self, caller_name):
        template = None
        try:
            class_name = self.__class__.__name__.replace('Controller', '')
            view_base = '{0}/Views'.format(os.path.abspath("./").replace("\\", "/"))
            view_path = '{0}/{1}'.format(view_base, class_name)
            env = Environment(loader=FileSystemLoader([view_base, view_path]))
            template = env.get_template(caller_name.capitalize() + '.html')
        except TemplateNotFound as template_ex:
            pass
        return template

    def render_template(self, template_vars={}):
        try:
            caller_name = inspect.stack()[1][3]
            return self.get_template(caller_name).render(template_vars)
        except Exception as ex:
            return None