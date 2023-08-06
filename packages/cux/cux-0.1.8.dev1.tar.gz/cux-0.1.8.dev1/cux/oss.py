#!/usr/bin/env python
import re
from dataclasses import asdict, astuple, dataclass
from typing import List, Tuple

import codefast as cf
import oss2


@dataclass
class AppInfo:
    id: str = "TFRBSTRHS3JWRlJtNnBhdXRrYUdGdnpE"
    secret: str = "VGxXWFlPSzY0aUR3TktXSXJBWjJUTjQ4b1RhRGtv"
    appkey: str = "d1QxVm9KNFp0c09kbVN4aQ=="
    region: str = "https://oss-cn-zhangjiakou.aliyuncs.com"


class AliyunOSS:
    def __init__(self, appinfo=AppInfo(), bucket_name: str = "megaview"):
        self.appinfo = appinfo
        _id, _secret = list(
            map(cf.b64decode, (self.appinfo.id, self.appinfo.secret)))
        self.oss_auth = oss2.Auth(_id, _secret)
        self.server = oss2.Service(self.oss_auth, self.appinfo.region)
        self.bucket = oss2.Bucket(
            self.oss_auth, self.appinfo.region, bucket_name)

    def upload(self, local_file_name: str, remote_dir: str) -> str:
        '''upload a file to backend/, set expire duration to 1 hour'''
        basename = cf.io.basename(local_file_name)
        remote_object_name = "{}/{}".format(remote_dir, basename)
        self.bucket.put_object_from_file(remote_object_name, local_file_name)
        audio_url = self.bucket.sign_url('GET',
                                         remote_object_name,
                                         36000,
                                         slash_safe=True)
        return audio_url

    def sign(self, remote_path:str)->str:
        """Get public accessable url"""
        return self.bucket.sign_url('GET', remote_path, 36000, slash_safe=True)

    def get_metadata(self, object_name: str) -> oss2.models.GetObjectAclResult:
        '''Get metadata of a file'''
        return self.bucket.get_object_meta(object_name)

    def download(self, url: str, target_dir: str = "/tmp") -> oss2.models.GetObjectAclResult:
        '''Download file from an url '''
        _, directory, filename = AliyunOSS.parse_url(url)
        local_path = "{}/{}".format(target_dir, filename)
        if cf.io.exists(local_path):
            cf.info("{} already exists, skip".format(local_path))
            return

        object_full_path = "{}/{}".format(directory, filename)
        local_path = "{}/{}".format(target_dir, filename)

        cf.info("Downloading file '{}' to '{}'".format(object_full_path,
                                                       local_path))
        try:
            result = self.bucket.get_object_to_file(
                object_full_path, local_path)
            assert result.status == 200, "Status of bucket.get_object_to_file is not 200"
            return result
        except Exception as e:
            cf.error("Failed to download file '{}' to '{}'".format(
                object_full_path, local_path))
            return

    @staticmethod
    def parse_url(url: str) -> Tuple[str, str, str]:
        '''return (Bucket, directory, file) names '''
        bucket_name = re.search(r'.*//(.*?)\.', url).group(1)
        directory = re.search(r'com\/(.*?)/', url).group(1)
        filename = url.split('/')[-1]
        return bucket_name, directory, filename


if __name__ == '__main__':
    url = 'https://megaview.oss-cn-zhangjiakou.aliyuncs.com/transcription/19_7ad31ebb34294e845940db7144241b30.txt'
    url = "https://megaview.oss-cn-zhangjiakou.aliyuncs.com/audios/19_7ad31ebb34294e845940db7144241b30.wav"
    print(AliyunOSS.parse_url(url))
    print(AliyunOSS().download(url))
    print(AliyunOSS().upload("/tmp/c.wav"))
