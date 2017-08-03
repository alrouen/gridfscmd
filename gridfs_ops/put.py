import sys
from os import walk
from os.path import isfile, dirname, basename, exists
from fs import Fs
from spinner import Spinner


def _build_local_file_list(source):
    """List from source the local files to upload, and return a tuple-2 the local root folder and a list of files to upload.

    Keyword arguments:
    source -- local path to a file or folder
    """
    if isfile(source):
        return dirname(source), ['/'+basename(source)]
    else:
        f = []
        root = dirname(source)
        for (current_folder, sub_folders, sub_files) in walk(root):
            if len(sub_files) > 0:
                remote_path = current_folder.replace(root,'').replace('\\', '')  # We remove any '\' (Windows env)
                f.extend(list(map(lambda sub_file: remote_path+'/'+sub_file, sub_files)))
        return root, f


# PUT
def cmd(args):
    _fs = Fs(args.host, args.db, args.user, args.password, args.bucket, args.ssl, args.auth_db)

    if exists(args.source):

        local_folder, local_files = _build_local_file_list(args.source)

        if len(local_files) > 0:

            # build remote gridFs prefix (prepend a '/' if required)
            remote_prefix = ''
            if len(args.prefix) > 0:
                remote_prefix = "/{0}".format(args.prefix) if not args.prefix.startswith('/') else args.prefix

            for local_file in local_files:
                local = local_folder + local_file
                remote = remote_prefix + local_file
                src_file = open(local, 'r')

                spinner = Spinner()
                sys.stdout.write(remote+': ')
                spinner.start()

                f_id = _fs.upload(src_file, remote)

                spinner.stop()
                sys.stdout.write(str(f_id)+'\n')
        else:
            print "No files to upload."

    else:
        print 'local file/folder [{0}] does not exists'.format(args.source)