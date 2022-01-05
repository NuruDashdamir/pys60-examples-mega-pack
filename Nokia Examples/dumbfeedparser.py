# A simple and limited RSS feed parser used in the RSS reader example.

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


import re
import urllib

def parse(url):
    return parse_feed(urllib.urlopen(url).read())

def parse_feed(text):
    feed={}
    items=[]
    currentitem=[{}]

    def clean_entities(text): return re.sub('&[#0-9a-z]+;','?',text)
    def clean_lf(text): return re.sub('[\n\t\r]',' ',text)

    def end_a(tag,content): write('LINK(%s)'%gettext())
    def start_item(tag,content):
        gettext()
        write(content)
        currentitem[0]={}
    def end_item(tag,content):
        items.append(currentitem[0])
        currentitem[0]={}
    def end_link(tag,content):
        if within('item'):
            currentitem[0]['link']=gettext()
    def end_description(tag,content):
        if within('item'):
            currentitem[0]['summary']=clean_entities(gettext())
    def end_title(tag,content):
        text=clean_lf(gettext()).strip()
        if within('item'):
            currentitem[0]['title']=text
        elif parentis('channel'):
            feed['title']=text
            
    tagre=re.compile('([^ \n\t]+)(.*)>(.*)',re.S)
    tagpath=[]
    textbuffer=[[]]
    assumed_encoding='latin-1'
    lines=text.split('<')
    def start_default(tag,content): write(content)
    def end_default(tag,content): pass
    def tag_default(tag,content): pass
    def write(text): textbuffer[0].append(text)
    def gettext():
        text=''.join(textbuffer[0])
        textbuffer[0]=[]
        return unicode(text,assumed_encoding)
    def current_tag(): return tagpath[-1]
    def current_path(): return '/'.join(tagpath)
    def within(tag): return tag in tagpath
    def parentis(tag): return current_tag()==tag
    for k in lines:
        m=tagre.match(k)
        if m:
            (tag,attributes,content)=m.groups()
            if tag.startswith('?'):
                continue
            if tag.startswith('/'):
                tagname=tag[1:]
                handler='end_%s'%tagname
                generic_handler=end_default
                if current_tag() != tagname:
                    pass # Unbalanced tags, just ignore for now.
                del tagpath[-1]
            elif tag.endswith('/'):
                tagname=tag[0:-1]
                handler='tag_%s'%tagname
                generic_handler=tag_default
            else:
                tagname=tag
                handler='start_%s'%tagname
                generic_handler=start_default
                tagpath.append(tagname)
            locals().get(handler,generic_handler)(tagname,content)
        else:
            pass # Malformed line, just ignore.
        
    feed['entries']=items
    return feed

