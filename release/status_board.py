"""
Simple module to used with the uStatusBoard.
It uses four (4) WS2812B (aka Neopixels) connected
by default to pin 15 on the ESP8266
-------------------------------
| |_| LED 0  #################|
|  _                          |
| |_| LED 1  #################|
|  _                          |
| |_| LED 2  #################|
|  _                          |
| |_| LED 3  #################|
-------------------------------
More info: https://github.com/yeyeto2788/uStatusBoard
"""
import machine
import neopixel
import urandom
class StatusBoard:
 def __init__(self,pin=15,neopixels=4,brightness=255):
  self.pin=machine.Pin(pin,machine.Pin.OUT)
  self.neopixels=neopixels
  self.neostrip=neopixel.NeoPixel(self.pin,self.neopixels)
  self.brightness=brightness
  self.colors={"nocolor":[0,0,0],"blue":[0,0,1],"green":[0,1,0],"cyan":[0,1,1],"red":[1,0,0],"magenta":[1,0,1],"yellow":[1,1,0],"white":[1,1,1],}
  self.clear_all()
 def _get_color_brightness(self,color):
  return[(c_value*self.brightness)for c_value in self.colors[color.lower()]]
 def set_pixel_color(self,pixel,color):
  self.neostrip[pixel]=self._get_color_brightness(color)
  self.neostrip.write()
 def clear_all(self):
  for pixel in range(self.neopixels):
   self.neostrip[pixel]=(0,0,0)
  self.neostrip.write()
 def color_all(self,color):
  for pixel in range(self.neopixels):
   self.neostrip[pixel]=self._get_color_brightness(color)
  self.neostrip.write()
 def _get_random_int(self):
  int_return=urandom.getrandbits(8)
  if 0<int_return<256:
   return int_return
  else:
   return 0
 def set_pixel_random_color(self,pixel):
  r_color=self._get_random_int()
  g_color=self._get_random_int()
  b_color=self._get_random_int()
  color=[r_color,g_color,b_color]
  self.neostrip[pixel]=color
  self.neostrip.write()
 def get_pixel_raw_color(self,pixel):
  return self.neostrip[pixel]
 def set_pixel_raw_color(self,pixel,color):
  self.neostrip[pixel]=color
  self.neostrip.write()
