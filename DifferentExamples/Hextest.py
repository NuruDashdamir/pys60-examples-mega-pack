import appuifw
import time
    
def hex2(val):
  h=''
  hx=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
  c=val/16
  o=val%16
  h=hx[o]+h
  val=c
  while c<>0:
    c=val/16
    o=val%16
    h=hx[o]+h
    val=c
  return h

print hex2(243)

def hexstr(val,l):
  return str(hex2(val)[2:len(hex2(val))]).rjust(l).replace(' ','0')

def hexstr2(val,l):
  h=hex2(val)
  ll=len(h)
  if ll<l:
    return '0'*(l-ll)+h
  return h
  
def hexnum(h):
  return int('0x'+h)
t1=time.clock()
for i in range(0,1000):
  c=hex(i)
print time.clock()-t1

t1=time.clock()
for i in range(0,1000):
  c=hex2(i)
print time.clock()-t1
