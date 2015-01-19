import common

import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import simplejson as json
from datetime import datetime, tzinfo

# Use the android app urls to fetch episodes
EPISODES_URL = 'http://api.comedycentral.com/feeds/ccnetworkapp/android/1.0/series/items/' \
               'd25c3f16-1730-4a83-9609-bcf680653d7e?key=ccnetworkapp1.0&numberOfItems=40&pageNumber=1' \
               '&filterType=season&filterValue=&episodesOnly=true'


def root():
    _add_directory('Full Episodes', 'full_episodes', 'list')
    xbmcplugin.endOfDirectory(common.pluginhandle)

def full_episodes():
    exec('full_episodes_' + common.args.sitemode + '()')


def full_episodes_list():
    data = json.loads(common.get_url(EPISODES_URL))
    total = len(data['result']['items'])

    for item in data['result']['items']:
        video = None
        for vid_item in item['items']:
            if vid_item['episodeType'] == 'fullEpisode':
                video = vid_item
                break

        if video is None:
            continue

        image = item['images'][0]
        thumb = image['url']
        airdate = datetime.fromtimestamp(float(video['airDate']))
        duration = str(int(video['duration']) / 60)

        labels = {
            'title': item['headerText'],
            'tvshowtitle': 'The Daily Show',
            'plot': video['description'],
            'tagline': video['shortDescription'],
            'studio': 'Comedy Central',
            'year': airdate.strftime('%Y'),
            'aired': airdate.strftime('%Y-%m-%d'),
            'duration': duration
        }

        if video['season']:
            labels['season'] = video['season']['seasonNumber']
            labels['episode'] = video['season']['episodeNumber'][-3:]

        li = xbmcgui.ListItem(item['headerText'], iconImage=thumb, thumbnailImage=thumb)
        li.setInfo(type='Video', infoLabels=labels)
        #item.setProperty('fanart_image', fanart)
        #item.setProperty('TVShowThumb', poster)

        li.addStreamInfo('video', {
            'codec': 'h264',
            'width': image['width'],
            'height': image['height'],
            'duration': duration
        })

        contextmenu = []

        contextmenu.append(('Episode Information', 'XBMC.Action(Info)'))

        li.addContextMenuItems(contextmenu)

        u = sys.argv[0] + '?url={0}&mode=full_episodes&sitemode=play'.format(video['canonicalURL'])

        xbmcplugin.addDirectoryItem(common.pluginhandle, url=u, listitem=li, isFolder=False, totalItems=total)

    xbmcplugin.endOfDirectory(common.pluginhandle)


def full_episodes_play():
    url = common.args.url
    kiosk = 'yes'
    if common.get_setting('usekioskmode') == 'false':
        kiosk = 'no'

    kiosk = 'yes'  # TODO make option
    xbmc.executebuiltin("RunPlugin(plugin://plugin.program.chrome.launcher/?url=" + urllib.quote_plus(
            url) + "&mode=showSite&stopPlayback=yes&kiosk=" + kiosk + ")")

    xbmcplugin.setResolvedUrl(common.pluginHandle, True, xbmcgui.ListItem())


def _add_directory(name, mode='', sitemode='', directory_url='', thumb=None, fanart=None, description=None,
                  contextmenu=None, is_folder=True):
    if fanart is None:
        fanart = common.__fanart__
    infoLabels = {'title': name,
                  'plot': description}
    u = sys.argv[0]
    u += '?url="' + urllib.quote_plus(directory_url) + '"'
    u += '&mode="' + mode + '"'
    u += '&sitemode="' + sitemode + '"'
    item = xbmcgui.ListItem(name, iconImage=thumb, thumbnailImage=thumb)
    item.setProperty('fanart_image', fanart)
    item.setInfo(type='Video', infoLabels=infoLabels)

    if contextmenu:
        item.addContextMenuItems(contextmenu)

    xbmcplugin.addDirectoryItem(common.pluginhandle, url=u, listitem=item, isFolder=is_folder)

