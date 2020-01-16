import logging
import logging.handlers
import os
import pdb
import sys
import fnmatch
from logging import config
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--enable', action='store_true',
                    dest='e', help="Enable command")
parser.add_argument('-u', '--userr', type=str,
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
                logger.error('i am line 177')
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


def enamble_command(u, c):
    logger.info('ENABLE COMMAND FUNCTION')
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


if __name__ == "__main__":
    try:
        if os.geteuid() != 0:
            logger.critical("User Must be ROOT!")
            exit(1)
        if args.e and args.c and args.u:
            enamble_command(args.u, args.c)
        elif args.e and args.c and not args.u:
            logger.critical("the option -u shall be used")
        elif args.e and not args.c and args.u:
            logger.critical("the option -c shall be used")
        elif not args.e and not args.c and args.u:
            logger.critical("Missing arguments")
        elif not args.e and args.c and args.u:
            logger.critical("Argument --enable required")
            print("Argument --enable required")
        elif not args.e and args.c and not args.u:
            logger.critical("Missing arguments")
        else:
            get_users_gid()
    except Exception as e:
        logger.exception("Exception: {0}".format(e))
        exit(1)
