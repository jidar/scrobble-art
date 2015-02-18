class ImageObject(object):
    def __init__(self, image_list):
        self.images = {}
        self._sizelist = ['small', 'medium', 'large', 'extralarge', 'mega']
        try:
            for image in image_list:
                for size in self._sizelist:
                    if image['size'] == size:
                        self.images[size] = image['#text']
        except Exception as e:
            print "Unable to initialize ImageObject"
            print e
        
        self.select_largest()
        
    def __repr__(self):
        repr_str = ''
        for image in self.images:
            repr_str = repr_str + self.images[image] + '\n'
            
        return repr_str

    def select_smallest(self):
        self.selected = self.images[self._sizelist[0]]
    
    def select_largest(self):
        for i in range(0, len(self._sizelist)):
            if self._sizelist[i] in self.images:
                self.selected = self.images[self._sizelist[i]]
        
    def get_selected_image_url(self):
        return self.selected


class AlbumObject():
    def __init__(self, album_dict):
        {u'@attr': {u'rank': u'1'},
         u'name': u'All The Pain Money Can Buy',
         u'artist': {u'url': u'http://www.last.fm/music/Fastball', u'mbid': u'dc083bd6-41a3-436e-9e0a-28b4dc773820', u'name': u'Fastball'},
         u'url': u'http://www.last.fm/music/Fastball/All+The+Pain+Money+Can+Buy',
         u'image': [{u'#text': u'http://userserve-ak.last.fm/serve/34s/9755249.jpg', u'size': u'small'}, {u'#text': u'http://userserve-ak.last.fm/serve/64s/9755249.jpg', u'size': u'medium'}, {u'#text': u'http://userserve-ak.last.fm/serve/126/9755249.jpg', u'size': u'large'}, {u'#text': u'http://userserve-ak.last.fm/serve/300x300/9755249.jpg', u'size': u'extralarge'}],
         u'mbid': u'58a38efc-17bc-4bab-ba9d-378a9eec5d8b',
         u'playcount': u'61'}
        self.name = None
        self.artist = None
        self.url = None
        self.images = None
        self.mbid = None
        self.playcount = None
        self.rank = None
        self.raw = album_dict
        
        if 'artist' in album_dict:
            self.artist = ArtistObject(album_dict['artist'])
            
        if 'image' in album_dict:
            self.images = ImageObject(album_dict['image'])
        
        if '@attr' in album_dict:
            if 'rank' in album_dict[u'@attr']:
                self.rank = album_dict[u'@attr']['rank']
        
        if 'name' in album_dict:
            self.name = album_dict['name']
        
        if 'url' in album_dict:
            self.url = album_dict['url']
        
        if 'mbid' in album_dict:
            self.mbid = album_dict['mbid']
        
        if 'playcount' in album_dict:
            self.placount = album_dict['playcount']
            
    def __repr__(self):
        return 'name: %s\nrank: %s\nmbid: %s\n url: %s\nplaycount: %s\nartist: %s\nimages: %s\n'%(
            self.name,
            self.rank,
            self.mbid,
            self.url,
            self.playcount,
            self.artist,
            self.images)            

class ArtistObject():
    def __init__(self, artist_dict):
        self.streamable = False
        self.rank = None
        self.name = None
        self.url = None
        self.mbid = None
        self.images = None
        self.raw = artist_dict
        try:
            if 'image' in artist_dict:
                self.images = ImageObject(artist_dict['image'])
            if 'streamable' in artist_dict:
                if artist_dict['streamable'] == u'1':
                    self.streamable = True
            if '@attr' in artist_dict:
                if 'rank' in artist_dict[u'@attr']:
                    self.rank = artist_dict[u'@attr']['rank']
            
            if 'name' in artist_dict:
                self.name = artist_dict[u'name']
            
            if 'url' in artist_dict:
                self.url = artist_dict[u'url']
                
            if 'mbid' in artist_dict:
                self.mbid = artist_dict[u'mbid']
            
            if 'playcount' in artist_dict:
                self.playcount = artist_dict[u'playcount']
        except Exception as e:
            print "Unable to initialize ArtistObject"
            print e
            
    def __repr__(self):
        return 'name: %s\nrank: %s\nmbid: %s\n url: %s\nstreamable: %s\nimages: %s\n'%(
            self.name,
            self.rank,
            self.mbid,
            self.url,
            self.streamable,
            self.images)
#
#class BaseConfig(object):
#    def __init__(self, request_format, username, apikey, api_url):
#        self.default_params = {}
#        self.default_params['format'] = request_format
#        self.default_params['user'] = username
#        self.default_params['api_key'] = apikey
#        self.api_url = api_url
#        
#class Album(BaseClient):
#    
#    def addTags():
#        pass
#
#    def getBuylinks():
#        pass
#
#    def getInfo():
#        pass
#
#    def getShouts():
#        pass
#
#    def getTags():
#        pass
#
#    def getTopTags():
#        pass
#
#    def removeTag():
#        pass
#
#    def search():
#        pass
#
#    def share():
#        pass
#
#        
#class Artist(BaseClient):
#    def addTags():
#        pass
#
#    def getCorrection():
#        pass
#
#    def getEvents():
#        pass
#
#    def getInfo():
#        pass
#
#    def getPastEvents():
#        pass
#
#    def getPodcast():
#        pass
#
#    def getShouts():
#        pass
#
#    def getSimilar():
#        pass
#
#    def getTags():
#        pass
#
#    def getTopAlbums():
#        pass
#
#    def getTopFans():
#        pass
#
#    def getTopTags():
#        pass
#
#    def getTopTracks():
#        pass
#
#    def removeTag():
#        pass
#
#    def search():
#        pass
#
#    def share():
#        pass
#
#    def shout():
#        pass
#
#class Auth(BaseClient):
#    def getMobileSession():
#        pass
#
#    def getSession():
#        pass
#
#    def getToken():
#        pass
#
#class Chart(BaseClient):
#    def getHypedArtists():
#        pass
#
#    def getHypedTracks():
#        pass
#
#    def getLovedTracks():
#        pass
#
#    def getTopArtists():
#        pass
#
#    def getTopTags():
#        pass
#
#    def getTopTracks():
#        pass
#
#class Event(BaseClient):
#    def attend():
#        pass
#
#    def getAttendees():
#        pass
#
#    def getInfo():
#        pass
#
#    def getShouts():
#        pass
#
#    def share():
#        pass
#
#    def shout():
#        pass
#
#class Geo(BaseClient):
#    def getEvents():
#        pass
#
#    def getMetroArtistChart():
#        pass
#
#    def getMetroHypeArtistChart():
#        pass
#
#    def getMetroHypeTrackChart():
#        pass
#
#    def getMetroTrackChart():
#        pass
#
#    def getMetroUniqueArtistChart():
#        pass
#
#    def getMetroUniqueTrackChart():
#        pass
#
#    def getMetroWeeklyChartlist():
#        pass
#
#    def getMetros():
#        pass
#
#    def getTopArtists():
#        pass
#
#    def getTopTracks():
#        pass
#
#class Group(BaseClient):
#    def getHype():
#        pass
#
#    def getMembers():
#        pass
#
#    def getWeeklyAlbumChart():
#        pass
#
#    def getWeeklyArtistChart():
#        pass
#
#    def getWeeklyChartList():
#        pass
#
#    def getWeeklyTrackChart():
#        pass
#
#class Library(BaseClient):
#    def addAlbum():
#        pass
#
#    def addArtist():
#        pass
#
#    def addTrack():
#        pass
#
#    def getAlbums():
#        pass
#
#    def getArtists():
#        pass
#
#    def getTracks():
#        pass
#
#    def removeAlbum():
#        pass
#
#    def removeArtist():
#        pass
#
#    def removeScrobble():
#        pass
#
#    def removeTrack():
#        pass
#
#class Playlist(BaseClient):
#    def addTrack():
#        pass
#
#    def create():
#        pass
#
#class Radio(BaseClient):
#    def getPlaylist():
#        pass
#
#    def search():
#        pass
#
#    def tune():
#        pass
#
#class Tag(BaseClient):
#    def getInfo():
#        pass
#
#    def getSimilar():
#        pass
#
#    def getTopAlbums():
#        pass
#
#    def getTopArtists():
#        pass
#
#    def getTopTags():
#        pass
#
#    def getTopTracks():
#        pass
#
#    def getWeeklyArtistChart():
#        pass
#
#    def getWeeklyChartList():
#        pass
#
#    def search():
#        pass
#
#class Tasteometer(BaseClient):
#    def compare():
#        pass
#
#    def compareGroup():
#        pass
#
#class Tag(BaseClient):
#    def addTags():
#        pass
#
#    def ban():
#        pass
#
#    def getBuylinks():
#        pass
#
#    def getCorrection():
#        pass
#
#    def getFingerprintMetadata():
#        pass
#
#    def getInfo():
#        pass
#
#    def getShouts():
#        pass
#
#    def getSimilar():
#        pass
#
#    def getTags():
#        pass
#
#    def getTopFans():
#        pass
#
#    def getTopTags():
#        pass
#
#    def love():
#        pass
#
#    def removeTag():
#        pass
#
#    def scrobble():
#        pass
#
#    def search():
#        pass
#
#    def share():
#        pass
#
#    def unban():
#        pass
#
#    def unlove():
#        pass
#
#    def updateNowPlaying():
#        pass
#
#class Venue(BaseClient):
#    def getEvents():
#        pass
#
#    def getPastEvents():
#        pass
#
#    def search():
#        pass
#
#        