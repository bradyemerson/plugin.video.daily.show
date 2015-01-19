#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import urllib
import urllib2
from datetime import datetime
import time
import unicodedata

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin


pluginhandle = int(sys.argv[1])

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')
__addonname__ = __addon__.getAddonInfo('name')
__addonpath__ = __addon__.getAddonInfo('path').decode('utf-8')
__addonprofile__ = xbmc.translatePath(__addon__.getAddonInfo('profile')).decode('utf-8')
__icon__ = __addon__.getAddonInfo('icon')
__fanart__ = __addon__.getAddonInfo('fanart')


class _Info:
    def __init__(self, s):
        args = urllib.unquote_plus(s).split(' , ')
        for x in args:
            try:
                (k, v) = x.split('=', 1)
                setattr(self, k, v.strip('"\''))
            except:
                pass
        if not hasattr(self, 'url'):
            setattr(self, 'url', '')


args = _Info(sys.argv[2][1:].replace('&', ' , '))


def get_setting(setting):
    return __addon__.getSetting(setting)


def get_url(url, values=None, header={}, amf=False):
    try:
        old_opener = urllib2._opener
        print 'Daily Show :: getURL :: url = ' + url
        if values is None:
            req = urllib2.Request(bytes(url))
        else:
            if amf is False:
                data = urllib.urlencode(values)
            elif amf is True:
                data = values
            req = urllib2.Request(bytes(url), data)
        header.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
        for key, value in header.iteritems():
            req.add_header(key, value)
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        urllib2.install_opener(old_opener)
    except urllib2.HTTPError, error:
        print 'HTTP Error reason: ', error
        return False
    else:
        return link
