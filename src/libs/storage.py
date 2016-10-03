########### Python 2.7 #############
import sys
import time
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions,
    BlobPermissions,
    PublicAccess,
)

class BlobStorageContainer:
    def __init__(self,account_name,account_key,container_name):
        self.__blobservice = BlockBlobService(
                            account_name=account_name,
                            account_key=account_key)
        self.__container_name = container_name

    def __list_blobs_with_prefix(self, postfix):
        bloblist =[]
        postfix_l = postfix.lower()
        generator = self.__blobservice.list_blobs(self.__container_name)
        for blob in generator:
            t = blob.name.split('.')
            if (postfix_l == t[-1].lower()):
                bloblist.append(blob.name)
        return bloblist

    def set_container_acl_public(self):
        self.__blobservice.set_container_acl(
                    self.__container_name,
                    public_access=PublicAccess.Container)

    def set_container_acl_private(self):
        self.__blobservice.set_container_acl(self.__container_name)


    def get_blobs_list (self, postfix):
        blobs = self.__list_blobs_with_prefix(postfix)
        return blobs

#if __name__ == '__main__': 
#    account_name = 'xxxxx'
#    account_key = 'FrDc4xbqYJXg0g0+3qdrMSC5AGaVWDpsHZZOuOnu0TABFFumK6LzbQd+MmJ/mhwzQmJ/lxO/oQg7/lU9iVsX3Q=='
#    container_name = 'asset-45df3b6c-3e01-454d-afb5-2ebfe851e5d3'
#    storage_container = BlobStorageContainer(account_name,account_key,container_name)
#    blobs = storage_container.get_blobs_list('jpg') 
#    for b in blobs:
#        print b
