import re
varname=re.compile('\$[a-zA-Z]+[0-9a-zA-Z]*')
kw=['include','new']
def parse_php(php):
  index={}
  m=varname.search(php)
  while m:
    index[m.start()]=('variable',m.end())
    m=varname.search(php,m.end())
  for w in kw:
    for o in re.finditer(w,php):
      index[o.start()]=('keyword',o.end())
  k=index.keys()
  k.sort()
  y=0
  i2=[]
  for i in k:
    if y<i:
      i2.append(('plain',php[y:i]))
    x=index[i]
    i2.append((x[0],php[i:x[1]]))
    y=x[1]
  if y!=len(php):
    i2.append(('plain',php[y:]))
  return i2

if __name__=='__main__':
  PHP='''include "php.classes/website.class.php";
$w=new Website();
$w->enable("stats");
$w->public_page();
$w->if_admin();
$w->display_page();'''

  p=parse_php(PHP)
  for e in p:
    print e

a=raw_input()