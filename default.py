#!/usr/bin/python
# -*- coding: utf-8 -*-
###########################################################################
#
#          FILE:  plugin.program.newscenter/default.py
#
#        AUTHOR:  Tobias D. Oestreicher
#
#       LICENSE:  GPLv3 <http://www.gnu.org/licenses/gpl.txt>
#       VERSION:  0.0.6
#       CREATED:  13.02.2016
#
###########################################################################
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.
#
###########################################################################
#     CHANGELOG:  (13.02.2016) TDOe - First Publishing
###########################################################################


import os
import sys
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import json
import urllib2

from resources.lib.FhemSet import FHEMSet
from resources.lib.FhemDialogs import FHEMDialogs
from resources.lib.PH import PluginHelpers


# Dialogwindows

##########################################################################################################################
##
##########################################################################################################################
def getUnicodePage(url):
    req = urllib2.urlopen(url)
    content = ""
    if "content-type" in req.headers and "charset=" in req.headers['content-type']:
        encoding=req.headers['content-type'].split('charset=')[-1]
        content = unicode(req.read(), encoding)
    else:
        content = unicode(req.read(), "utf-8")
    return content




##########################################################################################################################
##########################################################################################################################
##
##                                                       M  A  I  N
##
##########################################################################################################################
##########################################################################################################################

__addon__               = xbmcaddon.Addon()
__addonID__             = __addon__.getAddonInfo('id')
__addonDir__            = __addon__.getAddonInfo("path")
__addonFolder__         = xbmc.translatePath('special://home/addons/'+__addonID__).decode('utf-8')
__addonUserDataFolder__ = xbmc.translatePath("special://profile/addon_data/"+__addonID__).decode('utf-8')
__addonname__           = __addon__.getAddonInfo('name')
__version__             = __addon__.getAddonInfo('version')
__LS__                  = __addon__.getLocalizedString
__icon__                = os.path.join(__addonFolder__, "icon.png")#.encode('utf-8')

WINDOW                  = xbmcgui.Window( 10000 )

ip                      = __addon__.getSetting('ip')
port                    = __addon__.getSetting('port')


FeedFile = '%s/fhemset.json' % (__addonUserDataFolder__) # xbmc.translatePath('special://home/addons/'+__addonID__+'/NewsFeeds.json').decode('utf-8')

try:
    with open(FeedFile, 'r') as feeds:
        ConfigFeeds=feeds.read().rstrip('\n')
except:
    TemplateFeedFile = xbmc.translatePath('special://home/addons/'+__addonID__+'/fhemset.json').decode('utf-8')
    TemplateFeedFileHandle = open(TemplateFeedFile)
    TemplateFeedFileContent = TemplateFeedFileHandle.read()
    TemplateFeedFileHandle.close()
    UserFeedFileHandle = open(FeedFile, 'w')
    UserFeedFileHandle.write(TemplateFeedFileContent)
    UserFeedFileHandle.close()
    with open(FeedFile, 'r') as feeds:
        ConfigFeeds=feeds.read().rstrip('\n')




# Create Objects
ph          = PluginHelpers()

fhemset     = FHEMSet()
fhemdialogs = FHEMDialogs()


ph.writeLog('SYSARGV:         %s' % (sys.argv), level=xbmc.LOGDEBUG)
if len(sys.argv)>=3:
    addon_handle = int(sys.argv[1])
    params = ph.parameters_string_to_dict(sys.argv[2])
    methode = urllib.unquote_plus(params.get('methode', ''))
    cmd = urllib.unquote_plus(params.get('cmd', ''))
    file = urllib.unquote_plus(params.get('file', ''))
    title=urllib.unquote_plus(params.get('title', ''))
elif len(sys.argv)>=1:
    params = ph.parameters_string_to_dict(sys.argv[1])
    ph.writeLog('PARAMS:         %s' % (params), level=xbmc.LOGDEBUG)
    methode = urllib.unquote_plus(params.get('methode', ''))
    cmd = urllib.unquote_plus(params.get('cmd', ''))
    file = urllib.unquote_plus(params.get('file', ''))
    title=urllib.unquote_plus(params.get('title', ''))
else:
    methode = None

if file != '':
    WINDOW.setProperty( "FHEMControl.Window", file )
    WINDOW.setProperty( "FHEMControl.Title", title )
    ph.writeLog('SETFILE:         %s' % (file), level=xbmc.LOGDEBUG)

ph.writeLog('FILE:         %s' % (file), level=xbmc.LOGDEBUG)
ph.writeLog('IP  :         %s' % (ip), level=xbmc.LOGDEBUG)
ph.writeLog('PORT:         %s' % (port), level=xbmc.LOGDEBUG)
ph.writeLog('CMD :         %s' % (cmd), level=xbmc.LOGDEBUG)

##########################################################################################################################
## Check methode to process
##########################################################################################################################

## Service
if methode=='set':
        fhemset.SendCommand(ip,port,cmd)
elif methode=='stop_service':
        WINDOW.setProperty( "LatestNews.Service", "inactive" )

# Selects
elif methode=='get_sets_items':

    file=WINDOW.getProperty("FHEMControl.Window")
    title=WINDOW.getProperty("FHEMControl.Title")
    ph.writeLog("IN get_sets_items2:         %s" % (title), level=xbmc.LOGDEBUG)
    feedjson = fhemdialogs.feed2container2(file,title)

    for sitem in feedjson:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=sitem['PIC'])
        li.setProperty("URL", sitem['URL'])
        li.setProperty("CMD", sitem['CMD'])
        ph.writeLog('CMD - SITEM :         %s' % (sitem['CMD']), level=xbmc.LOGDEBUG)
        url="plugin.program.fhemcontrol/?methode=set&cmd=%s" % (sitem['CMD'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

elif methode=='show_sets_window':
    DETAILWIN = xbmcgui.WindowXMLDialog('sets-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()




