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
def show_bulispielplan(liga):
    DETAILWIN = xbmcgui.WindowXMLDialog('bulilist-spielplan-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()

##########################################################################################################################
##
##########################################################################################################################
def show_bulinaechsterspieltag(liga):
    DETAILWIN = xbmcgui.WindowXMLDialog('bulilist-naechsterspieltag-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()

##########################################################################################################################
##
##########################################################################################################################
def show_bulilist(liga):
    DETAILWIN = xbmcgui.WindowXMLDialog('bulilist-platzierung-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()

##########################################################################################################################
##
##########################################################################################################################
def show_unwetterwarnungen():
    DETAILWIN = xbmcgui.WindowXMLDialog('unwetterwarnungen-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()





# To Remove: docu.cc Widget

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
    #xbmc.executebuiltin('Skin.SetString("fhemjsonfile","%s" % (file))')
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

    ph.writeLog("IN get_sets_items:         %s" % (xbmc.getInfoLabel('Skin.String(fhemjsonfile)')), level=xbmc.LOGDEBUG)
    ph.writeLog("IN get_sets_items:         %s" % (title), level=xbmc.LOGDEBUG)
    file=WINDOW.getProperty("FHEMControl.Window")
    title=WINDOW.getProperty("FHEMControl.Title")
    ph.writeLog("IN get_sets_items2:         %s" % (title), level=xbmc.LOGDEBUG)
    #xbmc.executebuiltin("Skin.SetString(fhemjsonfile,file,4711815)")
#    if file != '':
    feedjson = fhemdialogs.feed2container2(file,title)
#      xbmc.executebuiltin("Skin.SetString(fhemjsonfile,file)")
#    else:
#      feedjson = fhemdialogs.feed2container2("fhemsetheizung.json")
#      xbmc.executebuiltin('Skin.SetString(fhemjsonfile,"fhemsetheizung.json")')

    for sitem in feedjson:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=sitem['PIC'])
        li.setProperty("URL", sitem['URL'])
        li.setProperty("CMD", sitem['CMD'])
        ph.writeLog('CMD - SITEM :         %s' % (sitem['CMD']), level=xbmc.LOGDEBUG)
        url="plugin.program.fhemcontrol/?methode=set&cmd=%s" % (sitem['CMD'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

elif methode=='show_sets_window':
    #xbmc.executebuiltin("Skin.SetString(fhemjsonfile,file,4711815)")
    DETAILWIN = xbmcgui.WindowXMLDialog('sets-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()


elif methode=='show_livestream_select_dialog':
    dialog = xbmcgui.Dialog()
    ret = dialog.select(__LS__(30190), [__LS__(30191), __LS__(30192), __LS__(30193), __LS__(30194), __LS__(30195), __LS__(30196)])
    if ret == 0:
        nls.PlayTagesschau24()
    elif ret == 1:
        nls.PlayEuronews()
    elif ret == 2:
        nls.PlayNTV()
    elif ret == 3:
        nls.PlayN24()
    elif ret == 4:
        nls.PlayPhoenix()
    elif ret == 5:
        nls.PlayDW()

elif methode=='show_buli_select':
    dialog = xbmcgui.Dialog()
    ret = dialog.select(str(__LS__(30153)), [str(__LS__(30128)), str(__LS__(30129)), str(__LS__(30125)), str(__LS__(30126)), __LS__(30091), __LS__(30092)])
    if ret == 0:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "1" )
        show_bulilist(1)        
    elif ret == 1:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "2" )
        show_bulilist(2)
    elif ret == 2:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "1" )
        show_bulispielplan("1")
    elif ret == 3:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "2" )
        show_bulispielplan(2)
    elif ret == 4:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "1" )
        show_bulinaechsterspieltag(1)
    elif ret == 5:
        WINDOW.setProperty("NewsCenter.Buli.LigaInfo", "2" )
        show_bulinaechsterspieltag(2)




# Settings
elif methode=='set_default_feed':
    allfeeds = json.loads(str(ConfigFeeds))
    feedname=[]
    for f in allfeeds:
        feedname.append(f['name'])

    dialog = xbmcgui.Dialog()
    ret = dialog.select(str(__LS__(30155)),feedname)
    defaultfeedname=allfeeds[ret]['name']
    __addon__.setSetting('storedefault',defaultfeedname)




# Dialogwindows
elif methode=='show_bulilist':
    WINDOW.setProperty("NewsCenter.Buli.LigaInfo", buliliga )
    show_bulilist(buliliga)

elif methode=='show_bulispielplan':
    WINDOW.setProperty("NewsCenter.Buli.LigaInfo", buliliga )
    show_bulispielplan(buliliga)

elif methode=='show_bulinaechsterspieltag':
    WINDOW.setProperty("NewsCenter.Buli.LigaInfo", buliliga )
    show_bulinaechsterspieltag(buliliga)

elif methode=='show_wetter_karte_bundesland':
    DETAILWIN = xbmcgui.WindowXMLDialog('wetterkarten-bundesland-DialogWindow.xml', __addonDir__, 'Default', '720p')
    DETAILWIN.doModal()




# Container
elif methode=='get_buli_spielplan_items':
    spielelist = nb.get_buli_spielplan_items(buliliga)
    url = '-'
    for sitem in spielelist:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=sitem['Logo'])
        li.setProperty("Spieldatum", str(sitem['Spieldatum']))
        li.setProperty("Mannschaft1", sitem['Mannschaft1'])
        li.setProperty("Mannschaft2", sitem['Mannschaft2'])
        li.setProperty("Mannschaft1Logo", sitem['Mannschaft1Logo'])
        li.setProperty("Mannschaft2Logo", sitem['Mannschaft2Logo'])
        li.setProperty("Ergebniss", str(sitem['Ergebniss']))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


elif methode=='get_buli_table_items':
    bulilist = nb.get_buli_table_items(buliliga)
    url = '-'
    for sitem in bulilist:
        Logo = sitem['Logo']
        Logo = Logo.encode('utf-8')
        li = xbmcgui.ListItem(sitem['Label'], iconImage=Logo)
        li.setProperty("Spiele", str(sitem['Spiele']))
        li.setProperty("SUN", sitem['SUN'])
        li.setProperty("Platz", str(sitem['Platz']))
        li.setProperty("Tore", str(sitem['Tore']))
        li.setProperty("Punkte", str(sitem['Punkte']))
        li.setProperty("StatPic", str(sitem['StatPic']))
        li.setProperty("Logo", str(sitem['Logo']))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


elif methode=='get_buli_naechsterspieltag_items':
    bulilist = nb.get_buli_naechsterspieltag_items(buliliga)
    url = '-'
    for sitem in bulilist:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=__icon__)
        li.setProperty("Mannschaft1", sitem['Mannschaft1'])
        li.setProperty("Mannschaft2", sitem['Mannschaft2'])
        li.setProperty("Mannschaft1Logo", str(sitem['Logo1']))
        li.setProperty("Mannschaft2Logo", str(sitem['Logo2']))
        li.setProperty("Spieldatum", str(sitem['Label']))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)



elif methode=='get_feed_items':
    feedjson = nf.feed2container2()
    for sitem in feedjson:
        li = xbmcgui.ListItem(sitem['Label'], iconImage=sitem['Logo'])
        li.setProperty("Desc", sitem['Desc'])
        li.setProperty("HeaderPic", sitem['HeaderPic'])
        li.setProperty("Date", sitem['Date'])
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)




# Wetterkarten
elif methode=='get_dwd_pics_base':
        nwk.DWD_Base(clickable)

elif methode=='get_dwd_pics_base_uwz':
        nwk.DWD_Base_UWZ(clickable)

elif methode=='get_dwd_pics_extended':
        nwk.DWD_Extended(clickable)

elif methode=='get_dwd_pics_bundesland':
        nwk.DWD_Bundesland(clickable)

elif methode=='get_dwd_pics_bundesland_uwz':
        nwk.DWD_Bundesland_UWZ(clickable)

elif methode=='get_dwd_pics_base_extended':
        nwk.DWD_Base_Extended(clickable)

elif methode=='get_euronews_wetter_pics':
        nwk.Euronews(clickable)




# Pollen
elif methode=='get_pollen_items':
        npf = NewsPollenflug()
        npf.get_pollen_items()




# Unwetter
elif methode=='get_unwetter_warnungen':
        if __addon__.getSetting('plz') != '':
            nuwz.Warnungen("DE", __addon__.getSetting('plz'))
        else:
            notifyheader= str(__LS__(30010))
            xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30149))+' ,4000,'+__icon__+')')

elif methode=='get_uwz_count':
        if __addon__.getSetting('plz') != '':
            nuwz.WarnAnzahl("DE", __addon__.getSetting('plz'))
        else:
            notifyheader=str(__LS__(30010))
            xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30149))+' ,4000,'+__icon__+')')

elif methode=='get_uwz_maps':
        nwk.UWZ(clickable)

elif methode=='show_unwetter_warnungen':
	show_unwetterwarnungen()




# Default Entry
elif methode=='refresh':
        WINDOW.setProperty( "LatestNews.Service", "active" )
        notifyheader= str(__LS__(30010))
        notifytxt   = str(__LS__(30108))
        xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifytxt+' ,4000,'+__icon__+')')
        allfeeds = json.loads(str(ConfigFeeds))
        storedefault=__addon__.getSetting('storedefault')
        if storedefault != '':
            for f in allfeeds:
                if f['name'] == storedefault:
                    url=f['url']
                    pic=f['pic']
                    break
        else:
            url="http://www.kodinerds.net/index.php/BoardFeed/?at=30575-8e710f12c83d6c7f66184ca3354f2c83baf4bbed"
            pic="http://www.kodinerds.net/images/wbbLogo.png"
        nf.feed2property(url, pic)

        if __addon__.getSetting('plz') != '':
            nuwz.WarnAnzahl("DE", __addon__.getSetting('plz'))
            WINDOW.setProperty( "NewsCenter.PLZ", __addon__.getSetting('plz') )
            WINDOW.setProperty( "NewsCenter.Bundesland", __addon__.getSetting('storebundesland') )
            WINDOW.setProperty( "NewsCenter.Ort", __addon__.getSetting('storeort') )
        else:
            xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30149))+' ,4000,'+__icon__+')')
        # To Remove: LatestDokus Widget
        #set_LatestDokus_to_Home('http://doku5.com/api.php?search=UFO&page=1&noDYV=on')




elif methode==None:

    allfeeds = json.loads(str(ConfigFeeds))
    feedname=[]
    for f in allfeeds:
        feedname.append(f['name'])
    dialog = xbmcgui.Dialog()
    ret = dialog.select("News Auswahl",feedname)
    headerpic=allfeeds[ret]['pic']
    url=allfeeds[ret]['url']
    notifyheader= str(__LS__(30010))
    xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+str(__LS__(30150))+' ,8000,'+__icon__+')')
    nf.feed2property(url, headerpic)

