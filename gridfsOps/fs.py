from pymongo import MongoClient
import gridfs
import re
from urllib import urlencode

# pattern to match a list of server,server:port, ...
# ie: server1,server2.domain.net:1233,192.168.1.23:27017
host_pattern = re.compile('^([a-zA-Z0-9_\-\.]+){1}(:\d+)?(,([a-zA-Z0-9_\-\.]+){1}(:\d+)?)*$')


class Fs(object):

    def __init__(self, host, db, user, password, bucket_name, ssl):

        host_ok = Fs.__check_hostname(host)
        if host_ok is None:
            raise ValueError('hostname syntax is invalid. Must be host:port or host1:port1,host2:port2 for replica sets')
        else:
            options = None
            if ssl:
                options = { 'ssl' : 'true', 'ssl_cert_reqs' : "CERT_NONE"}
            self.mongo_uri = Fs.build_uri(host, db, user, password, options)
            self.bucket_name = bucket_name
            client = MongoClient(self.mongo_uri)
            db = client[db]
            self.fs = gridfs.GridFSBucket(db, bucket_name=self.bucket_name)

    @staticmethod
    def __build_credentials(user, password):
        if user is not None and password is not None:
            return "{0}:{1}@".format(user, password)
        else:
            return ''

    @staticmethod
    def __check_hostname(host):
        return host_pattern.match(host)

    @staticmethod
    def build_uri(host, db, user, password, options=None):
        # -----------------
        # Mongo URI syntax:
        # mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
        # -----------------
        uri = "mongodb://{0}{1}/{2}".format(
                Fs.__build_credentials(user, password),
                host,
                db
            )

        if options is None:
            return uri
        else:
            encoded_options = urlencode(options.items())
            return "{0}?{1}".format(uri, encoded_options)

    def find(self, pattern):
        files = list(
            map(
                lambda f: f, self.fs.find({'filename': {'$regex': pattern}})
            )
        )
        return files

    def download(self, source, destination):
        self.fs.download_to_stream_by_name(source, destination)

    def upload(self, source, destination):
        return self.fs.upload_from_stream(destination, source)

    def rm(self, id):
        return self.fs.delete(id)

