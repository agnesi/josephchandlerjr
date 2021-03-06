from utils import *
import logging
import datetime
import sys
sys.path.append('..')
from handlers.base import jinja_env

from google.appengine.ext import db

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @staticmethod
    def blog_key(name = 'default'):
        return db.Key.from_path('blogs',name)

    @staticmethod
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    @classmethod
    def get_front(cls):
        """Runs DB Query and returns list of 10 latest posts and updated memcache"""
        logging.info("DB QUERY IN Post.get_front()")
        q = db.GqlQuery('select * from Post where ancestor is :1 order by created desc limit 10',cls.blog_key())
        front = list(q)
        age_set('front',front) # update memcache
        return front
            
    @classmethod
    def create(cls, subject, content):
        """Creates new post and adds it to DB. Returns post's key"""
        logging.info("Post.create()")
        p = Post(parent=cls.blog_key(), subject=subject ,content=content)
        key = p.put()
        age_set(str(key.id()),p)
        Post.get_front()
        return p.key()

    @classmethod
    def by_id(cls, pid):
        """search for post by id"""
        logging.info("Post.by_id")
        post = Post.get_by_id(pid, parent = cls.blog_key())   
        return post    

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return Post.render_str("blog_post.html", p = self)

    def dict_repr(self):
        """Returns dictionary representation of post"""        
        return {"subject":self.subject,
                "content":self.content,
                "created":self.created.strftime("%b %d,%Y")}

class User(db.Model):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()
    user_since = db.DateTimeProperty(auto_now_add = True)

    @staticmethod
    def user_key(group = 'default'):
        return db.Key.from_path('users',group)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=cls.user_key())

    @classmethod
    def by_name(cls, username):
        u = cls.all().filter('username =', username).get()
        return u

    @classmethod
    def register(cls, username, pw, email=None):
        salt = make_salt()
        pw_hash = make_pw_hash(username,pw)
        u = User(parent = cls.user_key(), 
                 username = username, 
                 pw_hash = pw_hash, 
                 email = email)
        return u

    @classmethod
    def login(cls, username, pw):
        u = cls.by_name(username)
        if u and valid_pw(username,pw,u.pw_hash):
            return u


class WikiPage(db.Model):
    uri = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @staticmethod
    def wiki_key(group = 'default'):
        return db.Key.from_path('wiki',group)

    @classmethod
    def get_page(cls, uri):
        """Runs DB Query and returns page associated with uri"""
        logging.info("getting page")
        if uri == 'front':
            q = db.GqlQuery('select * from WikiPage')
            return [(page.uri,page.created) for page in q] # returns list of tuples, (uri,created)
        else:
            q = db.GqlQuery('select * from WikiPage where uri = :1 limit 1',uri)
        return q.get()
            
    @classmethod
    def create(cls, uri, content):
        """Creates new page and adds it to DB. Returns page instance"""
        logging.info("WikiPage.create()")
        p = WikiPage(parent=cls.wiki_key(), uri=uri ,content=content)
        p.put()      
        return p

    @classmethod
    def by_id(cls, name, pid):
        """search for pages by id"""
        logging.info("WikiePage.by_id")
        p = WikiPage.get_by_id(pid, parent = cls.wiki_key())   
        return p    

    @classmethod
    def get_all(cls):
        q = db.GqlQuery('select * from WikiPage')
        return list(q)

class WikiEdit(db.Model):
    uri = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    @staticmethod
    def edit_key(group = 'default'):
        return db.Key.from_path('edit',group)


    @classmethod
    def by_page(cls, page):
        q = db.GqlQuery('select * from WikiEdit where uri = :1 order by created desc', page)
        return list(q)

    @classmethod
    def create(cls, uri, content):
        """Creates new edit and adds it to DB. Returns instance"""
        logging.info("WikiEdit.create()")
        e = WikiEdit(parent=cls.edit_key(), uri=uri ,content=content)
        e.put()      
        return e




