from fs import Fs
from hurry.filesize import size


def _long_display(files):
    print 'total ' + str(len(files))
    for f in files:
        print "{0}\t{1}\t{2}\t{3}".format(
            size(f.length),
            f.upload_date.strftime('%Y-%m-%d %H:%M.%S %z'),
            f.filename,
            f.md5
        )


def _display(files):
    for f in files:
        print f.filename


# LS
def cmd(args):
    _fs = Fs(args.host, args.db, args.user, args.password, args.bucket, args.ssl, args.auth_db)
    files = _fs.find(args.filename)

    if len(files) > 0:
        if args.long_format:
            _long_display(files)
        else:
            _display(files)
    else:
        print "no matching file found."

