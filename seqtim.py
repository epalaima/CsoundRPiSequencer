# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
import ctcsound
import math
import RPi.GPIO as GPIO
from threading import Timer,Thread,Event


cs = ctcsound.Csound()

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 22
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
CS2  = 4
mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS2, miso=MISO, mosi=MOSI)


GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

ret = cs.compile_("csound", "seqtim.csd")
if ret == ctcsound.CSOUND_SUCCESS:
    pt = ctcsound.CsoundPerformanceThread(cs.csound())
    pt.play()

pots = [1.0] * 15
switch = [1] * 6

class TimerInterrupt():

   def __init__(self, time, rate, cspt):
    	self.time=time
    	self.gpio = 17
    	self.rate=rate
    	self.counter = 0
    	self.stage = 0
    	self.cspt = cspt
    	self.thread = Timer(self.time,self.handle_function)
    	GPIO.setup(17, GPIO.OUT)
    	GPIO.setup(27, GPIO.OUT)
    	GPIO.setup(12, GPIO.OUT)
    	GPIO.setup(13, GPIO.OUT)

   def start(self):
    	self.thread.start()

   def cancel(self):
   		self.thread.cancel()

   def setRate(self, rate):
   		self.rate = rate

   def handle_function(self):
   		self.counter += 1
   		if self.counter > self.rate: 
   			self.counter = 0
   			if self.stage == 0:
   				GPIO.output(17, GPIO.HIGH)
	   			GPIO.output(27, GPIO.LOW)
	   			GPIO.output(12, GPIO.LOW)
	   			GPIO.output(13, GPIO.LOW)
	   		elif self.stage == 1:
	   			GPIO.output(17, GPIO.LOW)
	   			GPIO.output(27, GPIO.HIGH)
	   			GPIO.output(12, GPIO.LOW)
	   			GPIO.output(13, GPIO.LOW)
	   		elif self.stage == 2:
	   			GPIO.output(17, GPIO.LOW)
	   			GPIO.output(27, GPIO.LOW)
	   			GPIO.output(12, GPIO.HIGH)
	   			GPIO.output(13, GPIO.LOW)
	   		elif self.stage == 3:
	   			GPIO.output(17, GPIO.LOW)
	   			GPIO.output(27, GPIO.LOW)
	   			GPIO.output(12, GPIO.LOW)
	   			GPIO.output(13, GPIO.HIGH)
	   		self.cspt.scoreEvent(False, "i", (100, 0, 1, self.stage))
	   		self.stage += 1
   			if self.stage > 3:
   				self.stage = 0

   		self.thread = Timer(self.time ,self.handle_function)
   		self.thread.start()


t = TimerInterrupt(.005, 100, pt)
t.start()

def quantize(input):
	incr = 0
	scale = [32.7, 36.71, 41.2, 49.0, 55.0, 65.41, 73.42, 82.41, 98.0, 110.0, 130.81, 146.83, 164.81, 196.0, 220.0, 261.63, 293.66, 329.63, 392.0, 440.0, 532.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.66, 1318.51, 1567.98, 1760.0, 2093.0]
	while input > scale[incr]:
		incr += 1
	return scale[incr]

while True:

	switch[0] = GPIO.input(5) # lfo route (filt, freq)
	switch[1] = GPIO.input(15) # lfo rate (lfo vs audio)
	switch[2] = GPIO.input(14) # oscil waveform (square vs saw)
	switch[3] = GPIO.input(6) # quantize freq
	switch[4] = GPIO.input(2) # lfo waveform
	switch[5] = GPIO.input(3) # lfo follow oscil rate
	for index in range(0, 4):
		pots[index] = (1 - math.sqrt(mcp.read_adc(index) / 1023.0)) * 2000 + 40
		if switch[3] == 1:
			pots[index] = quantize(pots[index])
	for index in range(4, 8):
		pots[index] = (1 - math.sqrt(mcp.read_adc(index) / 1023.0)) * 10000
	pots[8] = 5 + 100 * (mcp2.read_adc(0) / 1023.0)**2 #rate
	t.setRate(pots[8])
	pots[9] = mcp2.read_adc(1) / 3072.0 #port
	if switch[5] == 0:
		pots[10] = 0.1 + 102.3 * (1 - math.sqrt(mcp2.read_adc(2) / 1023.0))#lfo rate
	else: #if lfo is following oscillator rate
		if switch[1] == 1:
			pots[10] = 0.05 + 0.15 * (1 - math.sqrt(mcp2.read_adc(2) / 1023.0))#lfo rate
		else:
			pots[10] = 0.01 + .09 * (1 - math.sqrt(mcp2.read_adc(2) / 1023.0))#lfo rate
	pots[11] = 1 - (mcp2.read_adc(3) / 1023.0)  #lfo depth
	pots[12] = 0.85 * (1 - (mcp2.read_adc(4) / 1023.0)) # resonance
	pots[13] = .1 * (1 - (mcp2.read_adc(5) / 1023.0)) # detune
	pots[14] = 0

	pt.scoreEvent(False, 'i', (10, 0, 1, pots[0], pots[1], pots[2], pots[3], pots[4], pots[5], pots[6], pots[7], pots[8], pots[9], pots[10], pots[11], pots[12], pots[13], pots[14], switch[0], switch[1], switch[2], switch[3], switch[4], switch[5]))
	time.sleep(0.1)

pt.stop()
pt.join()
