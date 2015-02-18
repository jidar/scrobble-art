import consts
import rest
from functools import wraps
import json

from base import ArtistObject, ImageObject, AlbumObject

class User():
    def __init__(self, config):
        self.config = config
    
    def _get(self, method, **kwargs):
        params = {} if 'params' not in kwargs else kwargs['params']
        params['user'] = self.config.username
        params['api_key'] = self.config.apikey

        if 'format' not in params:
            params['format'] = consts.FORMAT
        
        if 'method' not in params:
            params['method'] = 'user.%s'%(method)

        return rest.get(self.config.apiurl, params).content
    
    def getArtistTracks():
        pass
    
    def getBannedTracks():
        pass
    
    def getEvents():
        pass
    
    def getFriends():
        pass
    
    def getInfo():
        pass
    
    def getLovedTracks(limit=None, page=None):
        '''
        Optional: limit (result return limit, default 50)
                  page (page of search results to return, default 1)
        '''
        params = {}
        if limit is not None:
            params['limit'] = limit
            
        if page is not None:
            params['page'] = page

        tracks = json.loads(self._get('getLovedTracks', params=params))['lovedtracks']['track']
        return tracks        
        #TODO: Need track object in base.py
    
    def getNeighbours():
        pass
    
    def getNewReleases():
        pass
    
    def getPastEvents():
        pass
    
    def getPersonalTags():
        pass
    
    def getPlaylists():
        pass
    
    def getRecentStations():
        pass
    
    def getRecentTracks():
        pass
    
    def getRecommendedArtists():
        pass
    
    def getRecommendedEvents():
        pass
    
    def getShouts():
        pass
    
    def getTopAlbums(self, limit=None, page=None, period=None):
        '''
        Optional: limit (result return limit, default 50)
                  page (page of search results to return, default 1)
                  period (overall, 7day, 1month, 3month, 6month, 12month)
        '''
        params = {}
        if limit is not None:
            params['limit'] = limit
            
        if page is not None:
            params['page'] = page
            
        if page is not None:
            params['period'] = period
        
        data = (json.loads(self._get('getTopAlbums', params=params))['topalbums']['album'])
        albums = []
        for album in data:
            albums.append(AlbumObject(album))
        return albums
    
    def getTopArtists(self, limit=None, page=None, period=None):
        '''
        Optional: limit (result return limit, default 50)
                  page (page of search results to return, default 1)
                  period (overall, 7day, 1month, 3month, 6month, 12month)
        '''
        params = {}
        if limit is not None:
            params['limit'] = limit
            
        if page is not None:
            params['page'] = page
            
        if page is not None:
            params['period'] = period
            
        data = (json.loads(self._get('getTopArtists',params=params))['topartists']['artist'])
        artists = []
        for artist in data:
            artists.append(ArtistObject(artist))
        return artists
    
    def getTopTags():
        pass
    
    def getTopTracks(self, **kwargs):
        return json.loads(_get('getTopTracks'))['toptracks']['track']
    
    def getWeeklyAlbumChart():
        pass
    
    def getWeeklyArtistChart():
        pass
    
    def getWeeklyChartList():
        pass
    
    def getWeeklyTrackChart():
        pass
    
    def shout():
        pass