#blog.py
import logging
import datetime
import json
from lib.DB import *
from lib.utils import *
from base import AppHandler

from google.appengine.api import memcache

class BlogHandler(AppHandler):
    """Base blog handler"""
    def initialize(self,*a,**kw):
        super(BlogHandler,self).initialize(*a,**kw)
        uid = self.read_secure_cookie("user_id")
        self.user = uid and User.by_id(int(uid))
        if self.user:
            self.username = self.user.username
        
    def login(self,u):
        """ u is an instance. sets user_id Cookie"""   
        self.set_secure_cookie("user_id",u.key().id())    

    def logout(self):
        self.response.headers.add_header('Set-Cookie',str('user_id=; Path=/'))

    def read_secure_cookie(self,name):
        """Returns cookie value if cookie is valid else None|False"""
        cookie = self.request.cookies.get(name)    
        return cookie and get_cookie_val(cookie)        
            
    def set_secure_cookie(self,name,val):
        """Sets secure Cookie of form name=val"""
        secure_val = make_secure_cookie(str(val))
        self.response.headers.add_header('Set-Cookie','%s=%s; Path=/' %(name,secure_val))

    def write_json(self,data):
        self.response.headers.add_header('Content-Type','application/json; charset=UTF-8')
        self.write(json.dumps([d.dict_repr() for d in data]))


class Front(BlogHandler):
    def get(self,suffix):
        admin_option = self.user and ("/logout","logout") or ("/login", "admin")
        posts = age_get('front') or Post.get_front()
        if isinstance(posts,tuple):  
            (posts,t1) = posts
            timedelta = get_time_delta(t1)
        else:
            timedelta = ""           
        self.render("blog_front.html",entries=posts,queried=timedelta,admin1=admin_option[0],admin2=admin_option[1])

class NewPost(BlogHandler):
    def get(self, suffix):
        if not self.user:
            logging.info('redirect')
            self.redirect_to("login","/")
        self.render("blog_newpost.html")

    def post(self,suffix):
        if not self.user:
            logging.info('redirect')
            self.redirect_to("login","/")
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            p = Post.create(subject,content)
            self.redirect_to("blog_front", "/")
        else:
            error = "Subject and Content are both required fields"
            self.render("blog_newpost.html",subject=subject,content=content,error=error)




