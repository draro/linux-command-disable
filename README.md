# Usage
usage: disable_command.py [-h] [--enable= [TRUE/FALSE]]
                          [--disable= [[TRUE/FALSE]] [-u U] [-c C] [--log LOG]


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

  --log                 Provide logging level. Example --log debug.

                        Accepted Options:   
                        debug --> For development environment  
                        info --> Provide info, warnings and errors  
                        warnings --> provide warnings and errors  
                        errors --> provide only errors



#### __Note:__ If launched with no options, the script will disable the commands as described in the description


# Description
 Unable users to run specified commands. 

 The script it is supposed to be used when a LDAP connection exists and the home directory is created under /home.
##  get_users_gid()
 get_user_gid will list users home expecting that the username and its own home deirectory have the same name.
 
 Example:  for user test, the get_users_gid expects to find a /home/test directory.
 
 Once found it uses the "id" command to search the appartenency to groups and then call the commands_config function passing the user and group arguments.
 

## commands_config(user, group)
 User and Group are passed automatically from the get_users_gid funcion
 
 It search for the denied command list per user goup.
 
 The command's list file shall be located in /tmp and the filename shall be commands_{groupname}.
 
 After found the file the program will write a bashrc.done_{group} and use that file to aplly the rules in the user .bashrc file
 
 __commands_config()__ expect that in the /tmp there are predifine files, containing the list of commands, for each user group for example: /tmp/commands_sysadmin where sysadmin is the groupname.

 __/tmp/commands_sysadmin content:__

 yum

 reboot

 shutdown

 
 Once found them the script is going to create aliases in the user ".bashrc" file. At that point once the user will log in the system, he/she won't be able to run the commands.


## enable_command(enable, u, c) 
  The function get the arguments from the argparse and remove lines in the .bashrc file.

  It is also expected that username and home directory folder, matches.

## disable_command(disable, u, c)
 disable_command(disable, u, c) get the arguments from the argparse and add a line in the .bashrc file.
 
 It is also expected that username and home directory folder, matches.

# Syslog
 To enable the syslog, move the disable_commands.conf in /etc/rsyslog.d/ and restart the rsyslog service with the command "systemctl restart rsyslog" 
 File logs are written in the /var/log/disable_commands.log


 

