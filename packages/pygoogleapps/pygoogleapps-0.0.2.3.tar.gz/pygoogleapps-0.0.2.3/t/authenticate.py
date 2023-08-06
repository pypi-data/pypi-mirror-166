import pytest
import os, sys, shutil
sys.path.append('.')
import googleapps

# This re/creates an aunthenticated credential.
# It is not an automated test because it requires user input to authorize 
# access via the web. 

# We're not super fancy here.  In order to use this test you need to have a live set of credentials
# We're using a fake google account here.

# For your real work, go here and create a project wuth credentials:
# https://console.developers.google.com


# create a subclass to encapsulate the parameters
class EncapsulatedServiceManager(googleapps.ServiceManager):
    def __init__(self, *args, **kwargs):
        self.detach_services()
        super().__init__(*args, **kwargs)


class AuthorizationTest():
    service = None
    
    def setup_class(cls):
        # delete the test credential tree if it exists (because we'll auto-create it)
        if os.path.exists('t/auth-credentials'):
            shutil.rmtree('t/auth-credentials')
        assert not os.path.exists('t/auth-credentials')

    def teardown_class(cls):
        if os.path.exists('t/auth-credentials'):
            shutil.rmtree('t/auth-credentials')
        assert not os.path.exists('t/auth-credentials')
            
    def test_spreadsheet_service(self):
        sheet_service = self.service.load_service('sheets.readonly')
        assert sheet_service.spreadsheets()
        assert sheet_service.spreadsheets().values()

    def test_drive_service(self):
        drive_service = self.service.load_service('drive.readonly')
        assert drive_service
        assert drive_service.revisions()


class TestAPIKey(AuthorizationTest):
    
    # create the service object that we use
    def setup_class(cls):
        super().setup_class(cls)
        # read the api key from the text file where it should be stored
        with open('t/test-account-client/test-api-key.txt', 'r') as f:
            api_key = f.readline()
        
        cls.service = EncapsulatedServiceManager( api_key = api_key )


        
class TestOAuth2(AuthorizationTest):

    # create the service object that we use
    def setup_class(cls):
        super().setup_class(cls)
        cls.service = EncapsulatedServiceManager(
            oauth_credential_directory='t/auth-credentials',
            oauth_secret_file = 't/test-account-client/test-account-client.json',
        )

        

class TestSanity():
    # this is just so everything dies in a vacuum
    def test_failure(self):
        with pytest.raises(Exception):
            # this should fail because none of these credentials should exist
            service = EncapsulatedServiceManager()
            drive_service = service.load_service('drive.readonly')
            rev = drive_service.revisions()
            
        def setup_class(cls):
            shutil.rmtree('t/no-credentials')
            
        def teardown_class(cls):
            shutil.rmtree('t/no-credentials')
        
