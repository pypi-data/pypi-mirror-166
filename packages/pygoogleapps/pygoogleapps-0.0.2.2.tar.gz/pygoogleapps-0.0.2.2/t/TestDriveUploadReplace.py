import pytest
import os, sys, shutil
import datetime
from fileinput import close
sys.path.append('.')
import googleapps

def setup_module():
    googleapps.ServiceManager.oauth_credential_directory='t/test-account-client'
    googleapps.ServiceManager.oauth_secret_file = 'test-account-client.json'

class TestDownload():
    def setup_class(self):
        self.debug = True
        self.convertedfile = googleapps.drive.upload(filepath="t/upload_sources/ssheet.xlsx", 
                                                     name="googlesheet",
                                                     )
        self.debug = False
        self.unconverted_xls = googleapps.drive.upload(filepath="t/upload_sources/ssheet.xlsx", 
                                                       name="sheet.xlsx", 
                                                       convert=False)
        self.modtime = datetime.datetime(1997, 8, 29, 2, 14)
        self.oldfile = googleapps.drive.upload(filepath="t/upload_sources/raw_text", 
                                               modified_time=self.modtime)
        if os.path.exists('t/download_test'):
            shutil.rmtree('t/download_test')
        os.mkdir('t/download_test')
        
        
    def test_download(self):
        file = googleapps.drive.get(self.oldfile.id)
        file.download('t/download_test/file_test_1')
        assert os.path.exists('t/download_test/file_test_1')
        
        stat = os.stat('t/download_test/file_test_1')
        assert stat.st_mtime == self.modtime.timestamp()

        
    def test_converted_download(self):
        file = googleapps.drive.get(self.convertedfile.id)
        file.download('t/download_test')
        assert os.path.exists('t/download_test/' + file.name + '.xlsx')
        file.download('t/download_test', mime_type='application/vnd.oasis.opendocument.spreadsheet')
        assert os.path.exists('t/download_test/' + file.name + '.ods')

        
        #with pytest.raises(Exception e):
        #    print("WHAT EXCEPTION", e)
            
 
 
    def test_replace(self):
        file = googleapps.drive.get(self.oldfile.id)
        file.replace('t/upload_sources/raw_text_replacement')
        file.save()


class TestFileUpload():

    def setup_class(self):
        files = googleapps.drive.find_all('ssheet.xlsx')
        if files:
            for file in files:
                file.delete()
            
        files = googleapps.drive.find_all('raw_text')
        if files:
            for file in files:
                file.delete()

    def teardown_class(self):
        file = googleapps.drive.find('ssheet.xlsx')
        #file.delete()

        file = googleapps.drive.find('raw_text')
        #file.delete()

     
    def test_upload(self):
        file = googleapps.drive.upload(filepath="t/upload_sources/raw_text")
        assert file.id
        assert file.name == 'raw_text'
        #assert file.mime_type == 'application/vnd.google-apps.unknown'
        assert file.file_type == 'file'
        
        test = googleapps.drive.get(file.id)
        assert test.id == file.id
        assert test.name == file.name
        #assert file.mime_type == test.mime_type
        assert file.md5_checksum == test.md5_checksum
        orig_md5 = file.md5_checksum 
        
        test.replace('t/upload_sources/raw_text_replacement')
        assert test.id == file.id
        assert test.name == file.name
        #assert file.mime_type == test.mime_type
        assert file.md5_checksum != test.md5_checksum
        assert test.md5_checksum != orig_md5 
        
        file.refresh()
        assert file.md5_checksum == test.md5_checksum 
                
    def test_upload_and_not_convert(self):
        file = googleapps.drive.upload(filepath="t/upload_sources/ssheet.xlsx", convert=False)
        assert file.id
        assert file.name == 'ssheet.xlsx'
        assert file.mime_type == googleapps.drive.MimeType.ms_excel
        assert file.file_type == 'microsoft_excel'
        assert file.document_type == 'spreadsheet'

        test = googleapps.drive.get(file.id)
        assert test.id == file.id
        assert test.name == file.name
        assert file.mime_type == test.mime_type
        assert file.md5_checksum == test.md5_checksum
     
    def test_upload_and_convert(self):
        file = googleapps.drive.upload(filepath="t/upload_sources/ssheet.xlsx", name="googlesheet")
        assert file.id
        assert file.name == 'googlesheet'
        assert file.mime_type == googleapps.drive.MimeType.google_spreadsheet
        assert file.file_type == 'google_sheets'
        assert file.document_type == 'spreadsheet'

        test = googleapps.drive.get(file.id)
        assert test.id == file.id
        assert test.name == file.name
        assert file.mime_type == test.mime_type
        assert file.md5_checksum == test.md5_checksum


