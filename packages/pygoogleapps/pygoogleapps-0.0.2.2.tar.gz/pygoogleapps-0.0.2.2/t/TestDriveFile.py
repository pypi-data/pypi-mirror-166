import pytest
import os, sys, shutil
from fileinput import close
sys.path.insert(0,'.')
import googleapps

def setup_module():
    googleapps.ServiceManager.oauth_credential_directory='t/test-account-client'
    googleapps.ServiceManager.oauth_secret_file = 'test-account-client.json'

    # -- clean up old garbage
    found_files = googleapps.drive.find_all('test file 1')
    for found in found_files:
        found.delete()

class TestFileCreate():

    def setup_class(self):
        file = googleapps.drive.File(name="test file creation")
        assert file is not None
        #assert file.file_type == 'file'
        #assert file.__class__.__name__ == 'File'

        # but it hasn't actually committed it, so the id should fail
        with pytest.raises(Exception):
            file.id

        file.save()
        assert file.id is not None
        assert file.name == 'test file creation'
        file.delete()


class TestFileGet():

    test_filename = 'test file 1'

    def setup_class(self):
        file = googleapps.drive.File(name=self.test_filename)
        file.save()
        assert file.id is not None
        self.file_id = file.id

    def teardown_class(self):
        file = googleapps.drive.File(id=self.file_id)
        file.delete()

    def _verify_file(self, file):
        assert file.__class__.__name__ == 'File'
        assert file.id == self.file_id
        assert file.name == self.test_filename
        assert not file.trashed
        assert file.file_type == 'file'
        with pytest.raises(Exception):
            file.id = 'ReadOnly'
        print("---- Completed Verification -----")


    def test_get_manually(self):

        file = googleapps.drive.File(id=self.file_id)
        assert file is not None
        with pytest.raises(AttributeError):
            file.file_type
        assert file.__class__.__name__ == 'File'
        assert file.id == self.file_id

        # but it hasn't actually committed it, so asking if it is trashed should fail
        with pytest.raises(Exception):
            file.name

        with pytest.raises(Exception):
            file.trashed

        print("---------- ABOUT TO LOAD ---------------")
        file.load()
        self._verify_file(file)
        print("-------------------------")


    def test_find(self):

        found_file = googleapps.drive.find('test file 1')
        assert found_file
        self._verify_file(found_file)
