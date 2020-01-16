# Usage
usage: disable_commands.py [-h] [--enable] [-u U] [-c C]

optional arguments:

  -h, --help         show this help message and exit

  --enable           Enable command

  -u U, --user U     define the user

  -c C, --command C  define the command to enable



__Note:__ If launched with no options, the script will disable the commands as described in the description


# Description
 Unable users to run specified commands. 

 The script it is supposed to be used when a LDAP connection exists and the home directory is created under /home.
 The get_users_gid function will create a list of user's home directory and then check for their group and pass the user and gropu to the commands_config function.
 

 commands_config expect that in the /tmp there are predifine files for each user group for example: /tmp/commands_sysadmin where sysadmin is the groupname



# Syslog
 To enable the syslog, move the disable_commands.conf in /etc/rsyslog.d/ and restart the rsyslog service with the command "systemctl restart rsyslog" 
 File logs are written in the /var/log/disable_commands.log


 

