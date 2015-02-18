import userclient as _uc
import consts

class _config():
    def __init__(self, username, apikey, apiurl):
        self.username = username
        self.apikey = apikey
        self.apiurl = apiurl
        if self.apiurl == None:
            self.apiurl = consts.APIURL

class LastAPI():
    def __init__(self, username, apikey, apiurl = None):
        self.user = None
        if apikey == None:
            apikey = consts.APIURL

        self._config = _config(username, apikey, apiurl)

        self.user = _uc.User(self._config)

    
    



