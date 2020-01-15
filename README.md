# linux-command-disable
 Unable users to run specified commands

 The script it is supposed to be used when a LDAP connection exists and the home directory is created under /home.
 The get_users_gid function will create a list of user's home directory and then check for their group and pass the user and gropu to the commands_config function.

 commands_config expect that in the /tmp there are predivine files for each user group