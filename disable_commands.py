import logging
import logging.handlers
import os
import pdb
import sys
import fnmatch
from logging import config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s Module: %(module)s Process: %(process)d Thread: %(thread)d Message:%(message)s'
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
            'level': logging.INFO,
            'formatter': 'verbose',
            },
        },
    'loggers': {
        'user-commands': {
            'handlers': ['stdout','sys-logger6'],
            'propagate': True,
            },
        }
    }

config.dictConfig(LOGGING)


logger = logging.getLogger("user-commands")


groups = ['svn', 'wheel', 'admin', 'sys_admin','network_admin', 'security_admin', 'test2', r'test$']


def commands_config(user, group):
    '''
    commands_config(user, group)
    User and Group are passed automatically from the get_users_gid funcion
    It search for the denied command list per user goup.
    The command's list file shall be located in /tmp and the filename shall be commands_{groupname}.
    After found the file the program will write a bashrc.done_{group} and use that file to aplly the 
    rules in the user .bashrc file
    '''
    logger.debug('{0},{1}'.format(user,group))
    global groups
    if group in groups:
        logger.debug('{0},{1}'.format(group, groups))
        commands = '/tmp/commands_'+group
        logger.debug(commands)
        back_bashrc = '/home/{0}/.bashrc.original'.format(user)
        if os.path.isfile('/home/{0}/.bashrc.original'.format(user)):
            logger.debug('/home/{0}/.bashrc.original Exists'.format(user))
        else:
            os.system('cp /home/{0}/.bashrc /home/{0}/.bashrc.original'.format(user))
            logger.debug('/home/{0}/.bashrc.original Created')
        try:
            if os.path.getsize(commands) > 0:
                try:
                    if os.path.getsize(back_bashrc) > 0:
                        with open(commands, mode='r+') as file:
                            rows = file.read().splitlines()
                            file.seek(0)
                            bashrc = '/home/{0}/.bashrc.done_{1}'.format(user, group)
                            bashrc_orig = '/home/{0}/.bashrc'.format(user)
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
                                                    logger.debug('Row containing {0} already exist'.format(row))

                                                else:
                                                    logger.debug('Row with {0} missing'.format(row))
                                                    with open(bashrc_orig, mode='a')as original:
                                                        original.write(
                                                            'alias '+row+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                    with open(commands, mode='r') as c:
                                        file = c.read().splitlines()
                                        c.seek(0)
                                        for line in file:
                                            with open(bashrc, mode='r+') as done:
                                                rows = done.read()
                                                if line in rows:
                                                    logger.debug('Row containing {0} already exist'.format(line))
                                                else:
                                                    logger.debug('Row with {0} missing'.format(line))
                                                    done.write('alias '+line+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                                    with open(bashrc_orig, mode='a')as file:
                                                        file.write(
                                                            'alias '+line+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                else:
                                    for row in rows:
                                        with open(bashrc, mode='a')as file:
                                            file.write(
                                                'alias '+row+'='+'"echo ' + "'You are not allowed to run this command'"+'"'+'\n')
                                    os.system(
                                        'cat {0} >>/home/{1}/.bashrc '.format(bashrc, user))

                            except Exception as e:
                                logger.exception('An Error Occurred: {0}'.format(e))
                    else:
                        logger.warning('File {0} not found'.format(back_bashrc))
                except OSError as e:
                    logger.error('(!) Unable to get file size: {}'.format(e))
            else:
                try:
                    if os.path.getsize(commands) > 0 and os.path.isfile(back_bashrc):
                        os.system('cp {0} /home/{1}/.bashrc'.format(back_bashrc,user))
                        logger.debug('Apllying the original bashrc')
                except OSError as e:
                    logger.info('(!) Unable to get file size: {}'.format(e))
                logger.warning('File {0} not found'.format(commands))
                logger.warning("User {0} does not have command's limitation".format(user))
        except OSError as e:
            logger.info('(!) Unable to get file size: {}'.format(e))
        except Exception as e:
            logger.exception('An Error Occurred: {0}'.format(e))


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
                        logger.debug('Found group: ' + group + ' for user: ' + user)
                        commands_config(user, group)

if __name__ == "__main__":
    try:
        get_users_gid()
    except Exception:
        logger.exception("Exception in get_users_gid(): ")
        exit(1)
