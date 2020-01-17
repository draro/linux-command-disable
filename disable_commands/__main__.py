import logging
import logging.handlers
import os
import pdb
import sys
import fnmatch
from logging import config
import argparse
from disable_commands import *
parser = argparse.ArgumentParser(
    prog='disable_command.py',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
        This program allow you to enable or disable commands for specified users if the options below are used.
        If the command is launched with no options the program will try to find the user's group and the existence of
        the /tmp/command_{groupname} (containing the list of denied commands) to block the usage of those commands.
        
        Logs are written in /var/log/disable_commands.log  
        ''',
)
parser.add_argument('--enable=',  dest='e', nargs="*",
                    help='Add TRUE or FALSE to the option')
parser.add_argument('--disable=', dest='d', nargs="*",
                    help='Add TRUE or FALSE to the option')
parser.add_argument('-u', '--user', type=str,
                    dest='u', help="define the user")
parser.add_argument('-c', '--command', dest='c',
                    type=str, help="define the command to enable")


args = parser.parse_args()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s Module: %(module)s Process: %(process)d Message:%(message)s'
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': logging.DEBUG,
            'formatter': 'verbose',
        },
        'sys-logger6': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'facility': "local6",
            'level': logging.DEBUG,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'user-commands': {
            'handlers': ['stdout', 'sys-logger6'],
            'level': logging.INFO,
            'propagate': True,
        },
    }
}

config.dictConfig(LOGGING)
logger = logging.getLogger("user-commands")

if __name__ == "__main__":
    try:
        if os.geteuid() != 0:
            logger.critical("User Must be ROOT!")
            exit(1)
        if args.e and args.c and args.u and not args.d:
            enable_command(args.e, args.u, args.c)
        elif args.e and args.c and not args.u:
            logger.critical("the option -u shall be used")
        elif args.e and not args.c and args.u:
            logger.critical("the option -c shall be used")
        elif not args.e and not args.c and args.u:
            logger.critical("Missing arguments")
        elif not args.e and args.c and args.u and not args.d:
            logger.critical("Argument --enable required")
            print("Argument --enable required")
        elif not args.e and args.c and not args.u and not args.d:
            logger.critical("Missing arguments")
        elif args.d and args.c and args.u and not args.e:
            disable_command(args.d, args.u, args.c)
        elif args.d and args.c and not args.u and not args.e:
            logger.critical(
                "The option -u shall be used. To disable commands for all the user do not add any option")
        elif args.d and not args.c and args.u and not args.d:
            logger.critical(
                "The option -c shall be used. To disable commands for all the user do not add any option")
        elif not args.d and not args.c and args.u and not args.d:
            logger.critical(
                "Missing arguments. Run disable_commands.py -h for the help")
        elif not args.d and args.c and args.u and not args.d:
            logger.critical("Argument --enable or --disable required")
        elif not args.d and args.c and not args.u and not args.d:
            logger.critical(
                "Missing arguments. Run disable_commands.py -h for the help")
        else:
            get_users_gid()
    except Exception as e:
        logger.exception("Exception: {0}".format(e))
        exit(1)
