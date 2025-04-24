import requests
from constants import GET_S3_FERRY_PAYLOAD

class S3Ferry:
    def __init__(self, url):
        self.url = url

    def transfer_file(self, destinationFilePath, destinationStorageType, sourceFilePath, sourceStorageType):
        payload = GET_S3_FERRY_PAYLOAD(destinationFilePath, destinationStorageType, sourceFilePath, sourceStorageType)
        print("========================================================================")
        print("========================================================================")
        print("========================================================================")
        print("========================================================================")
        print("===================S3 FERRY============================================")
        print(destinationFilePath)
        print(destinationStorageType)
        print(sourceFilePath)
        print(sourceStorageType)
        print("========================================================================")
        print("========================================================================")
        print("========================================================================")
        print("========================================================================")
        print("========================================================================")

        response = requests.post(self.url, json=payload)
        return response
