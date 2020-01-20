import logging
import logging.handlers
import os
import pdb
import sys
import fnmatch
from logging import config
import argparse


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
parser.add_argument(
    "--log", help='''Provide logging level. Example --log debug''')


args = parser.parse_args()

level_config = {'debug': logging.DEBUG, 'info': logging.INFO,
                'warning': logging.WARNING, 'creitical': logging.CRITICAL, 'error': logging.ERROR, 'exception': logging.ERROR}
if args.log:
    log_level = level_config[args.log.lower()]
else:
    log_level = level_config['info']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s Module: %(module)s Process: %(process)d Message: %(message)s'
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'level': log_level,
            'formatter': 'verbose',
        },
        'sys-logger6': {
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'facility': "local6",
            'level': log_level,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'user-commands': {
            'handlers': ['stdout', 'sys-logger6'],
            'level': log_level,
            'propagate': True,
        },
    }
}

config.dictConfig(LOGGING)
logger = logging.getLogger("user-commands")
# GROUPS TO BE CHANGED DEPENDING ON THE EXPECTED GROUP ON LDAP
groups = ['svn', 'wheel', 'admin', 'sys_admin', 'test2',
          'network_admin', 'security_admin']


def commands_config(user, group):
    '''
    commands_config(user, group)
    User and Group are passed automatically from the get_users_gid funcion
    It search for the denied command list per user goup.
    The command's list file shall be located in /tmp and the filename shall be commands_{groupname}.
    After found the file the program will write a bashrc.done_{group} and use that file to aplly the
    rules in the user .bashrc file
    '''
    logger.debug('{0},{1}'.format(user, group))
    global groups
    if group in groups:
        logger.debug('{0},{1}'.format(group, groups))
        commands = '/tmp/commands_'+group
        logger.debug(commands)
        back_bashrc = '/home/{0}/.bashrc.original'.format(user)
        bashrc = '/home/{0}/.bashrc.done_{1}'.format(user, group)
        bashrc_orig = '/home/{0}/.bashrc'.format(user)
        # CREATE BASHRC BACKUP IF NOT EXISTS
        if os.path.isfile('/home/{0}/.bashrc.original'.format(user)):
            logger.debug('/home/{0}/.bashrc.original Exists'.format(user))
        else:
            os.system(
                'cp /home/{0}/.bashrc /home/{0}/.bashrc.original'.format(user))
            logger.debug('/home/{0}/.bashrc.original Created')
        try:
            # CHECK that /tmp/commands_{group} is not empty
            if os.path.getsize(commands) > 0:
                try:
                    # check bashrc.original is not empty
                    if os.path.getsize(back_bashrc) > 0:
                        with open(commands, mode='r+') as file:
                            rows = file.read().splitlines()
                            file.seek(0)
                            try:
                                if os.path.isfile(bashrc):
                                    logger.debug('{0} Exists'.format(bashrc))
                                    with open(bashrc, mode='r+') as done:
                                        rows = done.read().splitlines()
                                        done.seek(0)
                                        for row in rows:
                                            with open(bashrc_orig, mode='r') as orig:
                                                file = orig.read()
                                                if row in str(file):
                                                    logger.debug(
                                                        'Row containing {0} already exist'.format(row))

                                                else:
                                                    logger.debug(
                                                        'Row with {0} missing'.format(row))
                                                    logger.debug(
                                                        'opening the bashrc file')
                                                    with open(bashrc_orig, mode='a')as original:
                                                        logger.debug(
                                                            'inside the bashrc.done')
                                                        logger.debug(
                                                            'WRITING: ' + row)
                                                        original.write(
                                                            row+'\n')

                                    with open(commands, mode='r') as c:
                                        file = c.read().splitlines()
                                        c.seek(0)
                                        for line in file:
                                            with open(bashrc, mode='r+') as done:
                                                rows = done.read()
                                                if line in rows:
                                                    logger.debug(
                                                        'Row containing {0} already exist'.format(line))
                                                else:
                                                    logger.debug(
                                                        'Row with {0} missing'.format(line))
                                                    done.write(
                                                        'alias '+line+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                                    with open(bashrc_orig, mode='a')as file:
                                                        file.write(
                                                            'alias '+line+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                else:
                                    for row in rows:
                                        with open(bashrc, mode='a')as file:
                                            file.write(
                                                'alias '+row+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                    with open(bashrc, mode='r+') as done:
                                        rows = done.read().splitlines()
                                        done.seek(0)
                                        for row in rows:
                                            with open(bashrc_orig, mode='r') as orig:
                                                file = orig.read()
                                                if row in str(file):
                                                    logger.debug(
                                                        'Row containing {0} already exist'.format(row))

                                                else:
                                                    logger.debug(
                                                        'Row with {0} missing'.format(row))
                                                    logger.debug(
                                                        'opening the bashrc file')
                                                    with open(bashrc_orig, mode='a')as original:
                                                        logger.debug(
                                                            'inside the bashrc.done')
                                                        logger.debug(
                                                            'WRITING: ' + row)
                                                        original.write(
                                                            row+'\n')

                                    with open(commands, mode='r') as c:
                                        file = c.read().splitlines()
                                        c.seek(0)
                                        for line in file:
                                            with open(bashrc, mode='r+') as done:
                                                rows = done.read()
                                                if line in rows:
                                                    logger.debug(
                                                        'Row containing {0} already exist'.format(line))
                                                else:
                                                    logger.debug(
                                                        'Row with {0} missing'.format(line))
                                                    done.write(
                                                        'alias '+line+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                                    with open(bashrc_orig, mode='a')as file:
                                                        file.write(
                                                            'alias '+line+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')

                            except Exception as e:
                                logger.exception(
                                    'An Error Occurred: {0}'.format(e))
                    else:
                        logger.warning(
                            'File {0} not found'.format(back_bashrc))
                except OSError as e:
                    logger.error('(!) Unable to get file size: {}'.format(e))
                # for fileList in os.listdir('/home/{0}/'.format(user)):
                #     if fileList.startswith('.bashrc.done'):
                #         logger.error('{0}'.format(fileList))

            else:
                try:
                    os.remove(bashrc)
                    logger.critical('removed bashrc.done')
                    if os.path.getsize(commands) == 0 & os.path.isfile(back_bashrc):
                        file = []
                        for files in os.listdir('/home/{0}'.format(user)):
                            if files.startswith('.baschrc.done_'):
                                file.append(files)
                        if len(file) == 1:
                            os.system(
                                'cp {0} /home/{1}/.bashrc'.format(back_bashrc, user))
                            logger.info('Apllying the original bashrc')
                    else:
                        logger.warning('File {0} not found'.format(commands))
                        logger.warning(
                            "User {0} does not have command's limitation".format(user))

                except OSError as e:
                    logger.info('(!) Unable to get file size: {0}'.format(e))

        except OSError as e:
            logger.info('(!) Unable to get file size: {}'.format(e))
        except Exception as e:
            logger.exception('An Error Occurred: {0}'.format(e))
    else:
        logger.info('{0} not in the coded groups'.format(user))


def get_users_gid():
    '''
    get_user_gid will list users home expecting that the username and its own home deirectory have the same name.
    Example:  for user test, the get_users_gid expects to find a /home/test directory.
    Once found it uses the "id" command to search the appartenency to groups and then call the 
    commands_config function passing the user and group arguments.
    '''
    tmp_file = '/tmp/tmp.txt'
    tmp_file2 = '/tmp/tmp_file'
    users_list = os.system("ls /home >{0}".format(tmp_file))
    with open(tmp_file, mode='r') as file:
        user_list = file.read().splitlines()
        for user in user_list:
            command = "id {0}>{1}".format(user, tmp_file2)
            uid = os.system(command)
            with open(tmp_file2, mode='r') as file:
                f = file.read()
                for group in groups:
                    if group in f:
                        logger.debug('Found group: ' + group +
                                     ' for user: ' + user)
                        commands_config(user, group)


def enable_command(enable, u, c):
    '''
    enable_command(enable, u, c) get the arguments from the argparse and remove lines in the .bashrc file.
    It is also expected that username and home directory folder, matches.
    '''
    logger.debug('ENABLE COMMAND FUNCTION')
    command = c
    user = u
    logger.info('Enabling the command "{0}" for {1}'.format(command, user))
    for dirName, subDir, fileNames in os.walk('/home/{0}'.format(user)):
        for f in fileNames:
            if f.startswith('.bashrc'):
                with open("/home/{0}/{1}".format(user, f), "r+") as file:
                    logger.debug('opening /home/{0}/{1}'.format(user, f))
                    d = file.readlines()
                    file.seek(0)
                    for i in d:
                        if not command in i:
                            logger.debug('{0} not in {1}'.format(command, i))
                            file.write(i)
                        else:
                            logger.debug('{0} in {1}'.format(command, i))
                    file.truncate()


def disable_command(disable, u, c):
    '''
    disable_command(disable, u, c) get the arguments from the argparse and add a line in the .bashrc file.
    It is also expected that username and home directory folder, matches.
    '''
    logger.debug('Disable COMMAND FUNCTION')
    command = c
    user = u
    logger.info('Disabling the command "{0}" for {1}'.format(command, user))
    logger.debug('searcing for bashrc in /home/{0}'.format(user))
    for dirName, subDir, fileNames in os.walk('/home/{0}'.format(user)):
        for f in fileNames:
            if f.startswith('.bashrc') and not f.endswith('.original'):
                logger.info('{0}'.format(f))
                with open("/home/{0}/{1}".format(user, f), "r") as file:
                    logger.debug('opening /home/{0}/{1}'.format(user, f))
                    d = file.read()
                    # for i in d:
                    if not command in d:
                        logger.debug('{0} not in {1}'.format(command, d))
                        with open("/home/{0}/{1}".format(user, f), "a") as file:
                            file.write('alias '+command+'='+'"echo ' +
                                       "'You are not allowed to run this command'"+'"'+'\n')
                        # file.write(i)
                    else:
                        logger.debug('{0} in {1}'.format(command, d))


if __name__ == "__main__":
    try:
        logger.debug('Check if UID = 0')
        if os.geteuid() != 0:
            logger.debug(
                'User is not Root. Current UID = {0}'.format(os.geteuid()))
            logger.critical("User Must be ROOT!")
            exit(1)
        if args.e and args.c and args.u and not args.d:
            enable_command(args.e, args.u, args.c)
        elif args.e and args.c and not args.u and not args.d:
            logger.critical("the option -u shall be used")
        elif args.e and not args.c and args.u and not args.d:
            logger.critical("the option -c shall be used")
        elif not args.e and not args.c and args.u and not args.d:
            logger.critical("Missing arguments")
        elif not args.e and args.c and args.u and not args.d:
            logger.critical(
                "Argument --enable or --disable required. Use the --help or -h to see the help")
        elif not args.e and args.c and not args.u and not args.d:
            logger.critical(
                "Missing arguments. Run disable_commands.py -h for the help")
        elif args.d and args.c and args.u and not args.e:
            disable_command(args.d, args.u, args.c)
        elif args.d and args.c and not args.u and not args.e:
            logger.critical(
                "The option -u shall be used. To disable commands for all users do not add any option")
        elif args.d and not args.c and args.u and not args.d:
            logger.critical(
                "The option -c shall be used. To disable commands for all user do not add any option")
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
        logger.critical("Exception: {0}".format(e))
        exit(1)
