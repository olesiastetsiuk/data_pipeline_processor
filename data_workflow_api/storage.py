import json
import os

from configs.aws import UPLOAD_PATH, DOWNLOAD_PATH
from tasks import put_data_to_s3, get_data_from_s3


class DataStorage():

    def on_get(self, req, resp):
        """Storage's GET handler
        
                Awaits parameter 'file_key' in the request body.
                Runs celery task for getting file_name by file_key,
                downloads file from AWS S3 storage and returns response as
                file-like object.
        
        """

    def on_put(self, req, resp):
        """Storage's PUT handler
        
            Note:
                Awaits parameter 'file' as 'multipart/form-data' in the 
                request body.
                Runs celery task for getting file_key from md5 hash of file,
                uploads file to AWS S3 storage and returns in response file_key.
        
        """