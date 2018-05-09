'''
    FHEM-Control for XBMC
    Copyright (C) 2017 TDOe

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import xbmc
import xbmcaddon
import xbmcgui
import time
import os
import sys
import json
import re
import telnetlib

__settings__   = xbmcaddon.Addon(id='plugin.program.fhemcontrol')
__cwd__        = __settings__.getAddonInfo('path')
__icon__       = os.path.join(__cwd__,"icon.png")
__scriptname__ = "FHEM-Control"

__addon__     = xbmcaddon.Addon()
__addonID__   = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__addonUserDataFolder__ = xbmc.translatePath("special://profile/addon_data/"+__addonID__).decode('utf-8')
__version__   = __addon__.getAddonInfo('version')
__path__      = __addon__.getAddonInfo('path')
__LS__        = __addon__.getLocalizedString
__icon__      = xbmc.translatePath(os.path.join(__path__, 'icon.png'))




BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)

from settings import *
#from fhem import *

global g_failedConnectionNotified

def writeLog(message, level=xbmc.LOGNOTICE):
        xbmc.log('[%s %s]: %s' % (__addonID__, __version__,  message.encode('utf-8')), level)





def initGlobals():
  global g_failedConnectionNotified

  g_failedConnectionNotified = False   
  settings_initGlobals()

def process_fhem():
  while not xbmc.abortRequested:
    fetchFhem()
    for i in range(1,30):
      time.sleep(1)
      if xbmc.abortRequested:
        break


def fhem_get_json(ip,port,fhemdev):
  ret = ""
  try:
    tn = telnetlib.Telnet()
    writeLog("Connect to fhem %s:%s" % (str(ip),str(port)), level=xbmc.LOGDEBUG)
    tn.open(ip, port)
    tn.write("jsonlist2 %s\n" % (str(fhemdev)))
    tn.write("quit\n")
    ret = tn.read_all()
    tn.close()
    ret = re.sub(r'Bye...', '',str(ret))
  except:
    writeLog("telnet exception, could not connect to fhem instance",  level=xbmc.LOGNOTICE)
  return ret



def kodi_set_infovar(key,value):
    writeLog('Setting INFO Var', level=xbmc.LOGDEBUG)
    xbmcgui.Window(10000).setProperty('%s' % (key), value)


def fhem_process(ip,port,DeviceList,AllReadings,AllInternals):
    try:
        FHEMJsonRes=json.loads(fhem_get_json(ip,port,DeviceList))
        
        for Entity in FHEMJsonRes['Results']:
            for Reading in AllReadings:
                if Reading['FHEMDev'] == Entity['Name']:
                    SearchKey=Reading['SearchKey']
                    INFOVar=Reading['INFOVar']
                    logtext="INFOVar: %s Entity: %s[%s] -> %s" % (Reading['INFOVar'],Reading['FHEMDev'],Reading['SearchKey'],Entity['Readings'][Reading['SearchKey']]['Value'])
                    writeLog(logtext,level=xbmc.LOGDEBUG)
                    kodi_set_infovar(Reading['INFOVar'],Entity['Readings'][Reading['SearchKey']]['Value'])
                    break
        
            for Internal in AllInternals:
                if Internal['FHEMDev'] == Entity['Name']:
                    SearchKey=Internal['SearchKey']
                    INFOVar=Internal['INFOVar']
                    logtext="INFOVar: %s Entity: %s[%s] -> %s" % (Internal['INFOVar'],Internal['FHEMDev'],Internal['SearchKey'],Entity['Internals'][Internal['SearchKey']])
                    writeLog(logtext,level=xbmc.LOGDEBUG)
                    kodi_set_infovar(Internal['INFOVar'],Entity['Internals'][Internal['SearchKey']])
                    break
        
    except:
        pass




def fetchFhem():
  global g_failedConnectionNotified
  
  hostip   = settings_getHostIp()
  hostport = settings_getHostPort()
  
  while not xbmc.abortRequested:
    #check for new settings
    if settings_checkForNewSettings():    #networksettings changed?
      g_failedConnectionNotified = False  #reset notification flag
    hostip   = settings_getHostIp()
    hostport = settings_getHostPort()    
    writeLog("IP:           %s" % (hostip),level=xbmc.LOGDEBUG)
    writeLog("Port:         %s" % (hostport),level=xbmc.LOGDEBUG)
    writeLog("DeviceList:   %s" % (DeviceList),level=xbmc.LOGDEBUG)
    FHEMJsonRes=""
    try:
      FHEMJsonRes=json.loads(fhem_get_json(hostip,hostport,DeviceList))
    except:
      pass
    if not FHEMJsonRes:
      writeLog('Connection Failed', level=xbmc.LOGNOTICE)
      count = 10
      while (not xbmc.abortRequested) and (count > 0):
        time.sleep(1)
        count -= 1
      if not g_failedConnectionNotified:
        g_failedConnectionNotified = True
        text = __settings__.getLocalizedString(500)
        xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,text,10,__icon__))
    else:
      text = __settings__.getLocalizedString(501)
      if not g_failedConnectionNotified:
        xbmc.executebuiltin("XBMC.Notification(%s,%s,%s,%s)" % (__scriptname__,text,10,__icon__))
        g_failedConnectionNotified = True
      fhem_process(hostip,hostport,DeviceList,AllReadings,AllInternals)  
      writeLog('Connection Successfull', level=xbmc.LOGDEBUG)
      break
  return True

#MAIN - entry point
initGlobals()

FHEMGetFile = '%s/fhemget.json' % (__addonUserDataFolder__) 
try:
    with open(FHEMGetFile, 'r') as toread:
            ConfigReads=toread.read().rstrip('\n')
except:
    writeLog('Could not open configfile fhemget.json', level=xbmc.LOGNOTICE)

allreads = json.loads(str(ConfigReads))


AllReadings=allreads['Readings']
AllInternals=allreads['Internal']
Keys=[]
for Reading in AllReadings:
    Keys.append(Reading['FHEMDev'])

for Internal in AllInternals:
    Keys.append(Internal['FHEMDev'])

DeviceList=','.join(Keys)




#main loop
while not xbmc.abortRequested:
  settings_setup()
  process_fhem()    #fhem loop

