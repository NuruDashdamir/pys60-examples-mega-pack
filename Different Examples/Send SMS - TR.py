import appuifw,messaging 

veri=appuifw.query(u"Mesajinizi yazin:", "text") 
num=appuifw.query(u"Numarayi girin:", "text") # numarayi uluslararasi kodu ve basina + koyarak girin (+9)

messaging.sms_send(num,veri)