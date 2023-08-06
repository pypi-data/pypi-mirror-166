import GoogleApps


class TestService(GoogleApps.Service):
    credential_searchpath=['t']
    default_services = {
        'drive':'',
        'sheets':'',
    }
    
    def __init__(self):
        pass
