from os import makedirs
from os.path import exists, dirname
from fs import Fs
from spinner import Spinner


# GET
def cmd(args):
    _fs = Fs(args.host, args.db, args.user, args.password, args.bucket, args.ssl)
    gridfs_files = _fs.find(args.filename)
    nb_of_files = len(gridfs_files)
    if nb_of_files > 0:
        print 'downloading '+str(nb_of_files)+' files:'
        for gridfs_file in gridfs_files:
            gridfs_filename = gridfs_file.filename
            destination = args.destination + gridfs_filename

            # check for any non-existing parent directories for local destination, and create them
            destination_root = dirname(destination)
            if not exists(destination_root):
                makedirs(destination_root)

            spinner = Spinner()
            spinner.start()
            dst_file = open(destination, 'wb')
            _fs.download(gridfs_filename, dst_file)
            spinner.stop()
            print destination
    else:
        print "no matching file found."
