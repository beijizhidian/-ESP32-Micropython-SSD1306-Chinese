import machine
from machine import Pin, SPI
import ssd1306
import framebuf,time
import font_new

spi = SPI(1, 10000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = ssd1306.SSD1306_SPI(128,64,spi,Pin(25),Pin(26),Pin(27))
display.poweron()
display.init_display()

byte = b'11111111111111110000000000000000111111111111111100000000000000001111111111111111000000000000000011111111111111110000000000000000'

byte = bytearray(byte)
print(byte)
buf = framebuf.FrameBuffer(byte,128,1,framebuf.MONO_VLSB)
print(buf)
display.fill(0)
display.blit(buf,0,0)
display.blit(buf,0,10)
display.fill(0)

byte_list = [0x01,0x01,0x01,0x01,0x01,0xFF,0x01,0x01,0x02,0x02,0x04,0x04,0x08,0x10,0x20,0xC0,
  0x00,0x00,0x00,0x00,0x00,0xFE,0x00,0x00,0x80,0x80,0x40,0x40,0x20,0x10,0x08,0x06,]
n=0
start = time.ticks_ms()
for i in byte_list:
  s = '{:08b}'.format(i)
  byte = bytes(s.encode('utf-8'))
  byte = bytearray(byte)
  #print(byte)
  buf = framebuf.FrameBuffer(byte,8,1,framebuf.MONO_VLSB)
  if n<17:
    display.blit(buf,0,n)
  else:
    display.blit(buf,8,n-16)
  n+=1
print(time.ticks_diff(start,time.ticks_ms()))
display.show()

display.fill(0)
k='雨'
code = 0x00#将中文转成16进制编码
data_code = k.encode("utf-8")
code |= data_code[0]<<16
code |= data_code[1]<<8
code |= data_code[2]		  
print(code)
byte_data=font_new.byte2.get(code)

start = time.ticks_ms()
byte = bytearray(byte_data)
buf = framebuf.FrameBuffer(byte,16,16,framebuf.MONO_HLSB)
display.blit(buf,0,0)
print(time.ticks_diff(start,time.ticks_ms()))
display.show()
display.fill(0)
display.draw_chinese_fast('小雨',2,0)
display.show()
