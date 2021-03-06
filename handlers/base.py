#base.py
import webapp2
import jinja2
import logging
import urlparse
from main import template_dir 

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                             autoescape = True)

class AppHandler(webapp2.RequestHandler):
    """Base handler, encapsulating jinja2 functions."""
    def initialize(self,*a,**kw):        
        logging.info("initialize Handler")
        super(AppHandler,self).initialize(*a,**kw)
        if self.request.url.endswith(".json"):
            self.format = 'json'
        else:
            self.format = 'html'

    def render_str(self, template, values=None, **kwargs):
        t = jinja_env.get_template(template)
        return t.render(values or kwargs)

    def render(self,template, values=None, **kwargs):
        self.response.write(self.render_str(template,values or kwargs))

    def write(self,*args,**kwargs):
        """write an arbitrary string to the response string"""
        self.response.out.write(*args)
    
    def redirect_to_referer(self):
        if self.request.referer: 
            path = urlparse.urlparse(self.request.referer).path
            self.redirect(path)
        else:
            self.redirect('/')

    def redirect_to(self, name, *args, **kwargs):
        """Redirect to a URI that corresponds to a route name."""
        logging.debug("redirect to %s" %name)
        self.redirect(self.uri_for(name, *args, **kwargs))




