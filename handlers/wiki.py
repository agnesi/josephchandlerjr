#wiki.py
import logging
import re
from lib.DB import User, WikiPage, WikiEdit
from blog import BlogHandler

from google.appengine.api import memcache

class WikiHandler(BlogHandler):
    def initialize(self,*a, **kw):
        super(WikiHandler,self).initialize(*a,**kw)
        self.button = (self.user or '') and 'Save'
        self.edit_link = (self.user or '') and '<a href="/wiki/_edit/%s" class="nav-option">edit</a>'
        self.in_out = (self.user and 'logout') or 'login'

    def get_wiki_page(self,page):
        logging.info('get wiki page')
        wiki_page = memcache.get(page) or WikiPage.get_page(page)
        logging.info('wiki_page is %s' %wiki_page)
        return memcache.get(page) or WikiPage.get_page(page)

    def white_grey(self):
        while True:
            yield 'white'
            yield 'grey'

    def get_wiki_content(self,wiki_page):
        logging.info('get wiki content = %s')
        if wiki_page:
            if isinstance(wiki_page,WikiPage):
                logging.info('is instance of wikipage = %s' %wiki_page.content)
                return wiki_page.content
            else:
                logging.info('is NOT instance of wikipage = %s' %wiki_page)
                return wiki_page 
        else:
            logging.info('get_wiki_content returning empty string')
            return ''

    def get_front(self):
        return (memcache.get('front') or WikiPage.get_page('front')) or []

    def update_front(self,p):
        """p is a page object"""
        old_cache = memcache.get('front') or []
        memcache.set('front',old_cache.append((p.uri,p.created)))

    def create_edit(self,page,content):
        """makes new edit in db and updates memcache"""
        logging.info('CREATE_EDIT')
        e = WikiEdit.create(page, content)
        created = e.created
        old_cache = memcache.get(page + 'edits') or []
        memcache.set(page + 'edits',old_cache.append((content,created)))

    def get_page_edits(self,page):
        return memcache.get(page + 'edits') or WikiEdit.by_page(page)

    def create_wiki_page(self,page,content):
        """Creates new WikiPage and new WikiEdit in DB. Updates front in cache""" 
        logging.info('create_wiki_page')
        wiki_page = WikiPage.create(page,content) # make page
        memcache.set(page,content)  # update cache of page
        self.update_front(wiki_page) # update list of pages for front of wiki
        return wiki_page

    def update_wiki_page(self,wiki_page,content):
        """update wiki_page in DB and cache. create an edit"""
        wiki_page.content = content      # these lines upate the wiki page
        wiki_page.put()                     # in the database
        page = wiki_page.uri
        memcache.set(page,content)    # update cache
        self.create_edit(page,content)
               

class Front(WikiHandler):
    def get(self,*args):
        logging.info('Front.get()')
        front = self.get_front()
        color = self.white_grey()
        pages = [(page[0],page[1],color.next()) for page in front]
        self.render('wiki_front.html', pages=pages, in_out=self.in_out)

class History(WikiHandler):
    def get(self,page):
        logging.info('history.get()')
        edits = WikiEdit.by_page(page)
        color = self.white_grey()
        n = len(edits)
        edit_info = [(n-i,e.created,e.content,color.next()) for i,e in enumerate(edits)]
        logging.info('edits are %s' %edit_info)
        self.render('wiki_history.html', page=page, edits=edit_info, in_out=self.in_out)

class Page(WikiHandler):
    def get(self,page):
        logging.info('Page.get() page=%s' %page)
        page = page.strip('/')      
        wiki_page = self.get_wiki_page(page)
        if wiki_page:
            content = self.get_wiki_content(wiki_page)                   
            self.render('wiki_page.html',page = page, content = content, edit_button = self.edit_link %page)
        else:
            memcache.set(page,'')        # update memcache to show blank content so another DB query isn't necessary
            self.redirect_to('wiki_edit',page=page)

class Edit(WikiHandler):
    def get(self,page):
        logging.info('Edit.get(%s)' %page)
        if not self.user:
            self.redirect_to('wiki_front','/')
        page = page.strip('/')
        wiki_page = self.get_wiki_page(page)
        content = self.get_wiki_content(wiki_page)    
        self.render('wiki_edit.html',content=content, edit_button = self.button)

    def post(self,page):
        if not self.user:
            redirect_to('wiki_front','/')
        page = page.strip('/')
        new_content = self.request.get('content') # get updated content
        wiki_page = WikiPage.get_page(page)  # look for existing wiki page
        if not wiki_page:                   # if it's not there....
            wiki_page = self.create_wiki_page(page,new_content) 
            self.redirect_to('wiki_page', page=page)
        else:
            old_content = self.get_wiki_content(wiki_page)
            logging.info('new content is %s' %new_content)
            logging.info('old content is %s' %old_content)   
            if old_content == new_content:                    # if updated content is not an update at all...  
                logging.info('old==new....%s' %(old_content==new_content))
                self.render('wiki_edit.html',content=new_content, edit_button = self.button, error='no changes detected')
            else:
                self.update_wiki_page(wiki_page,new_content) 
                logging.info('page = %s' %page)                
                self.redirect_to('wiki_page', page=page)


