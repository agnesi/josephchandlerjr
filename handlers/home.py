import logging
import re
from lib.DB import *
from base import AppHandler, jinja_env
from blog import BlogHandler
from google.appengine.api import mail
from google.appengine.api import memcache
from lib.utils import Project
from lib.projects import projects

class Home(AppHandler):
    def get(self):
        self.render("about.html")

class About(AppHandler):
    def get(self):
        self.render("about.html")

class Family(AppHandler):
    def get(self):
        self.render("family.html")

class Projects(AppHandler):
    def get(self):
        p = []
        for project in projects:
            p.append(Project(*project))
        self.render("projects.html",projects=p)

class Resume(AppHandler):
    def get(self, *args):
        self.render("resume.html")

class Flush(BlogHandler):
    """Clears the cache and redirects to front page"""    
    def get(self):
        if not self.user:
            self.redirect_to_referer()
        memcache.flush_all()
        self.redirect_to("home")

class Login(BlogHandler):
    logging.info('LOGIN')
    def get(self, *args):
        self.render('login.html')

    def post(self, *args):
        username = self.request.get('username')
        password = self.request.get('password')   
        u = User.login(username,password)
        if u:
            self.login(u)
            logging.info("login user=%s" %username)
            logging.info('redirect')
            self.redirect_to("blog_front", "/")
        else:
            logging.info("login fail user=%s"%username)
            error = "Incorrect username/password combination"
            self.render('login.html', error=error)

class Logout(BlogHandler):
    """Logs user out and redirects to registration page"""
    def get(self):    
        self.logout()
        logging.info('redirect')
        self.redirect_to("blog_front",'/')


