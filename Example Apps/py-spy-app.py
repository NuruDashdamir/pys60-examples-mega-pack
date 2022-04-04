#! /usr/bin/python

def inline_module_py(str_module,name):
  import sys
  from zlib import decompress
  from imp import new_module
  tmp_module = new_module(name)
  exec decompress(str_module.decode("base64")) in tmp_module.__dict__
  if not name in sys.modules: sys.modules[name] = tmp_module

def inline_module_pyd(str_module,name,tmp_path):
  from os import unlink
  from zlib import decompress
  from imp import find_module, load_module
  tmp_file = file("%s/%s.pyd" % (tmp_path,name),"wb")  
  tmp_file.write(decompress(str_module.decode("base64")))
  tmp_file.close()
  r = find_module(name,[tmp_path])
  load_module(name,*r)
  r[0].close()
  unlink("%s/%s.pyd" % (tmp_path,name))
  

### Start of embedded module hmac ###
str_module = '''eJyNVMGO0zAQvecrRunFhhBBYfdQCSS0QoIDnLgtu1VaO41Zx45sB9L9emzHSey0AnKoXM+bmTfj
N5OxtpPKgDaKiVOWEVrD3v4ZpEL6TQF6i3cZ2E9R0ysBeV7+lEygtuoQr9oDqWAo4LyDY6OQVAQN
GB7BHc4YW/cxBM6yDXxvKGj2TEHWYOyZsBPVRofIlMDhDJ+/frwDQjsqiAYpPK4XhCp+dvQ20FS6
sSdoJem5tWlKymyMtPfB38M3KWiWHXmltY838veF7ZlgZr9HmvK6gCd6LqDVp+BTBEY2dLgJpbuP
1bF1NC9Wjxgb2ZKb5DqO6Wyz0XEoY+t8TiGyN1TF5lLQ3winICbEv0FpmxZodL/QO3B5fArQ23dL
H7rKcc1/DG9vc3ixwGaEnBE3dykibianAtn+Y/iwANJ+WutFQc4j0LXFZSnU/b70OnyNbV60VPBq
Toev9LbsO1IZiibZe1m4KtZo3+SraJaibX3I6gqnBfkYwdtZ7UxsJmUeOa2Ul6V1Gq/90FVMU6s1
86XtOG2pMJR8UkqqAvLRBUNLTWP1I6SB6lfFeHWwc8GEl36ZZ7P4Q+ZR+im7y+pGfjM72Z0ncvMz
29F0inNpUJ7j1JAIO1X6CjgpN+Lg060DTmMQvdsKFzaUhy/cg1pW7Ju/RmrKqFmB1KS6i3zNSpAu
aUOH63lXW/R+XLvlc804R9YrrFB8v909FLDFiYDir5YKBvfMprfKQFGLLcUHPC7yMDL/teQCM/+c
k08ExtkfNfLPcg==
'''
inline_module_py(str_module,"hmac")
### End of embedded moduled hmac ###

### Start of embedded module smtplib ###
str_module = '''eJzNG2tz27jxu34FQk9G5EXm2U5yvainZDx5NJnGl4ztdqZ1XIUSIYtnvkKAcXRt/3t3FwAJkJTs
XG6m59zZFIF9YLFvQHv32Pe1qL5fJPn3PP/Myo1cF/lolGRlUUkmiuU1l+ZTxZun1fLHoyPzSW5K
LsyHRST4D4/Mp3UWLUej+TxK0/mczdiFd3Zy/v7llyUvZVLk3oQ+n/HqM69eJGJZ5DlfSh7rgVMu
yiIX3AIYsfZHA+cxr075qhYW3DIpE55L4b5/EcnoZVUV1QCe54q2HqZXr3la2J+Pa7kGpMkyQl6G
EH2qC8mjOEYIeo6Boob2Lkcj/Dt//+70HGRx9Hj0/PTtq5n3ofqQe6PRu7cvzs7/8fbl/Phv569h
vOLhssjKJOV+5UVAeuaH3wXeBAfeBKNRzFeM58si5nMldF9MGC/S2c9FzoMp8VVxWVc587zwlyLJ
fTUvVFBCVkl+5YsgFGWaSN8DLgLAu8cacbNlGgnBBUMZssWGyXUiWFbEdcrDEQ0yZ0P95kkzUOIU
+BlZs/vb7TtIHFAbsKcOPTgCRMHM50meyPncFzxdTRiud8IycaVx4w+OhCKT5RxHQeD4Z2CU4z7D
MEC7o1F1JeC93yJ3V2nppT/I/l0YngAtRPR7Mq4wwoh6uGVVDQfuVnQs7M5bUTWQ3SW1I6T95sMw
e9aECXBmsdYY+VahG+2yoWzz/yrAxkl8FdSAK7k7/NnbV9E1PyPnvEvQUYoOHPZPpMXil7641TgJ
Wz121ITAUE3ooSWE+qCJgBPpaSbNDm+qRHIfx5th7Y1Snqv3IwWTxxAetDa2RJZpIThR2cZ4qKYE
Hbm8Ao85JBWmOR4Uxta1ArE4TfI+JxINyPOaF8s1vkDf27y6WQMrNHAPpoJ7bcFbCFtmSMw/DJxZ
SOjBDCd35Qgjt4hLaQ0ON4HJx1/GPDO0JGR5QowrwrLatBiymYr1YRlVwkJwcXhJczjpKTuWEEwW
teSkyR0G8CFZITGX2pTtsTd5jDYAIYYIsFWUpHXFGTguF2eDck8UGYc4lF+xG55UMVtzCIghK+tc
sv04zrpi8n66L5567D5DxhXTqeDTrdMyS2IYvn38ZSSmJwNFUS/8auw/y4J/fQjHEzYO4beFtJkw
xfj+H/yv8p/d+5AHAczGyD9hhNn1Xo3mLuqrlH/maBgH9GqFymRp2Bocz7wCf2G/5OuBl3HBxZxj
TCBk2xzGuhASJoyBPUreYK5ZdmMnhGW+4hGIgaMj/vd/mwmwx4jCVXIrOhpl12Hfx8mKlKvxgIcC
GxjN0dGBi45kGyWgKT2nbYdhs0LB5bwVpV5n+6K3PEfs7QfLzDTvrcRm47RYRik+bhEcrCcvpBqK
8pjRwsNVAk50PB0HaBb0pmpeBe6iE9ab0RVYwp4C1b6sWhlrHBfT5FIxfpE8OJxe9iDQ/A1Akku/
vz+kZ8ru/x6lddfm+1ulyoiQ8pEJ83KQYZ3xKlkSHW9IUA0LTcZsz+ru1VNYOishnZVsrHdoCpsx
qGGgIOi4r7hEf5Dkq0IbtYDNYTwr5YalibDYUh5aRUrHv6/AS6EVJLlZooXVIj5hBxMz4+zd87/O
z85PXx6fdHY5WqlJWE4BXFXIAvLACKUVZfBGRBSphQPkOOshhjVZ9ccfoNHf228UcI+LxuBF5M7S
SuSqB+xPf0V3Y4mix618GVxIdlhrLc51hrFLwo5KmB/gSCZ57Q4sIL5fd7V9Cy9DlmMn8gN+FZSv
4mW6sfjdLTfPbKXn4tZBbotH7eR+d7VLBMS9+QhgH3tAfQHs1uxQp41ugok/A0q1Bc+2zW3jy0Cl
OlbvaOuat5Y/dnOL29GVKYeinFV13sSWAEJ9BdHEknpZy2Vm5A5PE4Z10MzzLB/ieR7WnCwCRFmG
gUYWULCDEhHZ0PMcT6sKKUxhXXZVYju+L+6LMWRDPlHDdGXXGhsg5sIhkS50U4JaRQCusVFfncRa
6ijK2cVlT2coIUoEGWCHnWZ4ZqlMBsUBvvTH1cLaMZWlH7oYMOU3wAgTNnVAL/SqqZg3/Z565unc
Brswdc6/lPQ63ahEP/Z6bOyyPZIrGR8y+9FVT5BuGJUlbgiOXjyaXobYGyr9wCWC7mBGU6YP3bxh
jz1fc3CGch1JUjnVeqAsDjZIbHIZLbHYTXEBRQW1uww7GF4U+RjyIykxBKPqosRJmcmTUp2sZI3p
jkS8i6q45nl4u9sAdnSrBDMafBz0GbuymRbF/mFv0HXstkSw7qlTmRDjlS7uwyEVung4fXR5b+bt
e33iCn9rf1WlsxioKVVnD1Hf6vYdvI5qoMun5fn3RfBndgIxmGk71gufKKK9Yt4Ma6Zac46LrR7L
dQXat+EcnNKj0I1tIyVfIWNGJY32dqKhjIWRJoyZ02w87mbj8HbAYWhGPIT3FOxOnzcA06aBq09x
bhuQCqYowdm2YE3vm6putjUiuwEZK77tq71L0XaLOJDA14pDw3yTOPbY8RJ8RYyVPriD01fPD3/8
4QnD8p/5iwh9IfaYJM9tmJPz47FgN0masrjxpwxcByb3wFXIzguhUv2my52sLATkw9bkEIXbTzB1
6Qx9AFVy2MlSGViv+Nrq+Xd7/aHswuuoSFPjOypiV82PO8z01cdB2PYHZq1v21MNGfLmQLBxXt0e
C7DhcqWPE8YfcivIxuCCcPDioI0cWD7xaLnG+gnHXJ73YKPYgrNoAdEZ9h/NvM6pWQTbK9csEgzs
fkOi1DmOwJcl7G8CQJMOuhsO2/qZcEnIBGhlRRrvC7kBCnjAwqIYkEjYn4yDbwT/WLAIdLDOZRfZ
gi+jumsCe+wwYC/BMlhRV4ovbXSqu1VhjiNwY6ll3o2ARwE7x2YWeEqu1NysinSyyEHjGw6JfWIa
u2FFDDrPO/hwe+uS6uhakBWpFTNasUsdMc2zSMJuzJhzEhXSWx83qpdztFD9mAX7h4dFqFsY2Cue
FSD8uAbloIbfhC1qSSsDe80LLEZh07IengEPdkHHYd6lSdDcUfQlvpoxgew2YB8Gizz8ecA8+PfA
Wkd4VRV1KfyDwNZU89NUdR1Jg29i5Jwq/qlO0MdGTJTRkoOeyBvOleth13xzAw6NXAcoBDhUCbvb
VYM3KBBIl2rKljATAycA1R9YSasHhF2QpsC04gaP5xSpDraWjhL4DSoYuperQjvWJSUqaIzK9WE7
lUFSLbv61GR3amkJ7WsJqyVjWeGQVl7czi3ry2aAXqkUNkff/6S37enF8f4/o/1fD/afXLaPH/Yv
vwvGk0Hly/o6p3HNMrWNvqdfeEGIMqoGknDiUwCEOg69yEJMhFvANhkeaiQY88Y6ijRuR0Oho8P6
YZcS6w+3aTH+GE1Wy+lnr71wfRfWZh1sO7KQdQQR5IvMdSZSlNKqTO1ErrNMhAOz8AHAbJGNlael
xkjZI+U2DudW/lV6atbdEkg62xFcdo9MbBiVwno4zbPA8qIo7wCG02ywLEp0B1qdp04Kyj4ElLYW
IvUSG5DUirfDu55P7qMTt929dXHAvwf4WxUKGkkwLEbkEb3mq9N3J1Ms5fFAxG8Pj/RJMJu0JIKv
kPey1J1zOrz9IwoAWfQm3vm7odUT18FvWzudJNHaB24hGOp0W6SbJCOq7VnyUKl3wJoOH2LE9p6F
aihjfPj40bamVXucPoCi71c+gcTbozMn19Q0P13sH00vkSr2hfpeiTDAjuFoHzV6utAbGm77Sp9c
mneoNb5akr2F7fCNkLElq43xY6BIXPTuPhgN+FytNkDEPa7F+bdqGg7tsSi8DiMVcRHVTNG2qsUv
Zb6VE+wgYtI6VlDjppG4v6+yBEFpggZkn6M0iRO5cTqLbhkI1H7bakyRj1kw5MqrOjV5bruWtLhK
zGJgDqRIeNyMGZa1JuuW1BKC2TyLH/vLNeRMPL/iO+Dwp5kHiqevTsXcujrVjHdVQVdKM0LfxGa8
DBe+Pjl+7ht6k5ZEAJX/lzi5AtzdglE3WpyrXoaGuvHlmTjTWXGZRiChnWscxO7dFx8O1P/kAhWG
Dh6LdIMRC4b5+7fHb37G7hQ9eO7g89Pjk/nJi8c4js/78NyZ8vbdXxQ8PXj9E4b25Ft3f9uI0J5/
DzaG9ZmLf3RwwH6atSA+pvv45ujJk6DvkvRJCDXZTL5GXabBpNCmQA52K17agMbTtjeJLHK9Y2RF
3KRbKuvs7mmDsr0ppyybrhYCIM8FNj4InyoR1f0+c1Rgkd1j7l2lpt5sjxYMDtGygWzp+LujgNOt
AofaW4QqVG05QBWqeE1tylZVkWEBsuJVxfG4w0KToodqxzR4qO826nIH6vK6Kgss2KF8AdMzVfIN
j66ti3F7UHRhxQrEFUosywqw2qrhK02uOTMKbV2AMRzMcT3Ye7twzGBimczEUv9LWyQvsI7KsINs
iv6eYIC1cZqiiTpboAcHzq31CBSVHRZ7BtPONJvaV2SHlnrozek0sXX7wEDNXPcweInEsT+dZSOU
N3GBh6+TAInHBw+HGhXwmg5wVOsfCmo8etjYgubxuAfnnpK6DfjdTHfjEU7puVc7yRqWFSnNVwqq
twrLY5s4tSt43M4Vqe+3cuXRSSLFnhbppBOlFGs6CAXDm4657cNH/U1vXeTQTczfvKWasza+G+52
ia0fpgYd+M8FeL5EUj902AesijqPQ6+f4aOfB/u9OHoIDge0/bLbt4QBsoCOqxf1cgl+FLKvcQfg
603m6yU+ZGBN8idkVEmZCp3/XfONdT8O8ipeSeuFFSC1tVGi2dXGs/Pj0/Pzt2euCNV1uoHLaO2l
UX3JRqgCP1TXbjVPLTOdi53WHRLnSq+NQ99W7QPqxVl3Xv3uXCM/e8HuRY62JUGxdI7p+QTiKD0I
ffsbJ83bUr1vrFTXz51i/o+Ssv1fMjYzT+U8IBcK+/37C9u6F3vsdZZlz9iN6o3jdy6euacuatZQ
YjX+0yKR48uZVZE522DyxrFIfuXjgQW2TJtLAR5OnWFg+GjOuz66UsR8otBHabmjL3fBr6ZaOeDA
1pGiWiraYhlsZ/QOwNS9cWz3bT+Ms7+u0W6nZRl2ywgnV2LmHqQmIsnBL+VL7rc2RN+OCs+oYjzH
547QzUzUEfM8fEZmRoeCK0lLtTeoy4YwE8cwe/HRt6QVqIup7ZvDAdUwq75A5Jczi7AtBLrdr2cG
sxl+NIwHXT23SohKSR5PM+j0bOD7H3fbyP43UxpudmlYv131bfrUaZt1XMMeIIdi4qpQ5y0oiJya
HYsCoii+Rhmg1vcbJWoxo1uu/tuXpLZcjuodT9uBxSkYtt/S235VsndFsmX4E6Qxg9/s0GEYx7uH
3s13PUZ77BwqNa07KobpBGiCd7nAVrCSw6+pqUKSTj3xbEqEAIvnWlN1NBmlN9FGEBKBB2HNPe5w
lODleLzxgN9ahDRnPgcy+Xyur3iZr0durG5UCW4CDE/9sRe2EaGQcVFL/ZUYNQOz7SnzetFaT09y
68ZZcwJFk9EfoTmBXDVN7xX81ahkobyJNXpeeOY7fuOJPpPXTc2XuaQaVogIu2F4fZDO1v/1YqoC
iLpnpNvwvZty5pbcAM/dtgW+dVXHvTSlCOHvBzTX5vJE8Yeu5QqYg61zo5H5IhE5EnVl3Ldu5QfW
cNj5RsBhZ1DnREbGEyNPfQ3WmktKHIz+B+Z+5Yg=
'''
inline_module_py(str_module,"smtplib")
### End of embedded moduled smtplib ###

### Start of embedded module ConfigParser ###
str_module = '''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
'''
inline_module_py(str_module,"ConfigParser")
### End of embedded moduled ConfigParser ###

### Start of embedded module MimeWriter ###
str_module = '''eJylVE2P2yAQvftXIKRoidZ2k2uqnHpuT5V6SCxE4nFDiwEB7m7+fQE7OLj7JZWLwzDz5vHmBd5r
ZRzqeQ9OKWGLglImBKVojw74qw//MNyBwU1RnAWzFs2xXVEgv1roEKVcckcpsSC6EnV6vYtnYYVQ
TTvtETu9iF6AtWBsaNbMaKxtx4MJ7jdcS/SHiQFKpA10/Hm/uWsguIQAETNqqwV3BB8lXqeMpwsX
MOUx2SKp3Lg7VNtm53uKefuBok1Ws5lLOmUQR1wiw+RPINsSCZAkpq3vCCfSB9543jjsMXpMsdo6
wzWZ+cebhUx/q/qX4jdMXxNCmRI+zesVTnYRNNamDN5NCuZssmnUXFowjmzKCDjTAGHhrTqmNciW
jEVpmp0Y7GVKiQN9wRv1U3BUvBTJMNcfMox1zLiTaq+TYc7uqoNXBLduf2iSa7Z3rcOsJOthclaY
WszPLxiRfLfx+4gePh8lWtn9Ea/sET+gFSJ3IAu2s4/xFyUdSFd99zB4JjjSGj+L4ky2pQw3xRY+
N+AGI1POQqB+EI7rXCk7nEYqJzXIlpnr/puS70k34t8qvDrpp9c0PSX1+aKUhZRHXuY5zw4ngp+C
cW/Usnn8uw4E3zp4YXNq68bjxKu8h7KYRBJOwrMLjN42bhhDVUXSuTTj//OVAdH4oE6PZgC76+tP
/rNvVcXOfv0FsBy4IA==
'''
inline_module_py(str_module,"MimeWriter")
### End of embedded moduled MimeWriter ###

del(str_module,inline_module_py,inline_module_pyd)

### Start of main script ###
import telephone, e32, appuifw, camera, graphics, audio, messaging
import os, socket, time, smtplib, MimeWriter, ConfigParser, types, StringIO

False = 0
True = 1 

try:
    import mmsmodule
    MMS_send = mmsmodule.mms_send
except:
    MMS_send = messaging.mms_send


Languages = ("es","en")

Default_lang = "en"

Translations = {
  "$_lang_name":{
      "es":u"Espa\u00f1ol",
      "en":u"English"},
  "$_date_time_format":{
      "es":"%d/%m/%Y %H:%M:%S",
      "en":"%m/%d/%Y %H:%M:%S"},
  "M_yes":{
      "es":u"Si",
      "en":u"Yes"},
  "M_no":{
      "es":u"No",
      "en":u"No"},
  "M_language":{
      "es":u"Idioma",
      "en":u"Language"},
  "M_start_pause":{
      "es":u"Inicio/Pausa",
      "en":u"Start/Pause"},
  "M_a_v_set":{
      "es":u"Ajustes Audio/Video",
      "en":u"Audio/Video settings"},
  "M_audio":{
      "es":u"Audio",
      "en":u"Audio"},
  "M_video":{
      "es":u"Video",
      "en":u"Video"},
  "M_photo":{
      "es":u"Foto",
      "en":u"Photo"},
  "M_general_set":{
      "es":u"Ajustes generales",
      "en":u"General settings"},
  "M_alarm":{
      "es":u"Alarma",
      "en":u"Alarm"},
  "M_presence":{
      "es":u"Presencia",
      "en":u"Presence"},
  "M_actions":{
      "es":u"Acciones",
      "en":u"Actions"},
  "M_email":{
      "es":u"E-mail",
      "en":u"E-mail"},
  "M_sms":{
      "es":u"SMS",
      "en":u"SMS"},
  "M_mms":{
      "es":u"MMS",
      "en":u"MMS"},
  "M_call":{
      "es":u"Llamada",
      "en":u"Call"},
  "M_store":{
      "es":u"Archivar",
      "en":u"Store"},
  "M_file":{
      "es":u"Fichero",
      "en":u"File"},
  "M_internet_ap":{
      "es":u"Acceso internet",
      "en":u"Internet access"},
  "M_exit":{
      "es":u"Salir",
      "en":u"Exit"},
  "M_flash":{
      "es":u"Flash",
      "en":u"Flash"},
  "M_zoom":{
      "es":u"Zoom",
      "en":u"Zoom"},
  "M_exposure":{
      "es":u"Exposici\u00f3n",
      "en":u"Exposure"},
  "M_balance":{
      "es":u"Balance",
      "en":u"Balance"},
  "M_resolution":{
      "es":u"Resoluci\u00f3n",
      "en":u"Resolution"},
  "M_enable":{
      "es":u"Activar",
      "en":u"Enable"},
  "M_disable":{
      "es":u"Desactivar",
      "en":u"Disable"},
  "M_directory":{
      "es":u"Directorio",
      "en":u"Directory"},
  "M_counter":{
      "es":u"Contador",
      "en":u"Counter"},
  "M_interval":{
      "es":u"Int\u00e9rvalo",
      "en":u"Interval"},
  "M_phone_numbers":{
      "es":u"Tel\u00e9fonos",
      "en":u"Phone nums."},
  "M_attach_img":{
      "es":u"Adjuntar imagen",
      "en":u"Attach image"},
  "M_targets":{
      "es":u"Destinos",
      "en":u"Targets"},
  "M_sender":{
      "es":u"Remitente",
      "en":u"From"},
  "M_port":{
      "es":u"Puerto",
      "en":u"Port"},
  "M_host_smtp":{
      "es":u"Servidor",
      "en":u"Host"},
  "M_left":{
      "es":u"Izquierda",
      "en":u"Left"},
  "M_top":{
      "es":u"Arriba",
      "en":u"Top"},
  "M_right":{
      "es":u"Derecha",
      "en":u"Right"},
  "M_bottom":{
      "es":u"Abajo",
      "en":u"Bottom"},
  "M_thresold":{
      "es":u"Umbral",
      "en":u"Thresold"},
  "M_pixels":{
      "es":u"Pixels",
      "en":u"Pixels"},
  "M_grid_size":{
      "es":u"Precisi\u00f3n",
      "en":u"Accuracy"},
  "M_period":{
      "es":u"Periodo",
      "en":u"Period"},
  "M_sound":{
      "es":u"Sonido",
      "en":u"Sound"},
  "M_start_time":{
      "es":u"H. Inicio",
      "en":u"Start time"},
  "M_stop_time":{
      "es":u"H. Fin",
      "en":u"Stop time"},
  "M_start":{
      "es":u"Inicio",
      "en":u"Start"},
  "M_seconds":{
      "es":u"Segundos",
      "en":u"Seconds"},
  "M_motion_detected":{
      "es":u"Se ha detectado movimiento",
      "en":u"Motion detected"},
  "M_no_motion_detected":{
      "es":u"No se ha detectado movimiento en %d segundos",
      "en":u"No motion detected in %d seconds"},
  "M_pause":{
      "es":u"Pausa",
      "en":u"Pause"},
  "M_delayed_start":{
      "es":u"Inicio temporizado",
      "en":u"Delayed start"},
  "M_seconds_to_start":{
      "es":u"Faltan %d segundos  ",
      "en":u"%d seconds to start  "},
  "M_pyspy_alert":{
      "es":u"Alerta de Pyspy !",
      "en":u"Pyspy alert !"}
  }


def _(key):
    return Translations[key].get(config.get("language","lang",Default_lang),key)
    

class Motion:

    def __init__(self,square=(0,0,160,120),thresold=4000,max_pixels=25,step = 4):
        self.buffer=[]
        self.square = square
        self.thresold = thresold
        self.max_pixels = max_pixels
        self.step = step
        
    def reset(self):
        self.buffer=[]
        
    def check_motion(self,image):
        left,top,right,bottom =  self.square
        width = right - left
        height = bottom - top    
        first = False
        pixcount = 0
        max_left = right
        max_right = left
        max_top = bottom
        max_bottom = top
        
        if (len(self.buffer) <> width) or (len(self.buffer[0]) <> height):
            self.reset()
            for x in xrange(width): # remake buffer
                self.buffer.append([0] * height)
            first = True

        for y in xrange(0,height,self.step):
            for x in xrange(0,width,self.step):
                r,g,b = image.getpixel((left+x,top+y))[0]
                gray = r * 30 + g * 59 + b * 11
                if abs(gray - self.buffer[x][y]) > self.thresold:
                    pixcount+=1
                    if (left + x) < max_left:
                        max_left = left + x
                    if (left + x) > max_right:
                        max_right = left + x
                    if (top + y) < max_top:
                        max_top = top + y
                    if (top + y) > max_bottom:
                        max_bottom = top + y                    
                self.buffer[x][y] = gray
        if first or pixcount == 0:
            return (0,(0,0,0,0))
        return (pixcount,(max_left,max_top,max_right,max_bottom))
    
         
    def get_motion(self,mark = False):
        im = camera.take_photo(mode = "RGB", size = scan_res, flash = "none",position = 0)
        chg_pixels, chg_area = self.check_motion(im)
        im.rectangle(self.square, width = 1, outline = (0,0,255))
        if chg_pixels > self.max_pixels:
            if mark:
                im.rectangle(chg_area, width = 1, outline = (255,0,0))
            return (im,True)
        else:
            return (im,False)
        
class Config(ConfigParser.ConfigParser):

    def __init__(self,file):
        ConfigParser.ConfigParser.__init__(self)
        self.config_file = file
        self.read(self.config_file)
        
    def load(self):
        from os.path import exists
        if  exists(self.config_file):
            self.read(self.config_file)
            return True
        return False
        
    def save(self):
        f = file(self.config_file,"w")
        self.write(f)
        f.close()
        
    def update_section(self,section):
        if not section in self.sections():
            self.add_section(section)

    def get(self,section,option,default=None):
        try:
            st = ConfigParser.ConfigParser.get(self,section,option)
        except (ConfigParser.NoSectionError,ConfigParser.NoOptionError):
            return default
           
        if st.startswith('"'):
            return st.strip('"')
        if "." in st:
            return float(st)
        return int(st)

    def set(self,section,option,value):
        if isinstance(value,types.StringTypes):
            ConfigParser.ConfigParser.set(self,section,option,'"%s"' % value)
        else:
            ConfigParser.ConfigParser.set(self,section,option,str(value))
            
def get_day_seconds():
    now = time.time()
    return now - time.mktime(time.localtime(now)[0:3] + (0,) * 6)

def refresh_motion():
    left = config.get("video","left",0)
    top = config.get("video","top",0)
    right = config.get("video","right",scan_res[0] - 1)
    bottom = config.get("video","bottom",scan_res[1] - 1)
    motion.square = (left,top,right,bottom)
    motion.thresold = config.get("video","thresold",4000)
    motion.max_pixels = config.get("video","max_pixels",25)
    motion.step = config.get("video","step",4)
    
def quit():
    global running
    config.save()
    running = False
    
def pause_cb():
    global pause, pause_timer
    res=appuifw.popup_menu([_("M_start"),_("M_pause"),_("M_delayed_start")],_("M_start_pause"))    
    if res == 0:
        pause = False
    elif  res == 1:
        pause = True
        pause_timer = -1 # Abort count down
    elif res == 2:
        r = appuifw.query(u"Segundos","number",10)
        if r <> None:
            pause_timer = r
            pause = True    
    

def set_audio_cb():
    def save_hook(f):
        config.set("audio","enable",int(f[0][2][1]))
        config.set("audio","file",str(f[1][2]))
        config.save()
        load_sound()
        return True
    enable = config.get("audio","enable",0)
    aufile = config.get("audio","file","").decode()
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_file"),"text",aufile)]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    


def set_language_cb():
    lnames=[]
    for l in Languages:
        lnames.append(Translations["$_lang_name"][l])
    res=appuifw.popup_menu(lnames,_("M_language"))   
    if res <> None:
        config.set("language","lang",Languages[res])
        config.save()
        load_mainmenu()


def set_alarm_cb():
    def save_hook(f):
        config.set("alarm","enable",int(f[0][2][1]))
        config.set("alarm","start",int(f[1][2]))
        config.set("alarm","stop",int(f[2][2]))
        config.save()
        return True

    enable = config.get("alarm","enable",0)
    start = float(config.get("alarm","start",0))
    stop = float(config.get("alarm","stop",86399))
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_start_time"),"time",start),
              (_("M_stop_time"),"time",stop)]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    
    
def set_presence_cb():
    def save_hook(f):
        config.set("presence","enable",int(f[0][2][1]))
        config.set("presence","start",int(f[1][2]))
        config.set("presence","stop",int(f[2][2]))
        config.set("presence","period",int(f[3][2]))
        
        config.save()
        return True

    enable = config.get("presence","enable",0)
    start = float(config.get("presence","start",0))
    stop = float(config.get("presence","stop",86399))
    period = config.get("presence","period",1200)
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_start_time"),"time",start),
              (_("M_stop_time"),"time",stop),(_("M_period"),"number",period)]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    
    
def set_sms_cb():
    def save_hook(f):
        config.set("sms","enable",int(f[0][2][1]))
        config.set("sms","numbers",str(f[1][2]))
        config.set("sms","interval",int(f[2][2]))
        config.save()
        return True

    enable = config.get("sms","enable",0)
    numbers = config.get("sms","numbers","").decode()
    interval = config.get("sms","interval",3600)
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_phone_numbers"),"text",numbers),
              (_("M_interval"),"number",interval)]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    
    
def set_ap_cb():
    apid = socket.select_access_point()
    if apid <> None:
        config.set("internet","apid",apid)
        set_ap()

def set_call_cb():
    def save_hook(f):
        config.set("call","enable",int(f[0][2][1]))
        config.set("call","numbers",str(f[1][2]))
        config.set("call","interval",int(f[2][2]))
        config.save()
        return True

    enable = config.get("call","enable",0)
    numbers = config.get("call","numbers","").decode()
    interval = config.get("call","interval",3600)
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_phone_numbers"),"text",numbers),
              (_("M_interval"),"number",interval)]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()        

def set_photo_cb():
    def save_hook(f):
        config.set("photo","flash",int(f[0][2][1]))
        config.set("photo","zoom",int(f[1][2]))
        config.set("photo","exposure",int(f[2][2][1]))
        config.set("photo","balance",int(f[3][2][1]))
        config.set("photo","resolution",int(f[4][2][1]))
        config.save()
        return True

    flash_modes = []
    for x in camera.flash_modes():
        flash_modes.append(x.decode())
    exposure_modes = []
    for x in camera.exposure_modes():
        exposure_modes.append(x.decode())
    balance_modes = []
    for x in camera.white_balance_modes():
        balance_modes.append(x.decode())
    image_sizes = []
    for x in camera.image_sizes():
        image_sizes.append(u"%sx%s" % x)
        
    flash = config.get("photo","flash",0)
    zoom = config.get("photo","zoom",0)
    exposure = config.get("photo","exposure",0)
    balance = config.get("photo","balance",0)
    resolution = config.get("photo","resolution",0)
    fields = [(_("M_flash"),"combo",(flash_modes,flash)),(_("M_zoom"),"number",zoom),
              (_("M_exposure"),"combo",(exposure_modes,exposure)),
              (_("M_balance"),"combo",(balance_modes,balance)),
              (_("M_resolution"),"combo",(image_sizes,resolution))]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    

def set_storage_cb():
    def save_hook(f):
        config.set("storage","enable",int(f[0][2][1]))
        config.set("storage","directory",str(f[1][2]))
        config.set("storage","counter",int(f[2][2])) 
        config.set("storage","interval",int(f[3][2]))
        config.set("storage","resolution",int(f[4][2][1]))
        config.save()
        return True

    image_sizes = []
    for x in resolutions:
        image_sizes.append(u"%sx%s" % x)

    enable = config.get("storage","enable",0)
    directory = config.get("storage","directory","E:\\Images").decode()
    counter = config.get("storage","counter",0)
    interval = config.get("storage","interval",60)
    resolution = config.get("storage","resolution",0)
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_directory"),"text",directory),
              (_("M_counter"),"number",counter),(_("M_interval"),"number",interval),
              (_("M_resolution"),"combo",(image_sizes,resolution))]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    

def set_mms_cb():
    def save_hook(f):
        config.set("mms","enable",int(f[0][2][1]))
        config.set("mms","numbers",str(f[1][2]))
        config.set("mms","interval",int(f[2][2]))
        config.set("mms","resolution",int(f[3][2][1]))
        config.save()
        return True
    image_sizes = []
    for x in resolutions:
        image_sizes.append(u"%sx%s" % x)
    enable = config.get("mms","enable",0)
    numbers = config.get("mms","numbers","").decode()
    interval = config.get("mms","interval",3600)
    resolution = config.get("mms","resolution",0)
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_phone_numbers"),"text",numbers),
              (_("M_interval"),"number",interval),(_("M_resolution"),"combo",(image_sizes,resolution))]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    

def set_email_cb():
    def save_hook(f):
        config.set("email","enable",int(f[0][2][1]))
        config.set("email","host",str(f[1][2]))
        config.set("email","port",int(f[2][2]))
        config.set("email","from",str(f[3][2]))
        config.set("email","to",str(f[4][2]))
        config.set("email","interval",int(f[5][2]))
        config.set("email","attach",int(f[6][2][1]))
        config.set("email","resolution",int(f[7][2][1]))
        config.save()
        return True
    image_sizes = []
    for x in resolutions:
        image_sizes.append(u"%sx%s" % x)
    enable = config.get("email","enable",0)
    host = config.get("email","host","localhost").decode()
    port = config.get("email","port",25)
    sender = config.get("email","from","nobody@mydomain.com").decode()
    targets = config.get("email","to","nobody@mydomain.com").decode()
    interval = config.get("email","interval",3600)
    attach = config.get("email","attach",0)
    resolution = config.get("email","resolution",0)
    fields = [(_("M_enable"),"combo",([_("M_no"),_("M_yes")],enable)),(_("M_host_smtp"),"text",host),
              (_("M_port"),"number",port),(_("M_sender"),"text",sender),
              (_("M_targets"),"text",targets),(_("M_interval"),"number",interval),
              (_("M_attach_img"),"combo",([_("M_no"),_("M_yes")],attach)),
              (_("M_resolution"),"combo",(image_sizes,resolution))]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()    

def set_video_cb():
    def save_hook(f):
        left,top,right,bottom = (int(f[0][2]),int(f[1][2]),int(f[2][2]),int(f[3][2]))
        config.set("video","left",left)
        config.set("video","top",top)
        config.set("video","right",right)
        config.set("video","bottom",bottom)
        config.set("video","thresold",int(f[4][2]))
        config.set("video","max_pixels",int(f[5][2]))
        config.set("video","step",int(f[6][2]))
        config.save()
        refresh_motion()
        return True
    
    left,top,right,bottom = motion.square
    thresold = motion.thresold
    max_pixels = motion.max_pixels
    step = motion.step
    
    fields = [(_("M_left"),"number",left),(_("M_top"),"number",top),(_("M_right"),"number",right),
              (_("M_bottom"),"number",bottom),(_("M_thresold"),"number",thresold),
              (_("M_pixels"),"number",max_pixels),(_("M_grid_size"),"number",step)]
    form = appuifw.Form(fields)
    form.save_hook = save_hook
    form.execute()

def get_datetime_str():
    return time.strftime(_("$_date_time_format")).decode()

def check_alarm():
    if not config.get("alarm","enable",0):
        return
    ds = get_day_seconds()
    if ds > config.get("alarm","start",0) and ds < config.get("alarm","stop",0):
        body = u"[%s] %s" % (get_datetime_str(),_("M_motion_detected"))
        check_storage()
        check_email(body)
        check_sms(body)
        check_mms(body)
        check_call()

def check_presence():
    global presence_timer
    if not config.get("presence","enable",0):
        return
    ds = get_day_seconds()
    if ds < config.get("presence","start",0) or ds > config.get("presence","stop",0) or presence_timer == 0:
        presence_timer = time.time()
        return

    if (time.time() - presence_timer > config.get("presence","period",3600)):
        presence_timer = time.time()
        body = u"[%s]"  % get_datetime_str() + _("M_no_motion_detected") % config.get("presence","period",3600)
        check_storage()
        check_email(body)
        check_sms(body)
        check_mms(body)
        check_call()

def check_mms(body):
    global mms_timer
    if not config.get("mms","enable",0):
        return
    if time.time() - mms_timer <  config.get("mms","interval",3600):
        return
    mms_timer = time.time()    
    resolution = resolutions[config.get("mms","resolution",0)]
    img = take_photo(resolution)
    fname = "%s\\img%d.jpg" % (tmp_dir,time.time()) 
    img.save(fname)
    for number in config.get("mms","numbers").split():
        mmsmodule.mms_send(unicode(number),unicode(body),unicode(fname))
    os.unlink(fname)
        
def check_email(body):
    global email_timer
    if not config.get("email","enable",0):
        return
    if time.time() - email_timer <  config.get("email","interval",3600):
        return
    email_timer = time.time()    
    fromaddr = "<%s>" % config.get("email","from")
    toaddr = config.get("email","to").split()
    message = StringIO.StringIO()
    writer = MimeWriter.MimeWriter(message)
    writer.addheader('Subject', _("M_pyspy_alert"))
    writer.addheader('From',fromaddr)
    writer.addheader('To',",".join(["<%s>" % target for target in toaddr]))
    writer.addheader('MIME-Version',"1.0")
    writer.startmultipartbody('mixed',boundary = "----------_=_NextPart_%012d" % time.time())
    
    # start off with a text/plain part
    part = writer.nextpart()
    p_body = part.startbody('text/plain')
    p_body.write(body)
    
    if config.get("email","attach",False):
        resolution = resolutions[config.get("email","resolution",0)]
        img = take_photo(resolution)
        fname = "%s\\img%d.jpg" % (tmp_dir,time.time()) 
        img.save(fname)
        part = writer.nextpart()
        part.addheader('Content-Transfer-Encoding', 'base64')
        part.addheader('Content-Disposition','inline; filename="image.jpg"')        
        p_body = part.startbody('image/jpeg; name="image.jpg"')
        p_body.write(file(fname,"rb").read().encode("base64"))
        os.unlink(fname)
    # end of parts
    writer.lastpart()

    smtp = smtplib.SMTP(config.get("email","host"),config.get("email","port"))
    smtp.sendmail(fromaddr, toaddr, message.getvalue())
    smtp.quit()    
    
def check_sms(body):
    global sms_timer
    if not config.get("sms","enable",0):
        return
    if time.time() - sms_timer <  config.get("sms","interval",3600):
        return
    sms_timer = time.time()
                                
    for number in config.get("sms","numbers").split():
        messaging.sms_send(number,body)
        
def check_call():
    global call_timer
    if not config.get("call","enable",0):
        return
    if time.time() - call_timer <  config.get("call","interval",3600):
        return
    call_timer = time.time()
                                
    for number in config.get("call","numbers").split():
        telephone.dial(number)
        e32.ao_sleep(15)
        try:
          telephone.hang_up()
        except:
          pass
        e32.ao_sleep(5)

def check_storage():
    global storage_timer
    if not config.get("storage","enable",0):
        return
    if time.time() - storage_timer <  config.get("storage","interval",60):
        return
    storage_timer = time.time()   
    
    directory = config.get("storage","directory","E:\\Images")
    counter = config.get("storage","counter",0)
    resolution = resolutions[config.get("storage","resolution",0)]
    img = take_photo(resolution)
    img.save("%s\\img%05d.jpg" % (directory,counter))
    counter += 1
    config.set("storage","counter",counter)

def take_photo(desired_size, position = 0):
    global last_photo
    img = last_photo
    if img == None:
        flash = camera.flash_modes()[config.get("photo","flash",0)]
        zoom = config.get("photo","zoom",0)
        exposure = camera.exposure_modes()[config.get("photo","exposure",0)]
        balance = camera.white_balance_modes()[config.get("photo","balance",0)]
        resolution = camera.image_sizes()[config.get("photo","resolution",0)]
        img = camera.take_photo(mode="RGB", size=resolution, flash=flash, zoom=zoom,
                                exposure=exposure, white_balance=balance, position=position) 
        last_photo = img

    if img.size > desired_size:
        img = img.resize(desired_size,keepaspect=1)  
    img.text((10,img.size[1]-25),get_datetime_str(),font=u"LatinBold19",fill=(255,255,0))
    return img
    
def set_ap():
    apid = config.get("internet","apid",None)
    if apid == None:
        socket.set_default_access_point(None)
    else:
        ap = socket.access_point(apid)
        socket.set_default_access_point(ap)
        
def load_sound():
    global snd
    try:
        snd = audio.Sound.open(config.get("audio","file",""))
    except:
        snd = None

def load_mainmenu():
    appuifw.app.menu = [(_("M_start_pause"),pause_cb),
                        (_("M_general_set"),
                        ((_("M_alarm"),set_alarm_cb),
                         (_("M_presence"),set_presence_cb),
                         (_("M_language"),set_language_cb)
                        )),
                        (_("M_a_v_set"),
                        ((_("M_audio"),set_audio_cb),
                         (_("M_video"),set_video_cb),
                         (_("M_photo"),set_photo_cb)
                        )),
                        (_("M_actions"),
                        ((_("M_email"),set_email_cb),
                         (_("M_sms"),set_sms_cb),
                         (_("M_mms"),set_mms_cb),
                         (_("M_call"),set_call_cb),
                         (_("M_store"),set_storage_cb)
                        )),
                        (_("M_internet_ap"),set_ap_cb),
                        (_("M_exit"),quit)]        
    
   
running = True   
pause = True
snd = None
pause_timer = 0
storage_timer = 0
sms_timer = 0
mms_timer = 0
email_timer = 0
call_timer = 0
presence_timer = 0
last_motion_check = 0
tmp_dir = "D:\\system\\temp" 
last_photo = None
resolutions=((160,120),(320,240),(480,360),(640,480),(800,600),(1024,768),(1600,1200))
scan_res = min(camera.image_sizes())
sections = ("language","audio","video","photo","alarm","presence","email","sms","mms","call","storage","internet")

config = Config("C:\\system\\data\\pyspy.ini")
config.load()
for section in sections:
    config.update_section(section)

motion = Motion(square=(0,0,160,120), thresold=4000, max_pixels=25, step=4)
refresh_motion()

appuifw.app.exit_key_handler = quit
 
load_sound()
set_ap()
cv=appuifw.Canvas()
appuifw.app.body=cv
load_mainmenu()


while running: 
    if pause:
        while running and pause:
            if pause_timer > 0:
                while pause_timer > 0 and running and pause:
                    cv.clear()
                    cv.text((10,50),_("M_seconds_to_start") % pause_timer)
                    e32.ao_sleep(1)
                    pause_timer -= 1
                if pause_timer == 0: pause = False
                pause_timer = 0    
            e32.ao_sleep(.2)
        continue 
    if (time.time() - last_motion_check) > 5:
        motion.reset()
    last_motion_check = time.time()
    im, stat = motion.get_motion(mark = True)
    if stat:
        if snd <> None  and config.get("audio","enable",0) and (snd.state() & audio.EOpen):
            snd.play()
        check_alarm()
        presence_timer = time.time()
        e32.reset_inactivity()
    check_presence()
    last_photo = None
    cv.blit(im)
    e32.ao_sleep(.2) # Lets relax your phone ;-)
    
if snd:
    snd.close()
        
        
        
    
