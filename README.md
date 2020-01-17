# Usage
usage: disable_command.py [-h] [--enable= [TRUE/FALSE]]
                          [--disable= [[TRUE/FALSE]] [-u U] [-c C]

__This program allow you to enable or disable commands for specified users if the options below are used.__
__If the command is launched with no options the program will try to find the user's group and the existence of__
__the /tmp/command\_{groupname} (containing the list of denied commands) to block the usage of those commands.__

__Logs are written in /var/log/disable_commands.log__


optional arguments:

  -h, --help            show this help message and exit

  --enable=             Add TRUE or FALSE to the option

  --disable=            Add TRUE or FALSE to the option

  -u U, --user U        Define the user

  -c C, --command C     Define the command to enable

  --log                 Provide logging level. Example --log debug

                        Accepted Options:

                        debug --> For development environment

                        info --> Provide info, warnings and errors

                        warnings --> provide warnings and errors

                        errors --> provide only errors



__Note:__ If launched with no options, the script will disable the commands as described in the description


# Description
 Unable users to run specified commands. 

 The script it is supposed to be used when a LDAP connection exists and the home directory is created under /home.
 The get_users_gid function will create a list of user's home directory and then check for their group and pass the user and gropu to the commands_config function.
 

 commands_config expect that in the /tmp there are predifine files, containing the list of commands, for each user group for example: /tmp/commands_sysadmin where sysadmin is the groupname

 /tmp/commands_sysadmin content:

 yum

 reboot

 shutdown

 
 Once found them the script is going to create aliases in the user ".bashrc" file. At that point once the user will log in the system, he/she won't be able to run the commands.




# Syslog
 To enable the syslog, move the disable_commands.conf in /etc/rsyslog.d/ and restart the rsyslog service with the command "systemctl restart rsyslog" 
 File logs are written in the /var/log/disable_commands.log


 

