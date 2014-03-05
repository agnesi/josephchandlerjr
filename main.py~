import os
from webapp2 import WSGIApplication, Route
import sys
import logging




#set useful fields
root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'templates')


application = WSGIApplication([     Route(r'/', handler='handlers.home.Home', name='home'),
                                    Route(r'/about', handler='handlers.home.About', name='about'),
                                    Route(r'/family', handler='handlers.home.Family', name='family'),
                                    Route(r'/projects', handler='handlers.home.Projects', name='projects'),
                                    Route(r'/login<:/?>', handler='handlers.home.Login', name='login'),
                                    Route(r'/logout', handler='handlers.home.Logout', name='logout'),
                                    Route(r'/flush', handler='handlers.home.Flush', name='flush'), 
                                    Route(r'/blog<:/?>', handler='handlers.blog.Front', name='blog_front'),                        
                                    Route(r'/blog/newpost<:/?>',handler='handlers.blog.NewPost', name='new_post'),     
                                    Route(r'/blog/<post_id:\d+><suffix:.*>',handler='handlers.blog.Permalink', name='perm') ],    debug=True)

