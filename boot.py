import connectwifi,localtime
import _thread,time
import machine
from machine import Pin, SPI
import ssd1306
import urequests
import xmlConvert
import font

ts = ''
ts2= ''
weather_1=''
tem_1=''
tem_2=''

debug = False

lock = _thread.allocate_lock()
def time_thread():
  localtime.sync_ntp()
  while True:
    global ts
    global ts2
    
    t = localtime.getLocalTime()
    if lock.locked():
      pass
    else:
      lock.acquire()
      ts = '{}-{}-{}'.format(t[0],t[1],t[2])
      s = t[6]
      m = t[5]
      h = t[4]
      if int(s)<10:
        s = '0{}'.format(s)
      if int(m)<10:
        m = '0{}'.format(m)
      if int(h)<10:
        h = '0{}'.format(h)
      ts2 = '{}:{}:{}'.format(h,m,s)
      lock.release()
    global debug
    if debug:
      break
  print('结束time_thread')
   
def weather_thread():
  url = 'http://flash.weather.com.cn/wmaps/xml/jixi.xml'
  global weather_1
  global weather_2
  global tem_1
  global tem_2
  while True:
    response = urequests.get(url)
    xml = (response.content).decode('utf-8')
    result = xmlConvert.xml2DictInList(xml)
    
    for i in result:
      if 'cityname' in i.keys():
        if i['cityname'] == '密山市':
          if lock.locked():
            pass
          else:
            lock.acquire()
            weather_1 = i['stateDetailed']#天气
            tem_1 = i['tem1']#高
            tem_2 = i['tem2']#低
            lock.release()
            print('天气：{}'.format(i['stateDetailed']))
            #print("气温：{}℃ ~ {}℃".format(i['tem2'],i['tem1']))
            #print('当前气温：{}℃，湿度：{}'.format(i['temNow'],i['humidity']))
            #print('风力：{}'.format(i['windState']))
    
     
    
    global debug
    if debug:
      break  
    time.sleep(1800)
  print('结束weather_thread')
def lcd_thread():
  
  spi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
  display = ssd1306.SSD1306_SPI(128,64,spi,Pin(25),Pin(26),Pin(27))
  display.poweron()
  display.init_display()
  
  global ts
  global ts2
  global weather_1
  global tem_1
  global tem_2
  
  while True:
    #time.sleep(1)
    display.text(ts,1,1)
    display.text(ts2,1,8)
    display.draw_chinese_fast('密山',5,0)
    display.draw_chinese_fast('温度',0,1)
    display.draw_chinese_fast('天气',0,2)
    display.draw_chinese_fast(weather_1,2,2)
    t1 = '{} C'.format(tem_1)
    t2 = '{} C'.format(tem_2)
    print(t1,t2)
    display.text(t1,40,16) 
    display.text(t2,40,24)
    
    display.show()
    
    time.sleep(0.1)
    
    global debug
    if debug:
      break
    display.fill(0)
  print('结束lcd_thread')
if __name__ =='__main__':
  connectwifi.do_connect()
  _thread.start_new_thread(lcd_thread,())
  _thread.start_new_thread(time_thread,())
  
  _thread.start_new_thread(weather_thread,())


