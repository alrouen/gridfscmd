import sys
from fs import Fs
from spinner import Spinner

yes = set(['yes','y', 'ye', ''])
no = set(['no','n'])


def _confirm_removal(message='Do you confirm ? (y/n) '):
    sys.stdout.write(message)
    while True:
        choice = raw_input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")


# RM
def cmd(args):
    _fs = Fs(args.host, args.db, args.user, args.password, args.bucket, args.ssl, args.auth_db)
    confirmation = args.confirmation
    files = _fs.find(args.filename)

    if len(files) > 0:
        print "Found {0} files to remove".format(len(files))
        confirmed = _confirm_removal() if confirmation else False
        if not confirmation or confirmed:
            for f in files:
                spinner = Spinner()
                print f.filename
                spinner.start()
                _fs.rm(f._id)
                spinner.stop()
    else:
        print "no matching file found."
