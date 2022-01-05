# A simple RSS reader application.

# Copyright (c) 2005 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import anydbm

import e32
import appuifw
from key_codes import *

class RSSFeed:
    def __init__(self,url,title=None):
        self.url=url
        if title is None:
            title=url
        self.listeners=[]
        self.feed={'title': title,
                   'entries': [],
                   'busy': False}
        self.updating=False
    def listen(self,callback):
        self.listeners.append(callback)
    def _notify_listeners(self,*args):
        for x in self.listeners:
            x(*args)
    def start_update(self):
        if self.feed['busy']:
            appuifw.note(u'Update already in progress','info')
            return
        self.feed['busy']=True
        import thread
        thread.start_new_thread(self._update,())
    def _update(self):
        import dumbfeedparser as feedparser
        newfeed=feedparser.parse(self.url)
        self.feed.update(newfeed)
        self.feed['busy']=False
        self._notify_listeners()
    def __getitem__(self,key):
        return self.feed.__getitem__(key)

class CachingRSSFeed(RSSFeed):
    def __init__(self,cache,url,title=None):
        RSSFeed.__init__(self,url,title)
        self.cache=cache
        if cache.has_key(url):
            self.feed=eval(cache[url])
        self.dirty=False
        RSSFeed.listen(self,self._invalidate_cache)
    def _invalidate_cache(self):
        self.dirty=True
    # This method can't simply be a listener called by the RSSFeed,
    # since that call is done in a different thread and currently the
    # e32dbm module can only be used from the same thread it was
    # opened in.
    def save(self):
        if self.dirty:
            self.cache[self.url]=repr(self.feed)


def format_feed(feed):
    if feed['busy']:
        busyflag='(loading) '
    else:
        busyflag=''
    return unicode('%d: %s%s'%(len(feed['entries']),
                               busyflag,
                               feed['title']))

def handle_screen(mode):
    appuifw.app.screen = mode


class ReaderApp:
    def __init__(self,feedlist):
        self.lock=e32.Ao_lock()
        self.exit_flag=False
        self.old_exit_key_handler=appuifw.app.exit_key_handler
        self.old_app_body=appuifw.app.body
        appuifw.app.exit_key_handler=self.handle_exit
        self.feeds=feedlist
        self.articleviewer=appuifw.Text()
        self.feedmenu=appuifw.Listbox([u''],
                                      self.handle_feedmenu_select)
        self.articlemenu=appuifw.Listbox([u''],
                                         self.handle_articlemenu_select)
        screenmodemenu=(u'Screen mode',
                        ((u'full', lambda:handle_screen('full')),
                         (u'large', lambda:handle_screen('large')),
                         (u'normal', lambda:handle_screen('normal'))))
        self.statemap={
            'feedmenu':
            {'menu':[(u'Update this feed', self.handle_update),
                     (u'Update all feeds', self.handle_update_all),
                     (u'Debug',self.handle_debug),
                     screenmodemenu,
                     (u'Exit',self.abort)],
             'exithandler': self.abort},
            'articlemenu':
            {'menu':[(u'Update this feed', self.handle_update),
                     (u'Update all feeds', self.handle_update_all),
                     screenmodemenu,
                     (u'Exit',self.abort)],
             'exithandler':lambda:self.goto_state('feedmenu')},
            'articleview':
            {'menu':[(u'Next article',self.handle_next),
                     (u'Previous article',self.handle_prev),
                     screenmodemenu,
                     (u'Exit',self.abort)],
             'exithandler':lambda:self.goto_state('articlemenu')}}
        self.articleviewer.bind(EKeyDownArrow,self.handle_downarrow)
        self.articleviewer.bind(EKeyUpArrow,self.handle_uparrow)
        self.articleviewer.bind(EKeyLeftArrow,self.handle_exit)
        self.articlemenu.bind(EKeyRightArrow,
                              self.handle_articlemenu_select)
        self.articlemenu.bind(EKeyLeftArrow,self.handle_exit)
        self.feedmenu.bind(EKeyRightArrow,self.handle_feedmenu_select)
        for k in self.feeds:
            k.listen(self.notify)        
        self.goto_state('feedmenu')
    def abort(self):
        self.exit_flag=True
        self.lock.signal()
    def close(self):
        appuifw.app.menu=[]
        appuifw.app.exit_key_handler=self.old_exit_key_handler
        appuifw.app.body=self.old_app_body
    def run(self):
        try:
            while not self.exit_flag:
                self.lock.wait()
                self.refresh()
        finally:
            self.close()
    def notify(self):
        self.lock.signal()
    def refresh(self):
        self.goto_state(self.state)
    def goto_state(self,newstate):
        # Workaround for a Series 60 bug: Prevent the cursor from
        # showing up if the articleviewer widget is not visible.
        self.articleviewer.focus=False
        if newstate=='feedmenu':
            self.feedmenu.set_list(
                [format_feed(x) for x in self.feeds])
            appuifw.app.body=self.feedmenu
            appuifw.app.title=u'RSS reader'
        elif newstate=='articlemenu':
            if len(self.current_feed['entries'])==0:
                if appuifw.query(u'Download articles now?','query'):
                    self.handle_update()
                self.goto_state('feedmenu')
                return 
            self.articlemenu.set_list(
                [self.format_article_title(x)
                 for x in self.current_feed['entries']])
            appuifw.app.body=self.articlemenu
            appuifw.app.title=format_feed(self.current_feed)
        elif newstate=='articleview':
            self.articleviewer.clear()
            self.articleviewer.add(
                self.format_title_in_article(self.current_article()))
            self.articleviewer.add(
                self.format_article(self.current_article()))
            self.articleviewer.set_pos(0)
            appuifw.app.body=self.articleviewer
            appuifw.app.title=self.format_article_title(
                self.current_article())
        else:
            raise RuntimeError("Invalid state %s"%state)
        appuifw.app.menu=self.statemap[newstate]['menu']
        self.state=newstate
    def current_article(self):
        return self.current_feed['entries'][self.current_article_index]
    def handle_update(self):
        if self.state=='feedmenu':
            self.current_feed=self.feeds[self.feedmenu.current()]
        self.current_feed.start_update()
        self.refresh()
    def handle_update_all(self):
        for k in self.feeds:
            if not k['busy']:
                k.start_update()
        self.refresh()
    def handle_feedmenu_select(self):
        self.current_feed=self.feeds[self.feedmenu.current()]
        self.goto_state('articlemenu')
    def handle_articlemenu_select(self):
        self.current_article_index=self.articlemenu.current()
        self.goto_state('articleview')
    def handle_debug(self):
        import btconsole
        btconsole.run('Entering debug mode.',locals())
    def handle_next(self):
        if (self.current_article_index >=
            len(self.current_feed['entries'])-1):
            return
        self.current_article_index += 1
        self.refresh()
    def handle_prev(self):
        if self.current_article_index == 0:
            return
        self.current_article_index -= 1
        self.refresh()
    def handle_downarrow(self):
        article_length=self.articleviewer.len()
        cursor_pos=self.articleviewer.get_pos()
        if cursor_pos==article_length:
            self.handle_next()
        else:
            self.articleviewer.set_pos(min(cursor_pos+100,
                                           article_length))
    def handle_uparrow(self):
        cursor_pos=self.articleviewer.get_pos()
        if cursor_pos==0:
            self.handle_prev()
            self.articleviewer.set_pos(self.articleviewer.len())
        else:
            self.articleviewer.set_pos(max(cursor_pos-100,0))
    def format_title_in_article(self, article):
        self.articleviewer.highlight_color = (255,240,80)
        self.articleviewer.style = (appuifw.STYLE_UNDERLINE|
                                    appuifw.HIGHLIGHT_ROUNDED)
        self.articleviewer.font = 'title'
        self.articleviewer.color = (0,0,255)
        return unicode("%(title)s\n"%article)

    def format_article(self, article):
        self.articleviewer.highlight_color = (0,0,0)
        self.articleviewer.style = 0
        self.articleviewer.font = 'normal'
        self.articleviewer.color = (0,0,0)
        return unicode("%(summary)s"%article)

    def format_article_title(self, article):
        return unicode("%(title)s"%article)
    def handle_exit(self):
        self.statemap[self.state]['exithandler']()

class DummyFeed:
    def __init__(self,data): self.data=data
    def listen(self,callback): pass
    def start_update(self): pass
    def __getitem__(self,key): return self.data.__getitem__(key)
    def save(self): pass
dummyfeed=DummyFeed({'title': 'Dummy feed',
                     'entries': [{'title':'Dummy story',
                                  'summary':'Blah blah blah.'},
                                 {'title':'Another dummy story',
                                  'summary':'Foo, bar and baz.'}],
                     'busy': False})

def main():
    old_title=appuifw.app.title
    appuifw.app.title=u'RSS reader'
    cache=anydbm.open(u'c:\\rsscache','c')
    feeds=[ CachingRSSFeed(url='http://slashdot.org/index.rss',
                           title='Slashdot',
                           cache=cache),
            CachingRSSFeed(url='http://news.bbc.co.uk/rss/newsonline_world_edition/front_page/rss091.xml',
                           title='BBC',
                           cache=cache),
            dummyfeed]
    app = ReaderApp(feeds)
    # Import heavyweight modules in the background to improve application
    # startup time.
    def import_modules():
        import dumbfeedparser as feedparser
        import btconsole
    import thread
    thread.start_new_thread(import_modules,())
    try:
        app.run()
    finally:
        for feed in feeds:
            feed.save()
        cache.close()
        appuifw.app.title=old_title

if __name__=='__main__':
    main()

