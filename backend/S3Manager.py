# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:36:53 2018

@author: banderso2
"""


import boto3

class S3Manager():
    
    def __init__(self):
        self.client          = boto3.client('s3')
        self.s3              = boto3.resource('s3')
        self.bucket_name = 'nrel-nwtc-metmast-uni'
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.client.duplicate='' #Lists files with the same name of the file being uploaded
        self.keys = self.get_bucket_keys()
   

    def up_file(self,filepath,filename):
        ''' Uploads file with path 'filepath' and name 'filename' to the nrel-nwtc-metmast-uni/int bucket'''
        self.client.upload_file(filepath,self.bucket_name,filename) #upload file to bucket
        
    def is_file_in_bucket(self,filename):
        '''sets self.client.duplicate to filename if it exists already.'''
        self.get_bucket_keys()
        for string in self.keys:
            if string=='int/'+filename:
                self.client.duplicate=filename
                
    def get_bucket_keys(self):
        '''lists keys (filenames) in bucket'''
        keys = []
        for key in self.client.list_objects(Bucket=self.bucket_name)['Contents']:
            keys.append(key['Key'])
        print('Keys in bucket:')
        print(keys)
        return keys 
    
    def rename_file(self,oldname,newname):
        '''rename file in bucket'''
        self.s3.Object(self.bucket_name,'int/'+newname).copy_from(CopySource=self.bucket_name+'/int/'+oldname)
        self.s3.Object(self.bucket_name,'int/'+oldname).delete()
    
    def up_file_master(self,filepath,filename):
        ''' Uploads file with path 'filepath' and name 'filename' to the nrel-nwtc-metmast-uni/int bucket. 
        Includes functions to perform upload and handle duplicate files.'''
        self.is_file_in_bucket(filename)
        if self.client.duplicate:
            # handle duplicate files
            print('a file named '+self.client.duplicate+ ' already exists in '+ self.bucket_name+'. Would you like to replace it? (y/n)')
            while 1:
                change=input('--> ')
                if change == 'y':
                    self.s3.Object(self.bucket_name, 'int/'+self.client.duplicate).delete()
                    self.up_file(filepath,'int/'+filename)
                    print('replaced')
                    change==''
                    self.client.duplicate==''
                    break
                elif change == 'n':
                    print('not replaced')
                    change==''
                    self.client.duplicate==''
                    break
        else:
            self.up_file(filepath,'int/'+filename)
            print(filename+' uploaded')
        

if __name__=='__main__':  
    filename='ben.txt'
    filepath='C:/Users/banderso2/Desktop/ben.txt'
    s3_manager=S3Manager() #create S3Manager object
    print(s3_manager.bucket) 
    s3_manager.up_file_master(filepath,filename)
    s3_manager.rename_file('ben.txt','moby_dick')
#    if s3_manager.client.duplicate:
#        # handle duplicate files
#        print('a file named '+s3_manager.client.duplicate+ ' already exists in '+ s3_manager.bucket_name+'. Would you like to replace it? (y/n)')
#        while 1:
#            change=input('--> ')
#            if change == 'y':
#                s3_manager.s3.Object(s3_manager.bucket_name, s3_manager.client.duplicate).delete()
#                s3_manager.up_file('C:/Users/banderso2/Desktop/ben.txt',filename)
#                print('replaced')
#                change==''
#                s3_manager.client.duplicate==''
#                break
#            elif change == 'n':
#                print('not replaced')
#                change==''
#                s3_manager.client.duplicate==''
#                break
#    else:
#        s3_manager.up_file('C:/Users/banderso2/Desktop/'+filename,'int/'+filename)
#        print(filename+' uploaded')
            
    
    #check if file of the same name is there before upload
    #rename function

