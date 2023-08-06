import pytest
import os, sys, shutil
sys.path.append('.')
import googleapps

def setup_module():
    googleapps.ServiceManager.oauth_credential_directory='t/auth-credentials'
    googleapps.ServiceManager.oauth_secret_file = 't/test-account-client/test-account-client.json'
    googleapps.sheets.Spreadsheet.debug=True

class TestSheet():

    def setup_class(self):
        self.objects = []
        existing = googleapps.drive.find_all(filename='Test Create Sheet!')
        for f in existing:
            f.delete()
        
        
        
    def test_create_deferred(self):
        
        wb = googleapps.sheets.create('Test Create Sheet!')
        ws = wb.add_worksheet("Test Sheet 1")
        ws.update_cells(0,0,[1, 2, '3', '4'])
        ws.update_cells(1,0,['A','B','C','D'])
        ws.update_cells(2,10, 'X') 
        ws.update_cells(3,5, [ ['A1', 'A2', 'A3'], ['B1','B2','B3'], ['C1'], ['D1','D2','D3','D4','D5'] ])
        ws.title = "Renamed Sheet!"
        
        # wb has no ID, and ID will trigger autocommit, so we search by google drive
        # hopefully google drive works right!    
        existing = googleapps.drive.find_all(filename='Test Create Sheet!')
        assert not existing
        
        wb.commit() 

        # Now make sure we can find it via google drive
        existing = googleapps.drive.find_all(filename='Test Create Sheet!')
        assert existing
        
        # now see if we can get it by wb id
        testwb = googleapps.sheets.get(wb.id)
        assert testwb
        testws = testwb.get_worksheet("Renamed Sheet!")
        assert(testws)
        # test some values, and ensure types are correct
        assert(testws.get_cell(0,0) == 1)
        assert(testws.get_cell(0,2) == '3')
        assert(testws.get_cell(0,2) != 3)
        assert(testws.get_cell(3,5) == 'A1')
        assert(testws.get_cell(5,5) == 'C1')
        assert(testws.get_cell(6,6) == 'D2')
        
