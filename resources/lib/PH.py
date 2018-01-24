#!/usr/bin/python

import xbmc
import xbmcaddon
import xbmcgui
import json
import re


import xbmcplugin
import datetime
import urllib2
import sys
import os

class PluginHelpers():
    """
    PluginHelpers Class offers plugin developers a wide range of easy to use functions
    """
    def __init__(self):
        url=''

##########################################################################################################################
##
##########################################################################################################################
    def getUnicodePage(self,url):
        """
        retrieve a url webpage utf-8 encoded

        :param url: set the url to retrive
        :return: webpage content utf-8 encoded 
        """
        req = urllib2.urlopen(url)
        content = ""
        if "content-type" in req.headers and "charset=" in req.headers['content-type']:
            encoding=req.headers['content-type'].split('charset=')[-1]
            content = unicode(req.read(), encoding)
        else:
            content = unicode(req.read(), "utf-8")
        return content
    
##########################################################################################################################
##
##########################################################################################################################
    def parameters_string_to_dict(self,parameters):
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict
        
##########################################################################################################################
##
##########################################################################################################################
    def writeLog(self, message, level=xbmc.LOGNOTICE):
        try:
            xbmc.log('[plugin.program.fhemcontrol] %s' % ( message), level)
        except Exception:
            xbmc.log('[plugin.program.fhemcontrol] %s' % ('Fatal: Message could not displayed'), xbmc.LOGERROR)

##########################################################################################################################
##
##########################################################################################################################
    def debug(self, message):
        try:
            xbmc.log('[plugin.program.fhemcontrol] %s' % (message), xbmc.LOGDEBUG)
        except Exception:
            xbmc.log('[plugin.program.fhemcontrol] %s' % ('Fatal: Message could not displayed'), xbmc.LOGERROR)


##########################################################################################################################
##
##########################################################################################################################
    def notifyOSD(self,header, message, icon=xbmcgui.NOTIFICATION_INFO, disp=4000, enabled=True):
        if enabled:
            OSD = xbmcgui.Dialog()
            OSD.notification(header.encode('utf-8'), message.encode('utf-8'), icon, disp)






