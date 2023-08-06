import pytest
import os, sys, shutil
from fileinput import close
sys.path.append('.')
import googleapps
import googleapps.drive

def setup_module():
#    with open('t/test-account-client/test-api-key.txt', 'r') as f:
#        api_key = f.readline()
    googleapps.ServiceManager.oauth_credential_directory='t/test-account-client'
    googleapps.ServiceManager.oauth_secret_file = 'test-account-client.json'

class TestFolder():

    def setup_class(self):
        test_names = ['New Directory', 'Trunk', 'Branch', 'Twig', 'New Copy', 
                      'Copy to Trash', 'Copy to Delete', 'Wild File']
        old_objects = googleapps.drive.find_all(name=test_names)
        if old_objects:
            for obj in old_objects:
                if obj.name not in test_names:
                    raise Exception("WHAT THE HELL?! find_all returned something that wasn't specified: " + obj.name )
                obj.delete()
        self.objects = []


    def test_simple_new_directory(self):
        dir = googleapps.drive.Folder(name='New Directory')
        # make sure it hasn't been commited yet
        found = googleapps.drive.find(name='New Directory')
        assert not found
        dir.save()
        found = googleapps.drive.find(name='New Directory')
        assert found 
        assert found.id == dir.id
        assert found.modified_time == dir.modified_time
        assert found.__class__.__name__ == 'Folder'        
        dir.delete()
        
        with pytest.raises(Exception):
            dir.mime_type = 'something else'
            
        
    def test_create_with_commits(self):

        trunk = googleapps.drive.Folder(name='Trunk')
        assert trunk is not None
        assert trunk.mime_type == 'application/vnd.google-apps.folder'
        assert trunk.__class__.__name__ == 'Folder'
        with pytest.raises(AttributeError):
            trunk.id
        trunk.save()
        assert trunk.id
        
        branch = googleapps.drive.create_folder('Branch', in_folder=trunk)
        # not committed, make 
        assert branch.__class__.__name__ == 'Folder'
        assert branch.parents
        assert branch.parents[0] == trunk.id
        assert branch.folder 
        assert branch.folder.id == trunk.id
        #with pytest.raises(AttributeError):
        #    branch.id
        branch.save()
        # and committed...
        assert branch.__class__.__name__ == 'Folder'
        assert branch.parents
        assert branch.parents[0] == trunk.id
        assert branch.folder 
        assert branch.folder.id == trunk.id

        assert trunk.id in branch.parents
        twig = googleapps.drive.create_folder('Twig', in_folder=branch)
        assert twig is not None
        assert twig.__class__.__name__ == 'Folder'
        assert trunk.id not in twig.parents
        assert branch.id in twig.parents

        checktwig = googleapps.drive.get(twig.id)
        assert checktwig.name == twig.name
        for pid in checktwig.parents:
            assert pid in twig.parents

        file1 = googleapps.drive.create('Wild File')
        assert file1.__class__.__name__ == 'File'
        # TODO: figure out how to get the actual root directory key, as it will be here
        #assert len(file1.parents) == 0
        
        file2 = googleapps.drive.create('Branched File', in_folder=branch)
        assert file2.__class__.__name__ == 'File'
        assert branch.id in file2.parents

        copy = file2.copy('Branched Copy')
        assert file2.id != copy.id
        assert file2.__class__.__name__ == 'File'
        
        copy.rename('Copied')
        assert copy.name == 'Copied'
        testcopy = googleapps.drive.get(copy.id)
        assert copy.name == testcopy.name
                
        file2.move(twig)
        assert twig.id in file2.parents
        assert branch.id not in file2.parents

        assert not file2.trashed
        
        # deleted files are permanent and so they can't be found anywhere
        #with pytest.raises(FileNotFoundError):
        #    file2_verify = googleapps.drive.DriveItem(file2.id, defer_load=False)

        nextcopy = copy.copy('Copy to Delete', to_folder=twig)
        assert nextcopy.__class__.__name__ == 'File'

        ary = googleapps.drive.find_all(name=nextcopy.name, in_folder=twig)
        assert ary and len(ary) == 1
        test = ary[0]
        assert test.id == nextcopy.id
        assert twig.id in test.parents
        test.delete()
        test2 = googleapps.drive.find(name=nextcopy.name, in_folder=twig)
        assert not test2
        found = False
        for trashed_copies in googleapps.drive.find_all(name=nextcopy.name, trashed=True):
            if trashed_copies.id == nextcopy.id:
                found = True
                break
        assert not found, "Found deleted file in the trash with id " + nextcopy.id + ", but deleted files should NOT be trashed"
         
        # now do the same test, with trashing
        thirdcopy = copy.copy('Copy to Trash', to_folder=twig)
        thirdcopy.trashed = True
        find_nottrashed= googleapps.drive.find(name=thirdcopy.name, in_folder=twig)
        assert not find_nottrashed
        found = False
        for trashed_copies in googleapps.drive.find_all(name=thirdcopy.name, trashed=True):
            if trashed_copies.id == thirdcopy.id:
                found = True
                break
        
        assert found, "Did not find TRASHED file in the trash with id " + thirdcopy.id 
         
        
        
        # this should be something, right?
#        assert nextcopy.id == test2.id

        # now do some updates

        '''
        # try uploading
        ssheet = googleapps.drive.upload('t/upload_sources/ssheet.xlsx')
        assert(ssheet)
        assert ssheet.__class__.__name__ == 'File'
        
        presentation = googleapps.drive.upload('t/upload_sources/presentation.odp',
                                               in_folder=twig,
                                               name='presentthis.odp',
                                               convert=False)
        assert(presentation)
        assert presentation.__class__.__name__ == 'File'

        # download
        path = presentation.download('t/downloads/output.odp')
        path = presentation.download(directory='t/downloads')
        path = ssheet.download('t/downloads/output.ods')
        path = ssheet.download(directory='t/downloads', file_type='xlsx')
        path = ssheet.download('t/downloads/output.csv')
        path = ssheet.download('wtf.tsv', directory='t/downloads')
        
        #future
#        leaf = googleapps.drive.Folder.create('Leaf', path=['Root', 'Branch', 'Twig'])
        '''
