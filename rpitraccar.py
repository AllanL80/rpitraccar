#! /usr/bin/python
 
from gps import *
from time import *
from re import search
import time
import threading
import requests
import os

gpsd = None #seting the global variable
traccar_main = None
updatecounter = 0 
updatetimer = 8
batt = 69 #Yeah Baby! we need to impliment this!

#details for Traccar
id = <your ID here> #your ID or IMIE - needs to command line input for multi-instance use
server = 'http://demo.traccar.org:5055' #Traccar server to send your data too - needs to command line input for multi-instance use
#http://demo.traccar.org:5055/?id=123456&lat={0}&lon={1}&timestamp={2}&hdop={3}&altitude={4}&speed={5}

class updated():
    def __init__(self):
        self.update = True
updated2 = updated()       

class currentgpsdata():
    def __init__(self):
        self.latitude = '0'
        self.longitude = '0'
        self.gpstime = '0'
        self.altitude = '0'
        self.eps = '0'
        self.epx = '0'
        self.epy = '0'
        self.eph = '0'
        self.epv = '0'
        self.ept = '0'
        self.speed = '0'
        self.climb = '0'
        self.track = '0'
        self.mode = '0'
        self.avrerr = '0'
        self.hdop = '0'
currentgpsdata1 = currentgpsdata()
    
class newgpsdata():
    def __init__(self):
        self.latitude = '0'
        self.longitude = '0'
        self.gpstime = '0'
        self.altitude = '0'
        self.eps = '0'
        self.epx = '0'
        self.epy = '0'
        self.eph = '0'
        self.epv = '0'
        self.ept = '0'
        self.speed = '0'
        self.climb = '0'
        self.track = '0'
        self.mode = '0'
        self.avrerr = '0'
        self.hdop = '0'
newgpsdata1 = newgpsdata()

#print('Envroment setup')
def processgps():
      newgpsdata1.latitude  = str(gpsd.fix.latitude)
      newgpsdata1.longitude = str(gpsd.fix.longitude)
      newgpsdata1.gpstime = str(gpsd.utc)
      newgpsdata1.altitude = str(gpsd.fix.altitude)
      newgpsdata1.eps = str(gpsd.fix.eps)
      newgpsdata1.epx = str(gpsd.fix.epx)
      newgpsdata1.epy = str(gpsd.fix.epy)
      newgpsdata1.eph = str(gpsd.fix.eph)
      newgpsdata1.epv = str(gpsd.fix.epv)
      newgpsdata1.ept = str(gpsd.fix.ept)
      newgpsdata1.speed = str(gpsd.fix.speed)
      newgpsdata1.climb = str(gpsd.fix.climb)
      newgpsdata1.track = str(gpsd.fix.track)
      newgpsdata1.mode = str(gpsd.fix.mode)
      newgpsdata1.hdop = str(gpsd.hdop)
      #newgpsdata1.avrerr = 
      #print('Processed incoming gps data')
      #
#
def newtoolddata():
      currentgpsdata1.latitude  = str(newgpsdata1.latitude)
      currentgpsdata1.longitude = str(newgpsdata1.longitude)
      currentgpsdata1.gpstime = str(newgpsdata1.gpstime)
      currentgpsdata1.altitude = str(newgpsdata1.altitude)
      currentgpsdata1.eps = str(newgpsdata1.eps)
      currentgpsdata1.epx = str(newgpsdata1.epx)
      currentgpsdata1.epy = str(newgpsdata1.epy)
      currentgpsdata1.eph = str(newgpsdata1.eph)
      currentgpsdata1.epv = str(newgpsdata1.epv)
      currentgpsdata1.ept = str(newgpsdata1.ept)
      currentgpsdata1.speed = str(newgpsdata1.speed)
      currentgpsdata1.climb = str(newgpsdata1.climb)
      currentgpsdata1.track = str(newgpsdata1.track)
      currentgpsdata1.mode = str(newgpsdata1.mode)
      currentgpsdata1.avrerr = str(newgpsdata1.avrerr)
      currentgpsdata1.hdop = str(newgpsdata1.hdop)
      #print('copyed new gps data over old')
#
def newtoolddata2():
      if  ((newgpsdata1.latitude) !='nan') and ((int(float(newgpsdata1.latitude))) <= -90) and ((int(float(newgpsdata1.latitude))) >= 90): #-90 to 90
          pass
          #print('bad lat')
      else:
          currentgpsdata1.latitude  = str(newgpsdata1.latitude)
          
      if (str(newgpsdata1.longitude) !='nan') and ((int(float(newgpsdata1.longitude))) <=-180) and ((int(float(newgpsdata1.longitude))) >=180): #-180 to 180
          pass
          #print('bad lon')
      else:
          currentgpsdata1.longitude = str(newgpsdata1.longitude)
          
      if ("Z" in (newgpsdata1.gpstime)) and ((newgpsdata1.gpstime) !='nan'):
          currentgpsdata1.gpstime = str(newgpsdata1.gpstime)
      else:
          pass
        #print('no Zulu in Zulu!')
          
      if ((str(newgpsdata1.altitude)) !='nan') and ((int(float(newgpsdata1.altitude))) >=-100) and ((int(float(newgpsdata1.altitude))) <= 100000):  # She's no starship
          currentgpsdata1.altitude = str(newgpsdata1.altitude)
      else:
          pass
          #print('needs more Raptors!',(newgpsdata1.altitude))
      
      # only update if valid-ish
      if ((newgpsdata1.eps) !='nan'):
          currentgpsdata1.eps = str(newgpsdata1.eps)
          
      if ((newgpsdata1.epx) !='nan'):    
          currentgpsdata1.epx = str(newgpsdata1.epx)
                    
      if ((newgpsdata1.epy) !='nan'):
          currentgpsdata1.epx = str(newgpsdata1.epy)
                          
      if ((newgpsdata1.eph) !='nan'):
          currentgpsdata1.eph = str(newgpsdata1.eph)
                    
      if ((newgpsdata1.epv) !='nan'):
          currentgpsdata1.epv = str(newgpsdata1.epv)
            
      if ((newgpsdata1.ept) !='nan'):
          currentgpsdata1.ept = str(newgpsdata1.ept)
      #
      err = [ int((float(currentgpsdata1.eps))), int((float(currentgpsdata1.epx))), int((float(currentgpsdata1.epy))), int((float(currentgpsdata1.eph))), int((float(currentgpsdata1.epv))), int((float(currentgpsdata1.ept))) ]
      currentgpsdata1.avrerr = sum(err) / len(err)
          
      # Sandra Bullock in...
      if (str(newgpsdata1.speed) != 'nan'):
            currentgpsdata1.speed = str(newgpsdata1.speed)
      else:
            pass
        #print('no speed update')
      if (str(currentgpsdata1.speed) == 'nan'):
         currentgpsdata1.speed = '0'
         
      if ((newgpsdata1.climb) !='nan'):
          currentgpsdata1.climb = str(newgpsdata1.climb)
          
      if ((newgpsdata1.track) !='nan'):
          currentgpsdata1.track = str(newgpsdata1.track)
          
      if ((newgpsdata1.mode) !='nan'):
          currentgpsdata1.mode = str(newgpsdata1.mode)
          
      if ((newgpsdata1.hdop) !='nan'):
          currentgpsdata1.hdop = str(newgpsdata1.hdop)
      pass
    #print('copyed valid gps data over old')
#

def checkupdate():
      if newgpsdata1.mode == currentgpsdata1.mode:
          updated2.update = False
      elif newgpsdata1.longitude == currentgpsdata1.longitude:
          updated2.update = False
      elif newgpsdata1.gpstime == currentgpsdata1.gpstime: # unless time stopped... no GPS signal?
       #   print('time does not stay still')
          updated2.update = False
      elif newgpsdata1.altitude == currentgpsdata1.altitude:
          updated2.update = False
      elif newgpsdata1.eps == currentgpsdata1.eps:
          updated2.update = False
      elif newgpsdata1.epx == currentgpsdata1.epx:
          updated2.update = False
      elif newgpsdata1.epy == currentgpsdata1.epy:
          updated2.update = False
      elif newgpsdata1.eph == currentgpsdata1.eph:
          updated2.update = False
      elif newgpsdata1.epv == currentgpsdata1.epv:
          updated2.update = False
      elif newgpsdata1.ept == currentgpsdata1.ept:
          updated2.update = False
      elif newgpsdata1.speed == currentgpsdata1.speed:
          updated2.update = False
      elif newgpsdata1.climb == currentgpsdata1.climb:
          updated2.update = False
      elif newgpsdata1.track == currentgpsdata1.track:
          updated2.update = False
      elif newgpsdata1.hdop == currentgpsdata1.hdop:
          updated2.update = False
      elif newgpsdata1.latitude == currentgpsdata1.latitude:
          updated2.update = False
          #print('No new GPS data!')
          return False
      else:          
          pass
        #print('Yes, new GPS data!')
          updated2.update = True
          return True
#
def checkupdate1():
    if newgpsdata == currentgpsdata:
          pass
        #print('No new GPS data!')
          return False
    else:
          pass
        #print('Yes, new GPS data!')
          return True
        
def updaterate(speed = 0):
    uberfast = str(120)
    fastud = str(60)
    slowud = str(40)
    global updatetimer
    if ((currentgpsdata1.speed) == 'nan'): 
            #print('speed is n/a see: {}'.format(speed))
            updatetimer = 1 # Sleep 1 Second
    elif currentgpsdata1.speed 0.0:    
                updatetimer = 300 #only sleep for 5 minutes if not moving 
    elif currentgpsdata1.speed < fastud:
                updatetimer = 30 # Sleep 30 Seconds
    elif currentgpsdata1.speed > fastud:
                updatetimer = 15 # Sleep 15 Seconds 
    elif currentgpsdata1.speed > uberfast:
                updatetimer = 5 # Sleep 5 Seconds
    elif currentgpsdata1.speed < slowud:
        #print('less than slowud')
        if ((float(currentgpsdata1.avrerr))) < 15:
        #print('accu less than 60')
            updatetimer = 900 # Sleep 15 mins if we have a good lock and not moving
    else:
                updatetimer = 666 #what the devil is wrong
    #print('update timer',(updatetimer))
    return updatetimer
#
def traccar():#send Traccar Data
        running = True
        #Traccar server update rate.... this needs work... probably needs to loop on its own to catch movement from sleep, also needs fast update alert mode and low battery conservation
        #ground speed levels
        uberfast = str(120)
        fastud = str(60)
        slowud = str(40)
        #control the rate that we update the Traccar Server
        if ((currentgpsdata1.longitude) == 0): 
                #print('has not updated gps data)
                updatetimer = 1 # Sleep 1 Second wait for GPS data
        elif (int(float(currentgpsdata1.avrerr))) > 0 and (int(float(currentgpsdata1.avrerr))) < 10 and (int(float(currentgpsdata1.hdop))) < 0.9 and (int(float(currentgpsdata1.speed))) < 1:
                print('TRACKER LOG:',(currentgpsdata1.gpstime),'Low Error, high accuracy and Not moving, having a nap for 15 mins!')
                updatetimer = 900 # Sleep 15 mins if we have a good lock and not moving
        elif (int(float(currentgpsdata1.speed))) > 2 and and currentgpsdata1.speed < 10: 
                print('TRACKER LOG:',(currentgpsdata1.gpstime),'Did you move?',currentgpsdata1.speed)
                updatetimer = 60 #only sleep for 1 minute if doing over 2kph and less than 10 probably just GPS drift
        elif currentgpsdata1.speed < slowud:
                updatetimer = 30 # Sleep 30 seconds
        elif currentgpsdata1.speed < fastud and currentgpsdata1.speed > slowud :
                updatetimer = 15 # Sleep 15 Seconds
        elif currentgpsdata1.speed > fastud:
                updatetimer = 10 # Sleep 10 Seconds 
        elif currentgpsdata1.speed > uberfast:
                updatetimer = 5 # Sleep 5 Seconds
        else:
            updatetimer = 666 #what the devil is wrong
            print('TRACKER LOG:',(newgpsdata1.gpstime),'Something was wrong with update timer if statements')
#end of update timer section
#Server data upload section
            # this needs error checking, multi server, network checking, sms if no data, maybe turn on 433mhz radio beacon
        if ((currentgpsdata1.latitude) != 'nan'):
            if ((currentgpsdata1.latitude) != 0.0) and ("Z" in (currentgpsdata1.gpstime)): #if GPS time and latitude are available we can send data!
                requests.post((server), data = {
                    'id': (id),
                    'lat': (currentgpsdata1.latitude),
                    'lon': (currentgpsdata1.longitude),
                    'timestamp': (currentgpsdata1.gpstime),
                    'hdop': (currentgpsdata1.hdop),
                    'altitude': (currentgpsdata1.altitude),
                    'speed': (currentgpsdata1.speed),
                    'batt': (batt),
                    #'wifi': (wifi),
                    'accuracy': (currentgpsdata1.avrerr),
                    'heading': (currentgpsdata1.track),
                })
                #print('***  Complete data update sent ***')
                wifiap = os.popen("sudo iwgetid -r").read()
                wifimac = open('/sys/class/net/wlan0/address').readline()
                wifiap = wifiap.rstrip("\n")
                wifimac = wifimac.rstrip("\n")
                wifimac = wifimac.replace('-', ':')
                wifi = '{}'.format(wifimac)+' {}'.format(wifiap)
                print('TRACKER LOG:',(newgpsdata1.gpstime),(id),',',(currentgpsdata1.latitude),',',(currentgpsdata1.longitude),',',(currentgpsdata1.speed),',',(currentgpsdata1.avrerr),',',(batt),',',(wifi),'waiting',(updatetimer),'seconds')
            else:
                pass
                #print((currentgpsdata1.latitude))
                
        pass#print('TRACKER LOG:',str(currentgpsdata1.gpstime),'waiting',str(updatetimer),'seconds')
        time.sleep(updatetimer)
        
                    #pass
                    #time.sleep(updatetimer)
        
        #print('*** Waiting for valid data to send ***')
            
        return running
        #time.sleep(1)
        

class TraccarUpdater(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global traccar_main
    traccar_main = traccar
    self.current_value = None
    self.running = True #thread running to true
    
  def run(self):
    global traccar_main
    while traccar:
      traccar() #continue to loop and grab gpsd info
#
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting stream 
    self.current_value = None
    self.running = True #thread running to true
    
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #continue to loop and grab gpsd info
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  traccarp = TraccarUpdater()
  
  try:
    gpsp.start() # start it up
    traccarp.start()
    
    while True:
       
      #print data needs to be a def for debuging...
      #print()
      #print('GPS input')
      #print('-----------------')
      #print('latitude    ' , gpsd.fix.latitude,'longitude   ' , gpsd.fix.longitude)
      #print('time utc    ' , gpsd.utc)
      #print('altitude (m)' , gpsd.fix.altitude)
      #print('est speed err' , gpsd.fix.eps,'est lon err' , gpsd.fix.epx,'est lat err' , gpsd.fix.epy)
      #print('est virt err ' , gpsd.fix.epv,'est timeerr' , gpsd.fix.ept,'est pos err' , gpsd.fix.eph)
      #print()
      #print('speed (m/s) ' , gpsd.fix.speed)
      #print('climb       ' , gpsd.fix.climb,'track       ' , gpsd.fix.track)
      #print()
      #print('mode        ' , gpsd.fix.mode)
      #print('hdop        ' , gpsd.hdop)
      #print( 'sats        ' , gpsd.satellites)
      #print()
      #print('GPS Stored values used for Traccar')
      #print('-----------------')
      #print('latitude    ' , currentgpsdata1.latitude,'longitude   ' , currentgpsdata1.longitude)
      #print('time utc    ' , currentgpsdata1.gpstime)
      #print('altitude (m)' , currentgpsdata1.altitude)
      #print('est speed err' , currentgpsdata1.eps,'est lon err' , currentgpsdata1.epx,'est lat err' , currentgpsdata1.epy)
      #print('est virt err ' , currentgpsdata1.epv,'est timeerr' , currentgpsdata1.ept,'est pos err' , currentgpsdata1.eph)
      #print('adv error is',currentgpsdata1.avrerr)
      #print()
      #print('speed (m/s) ' , currentgpsdata1.speed, 'climb       ' , currentgpsdata1.climb,'track       ' , currentgpsdata1.track)
      #print()
      #print('mode        ' , currentgpsdata1.mode, 'Updated',updatecounter)
      #print('hdop        ' , currentgpsdata1.hdop)
      #turn data into string variables
      processgps()
            
      checkupdate1()
      if updated2.update == True:
            updatecounter = updatecounter+1
     
      newtoolddata2()
      
      time.sleep(5) #set to whatever
         
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print( "\nKilling Thread...")
    gpsp.running = False
    traccarp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    traccarp.join()
  print( "Done.\nExiting.")

