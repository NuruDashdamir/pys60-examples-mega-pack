# Timer module by smart4n
class Timer:
  def __init__(s):
    import time
    s.time=time
    s.start_hour=s.time.localtime()[3]
    s.start_min=s.time.localtime()[4]
    s.start_sec=s.time.localtime()[5]
    
  def endtimer(s):
    s.end_hour=s.time.localtime()[3]
    s.end_min=s.time.localtime()[4]
    s.end_sec=s.time.localtime()[5]
    temp2=s.end_hour*3600+s.end_min*60+s.end_sec
    temp1=s.start_hour*3600+s.start_min*60+s.start_sec
    time_total=temp2-temp1
    if time_total>=0:
      hour=time_total/3600
      min=(time_total%3600)/60
      sec=time_total%60
    else:
      time_total=time_total+86400
      hour=time_total/3600
      min=(time_total%3600)/60
      sec=time_total%60
    if min<10:
      min='0'+str(min)
    else:
      min=str(min)
    if sec<10:
      sec='0'+str(sec)
    else:
      sec=str(sec)
    if hour<10:
      hour='0'+str(hour)
    else:
      hour=str(hour)
    return str(hour+':'+min+':'+sec)