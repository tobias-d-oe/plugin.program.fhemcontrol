#!/usr/bin/python
# -*- coding: utf-8 -*-

#import re
#import HTMLParser
import xbmcgui
import json
import os
import sys

#####import urllib
#####import sys
#####import os
#####import datetime
import xbmc
#####import xbmcgui
import xbmcaddon
#####import xbmcplugin
#####from xml.dom.minidom import parseString
#####
class FHEMDialogs():
    def __init__(self):
        url=''


##########################################################################################################################
##
##########################################################################################################################
    def feed2container2(self,file,title):
        WINDOW = xbmcgui.Window( 10000 )
        listitems = []
        feedname=[]

        addon      = xbmcaddon.Addon()
        addonID    = addon.getAddonInfo('id')
        __addon__               = xbmcaddon.Addon()
        __addonID__             = __addon__.getAddonInfo('id')
        __addonDir__            = __addon__.getAddonInfo("path")
        __addonFolder__         = xbmc.translatePath('special://home/addons/'+__addonID__).decode('utf-8')
        __addonUserDataFolder__ = xbmc.translatePath("special://profile/addon_data/"+__addonID__).decode('utf-8')
        __addonname__           = __addon__.getAddonInfo('name')
        __version__             = __addon__.getAddonInfo('version')
        __LS__                  = __addon__.getLocalizedString
        __icon__                = os.path.join(__addonFolder__, "icon.png")#.encode('utf-8')

        mediaPath  = xbmc.translatePath('special://home/addons/'+addonID+'/resources/skins/Default/media/')

        FeedFile = '%s/%s' % (__addonUserDataFolder__,file) # xbmc.translatePath('special://home/addons/'+__addonID__+'/NewsFeeds.json').decode('utf-8')

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



        allfeeds = json.loads(str(ConfigFeeds))
        xbmc.log('[plugin.program.fhemcontrol] TITLE: %s' % (allfeeds['title']), xbmc.LOGDEBUG)
        WINDOW.setProperty( "FHEMControl.Title", allfeeds['title'] )
        for f in allfeeds['entries']:
            feedname.append(f['name'])
            cmd          = f['cmd']
            pic          = f['pic']
            xbmc.log('[plugin.program.fhemcontrol] NAME: %s' % (f['name']), xbmc.LOGDEBUG)
            xbmc.log('[plugin.program.fhemcontrol] CMD in for: %s' % (f['cmd']), xbmc.LOGDEBUG)
            json_str = { "Label": f['name'], "CMD": "%s" % (f['cmd']), "URL": "plugin.program.fhemcontrol/?methode=set&cmd=%s" % (f['cmd']), "PIC": f['pic']}
            listitems.append( json_str )
        return listitems

##########################################################################################################################
##
##########################################################################################################################
    def feed2property(self,url,headerpic):
        if headerpic == '':
            headerpic='http://www.kokobeet.at/wp-content/uploads/logo_platzhalter.gif'
        feed = feedparser.parse( url )
        WINDOW = xbmcgui.Window( 10000 )
        x=0
    
        for item in feed[ "items" ]:
            title = item[ "title" ]
    
            try:
                img = item[ "media_content" ][0][ "url" ]
            except:
                try:
                    ce = item[ "content" ][0][ "value" ]
                    imgsrc = re.search('img[^<>\\n]+src=[\'"]([^"\']+(?<!(gif|img)))[\'"]', ce)
                    img = imgsrc.group(1)
                except:
                    imgsrc = re.search('img[^<>\\n]+src=[\'"]([^"\']+(?<!(gif|img)))[\'"]', item[ "summary" ])
                    try:
                        img = imgsrc.group(1)
                    except:
                        if len(item[ 'links' ]) >= 1:
                            piclink = ''
                            for link in item[ 'links' ]:
                                if re.search('.*(png|jpg|jpeg)', link['href']):
                                    piclink = link['href']
                                    break
                        if piclink != '':
                            img = str(piclink)
                        else:
                            img = 'http://dzmlsvv5f118.cloudfront.net/wp-content/uploads/2013/04/newsandblogimage.jpg?cc475f'
    
    
            description = item[ "summary" ]
            description = re.sub('<p[^>\\n]*>','\n\n',description)
            description = re.sub('<br[^>\\n]*>','\n',description)
            description = re.sub('<[^>\\n]+>','',description)
            description = re.sub('\\n\\n+','\n\n',description)
            description = re.sub('(\\w+,?) *\\n(\\w+)','\\1 \\2',description)
            description = HTMLParser.HTMLParser().unescape(description).strip()
    
            pubdate = item[ "published" ]
    
            WINDOW.setProperty( "LatestNews.%s.Title" % (x), title )
            WINDOW.setProperty( "LatestNews.%s.Desc" % (x), description )
            WINDOW.setProperty( "LatestNews.%s.Logo" % (x), img )
            WINDOW.setProperty( "LatestNews.%s.Date" % (x), pubdate )
            WINDOW.setProperty( "LatestNews.%s.HeaderPic" % (x), headerpic )
            x+=1
    
        for i in range(x,50):
            WINDOW.clearProperty('LatestNews.%s.Title' % i)
            WINDOW.clearProperty('LatestNews.%s.Desc' % i)
            WINDOW.clearProperty('LatestNews.%s.Logo' % i)
            WINDOW.clearProperty('LatestNews.%s.Date' % i)
            WINDOW.clearProperty('LatestNews.%s.HeaderPic' % i)
    
    
    
