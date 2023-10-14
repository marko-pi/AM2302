import time
import pigpio

ampi=17                     # GPIO data pin

fall=0
data=[]
numb=[0]*5

def evnr(gpio,level,tick):  # action on rising edge
    global fall
    global data
    fall=tick

def evnf(gpio,level,tick):  # action on falling edge
    global fall
    global data
    data.append(tick-fall)

mypi=pigpio.pi()

# sending start signal
mypi.set_pull_up_down(ampi, pigpio.PUD_UP)
mypi.set_mode(ampi, pigpio.INPUT)
time.sleep(0.001)
mypi.write(ampi, 0)
mypi.set_mode(ampi, pigpio.OUTPUT)
time.sleep(0.001)
mypi.set_mode(ampi, pigpio.INPUT)

# reading reply
cbf = mypi.callback(ampi,pigpio.FALLING_EDGE,evnf)
cbr = mypi.callback(ampi,pigpio.RISING_EDGE,evnr)
time.sleep(0.1)
cbf.cancel()
cbr.cancel()

if(len(data)-2 != 40):
    print('Data error')
    quit()

for i in range(5):
    for j in range(8):
        if data[8*i+j+2]>50: numb[i]=numb[i] | (1 << (7-j))

if((numb[0]+numb[1]+numb[2]+numb[3])%256 != numb[4]):
    print('Checksum failed!')
    quit()

print('Temperature: %.1f°C, Relative humidity %.1f%%' % ((256*numb[2]+numb[3])/10,(256*numb[0]+numb[1])/10))
