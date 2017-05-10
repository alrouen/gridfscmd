import argparse
from gridfsOps import ls, get, put, rm

# Main parser
parser = argparse.ArgumentParser('gridsfscmd', add_help=False)
parser.add_argument('-h', help='mongodb host to connect to (host:port or host1:port1,host2:port2 for replica sets)', type=str, dest='host')
parser.add_argument('-d', help='database to use (default is \'test\')', type=str, dest='db')
parser.add_argument('-b', help='GridFS bucket to use (default is \'fs\')', type=str, dest='bucket')
parser.add_argument('-u', help='username for authentication', type=str, dest='user')
parser.add_argument('-p', help='password for authentication', type=str, dest='password')
parser.add_argument('--authDB', help='database that holds the user\'s credentials', type=str, dest='auth_db')
parser.add_argument('--ssl', help='use SSL', dest='ssl', action='store_true')
parser.add_argument('--no-ssl', help='do not use SSL', dest='ssl', action='store_false')
parser.add_argument('--help', action='help', help='show this help message and exit')

parser.set_defaults(ssl=False)
parser.set_defaults(host="localhost")
parser.set_defaults(db='test')
parser.set_defaults(bucket='fs')

subparsers = parser.add_subparsers(help='sub-command help')

# LS sub-command
parser_ls = subparsers.add_parser('ls', add_help=False)
parser_ls.add_argument('--help', action='help', help='show sub-command help message and exit')
parser_ls.add_argument('filename', help='filename, including path prefix, to search (regex)')
parser_ls.add_argument('-l', help='long format display', dest='long_format', action='store_true')
parser_ls.set_defaults(long_format=False)
parser_ls.set_defaults(func=ls.cmd)
#################

# GET sub-command
parser_get = subparsers.add_parser('get', add_help=False)
parser_get.add_argument('--help', action='help', help='show sub-command help message and exit')
parser_get.add_argument('filename', help='filename, including path prefix, to search (regex) and download')
parser_get.add_argument('destination', help='destination base folder')
parser_get.set_defaults(func=get.cmd)
#################

# PUT sub-command
parser_put = subparsers.add_parser('put', add_help=False)
parser_put.add_argument('--help', action='help', help='show sub-command help message and exit')
parser_put.add_argument('source', help='either one file, or one directory (recursive upload)')
parser_put.add_argument('--prefix', help='destination prefix (default is\'/\')', type=str, dest='prefix')
parser_put.set_defaults(prefix='')
parser_put.set_defaults(func=put.cmd)
#################

# RM (delete) sub-command
parser_rm = subparsers.add_parser('rm', add_help=False)
parser_rm.add_argument('--help', action='help', help='show sub-command help message and exit')
parser_rm.add_argument('filename', help='filename, including path prefix, to remove (regex)')
parser_rm.add_argument('-y', help='remove the files without prompting for confirmation', dest='confirmation', action='store_false')
parser_rm.set_defaults(confirmation=True)
parser_rm.set_defaults(func=rm.cmd)
#################

# Parse args and bootstrap sub-command
args = parser.parse_args()
args.func(args)


