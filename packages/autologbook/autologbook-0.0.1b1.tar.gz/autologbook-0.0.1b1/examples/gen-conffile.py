# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:04:20 2022

@author: elog-admin
"""

import configparser
from datetime import datetime


def write_conffile(config_object, filename):
    """
    Write a configuration objecto to a file.

    Parameters
    ----------
    config_object : ConfigParser
        The configuration dictionary to be dumped into a file.
    filename : str or path-like
        The output file name

    Returns
    -------
    None.

    """
    if not isinstance(config_object, configparser.ConfigParser):
        raise TypeError('Invalid configuration object')

    message = ('###  AUTOLOGBOOK CONFIGURATION FILE.\n'
               f'# Generated on {datetime.now():%Y-%m-%d %H:%M:%S}\n'
               f'# Autologbook version \n'
               '# \n'
               '## IMPORTANT NOTE ABOUT PASSWORDS:\n'
               '# \n'
               '# If you need to change the password in this configuration file, just\n'
               '# enter the plain text password in the password field and set use_encrypt_pwd to False.\n'
               '# The next time that autologook is executed the plain text password will be hashed \n'
               '# and this configuration file will be updated with the hashed value for your security.\n'
               '# \n\n')

    with open(filename, 'w') as configfile:
        configfile.write(message)
        config_object.write(configfile)


config = configparser.ConfigParser()
config['elog'] = {
    'elog_user': 'log-robot',
    'elog_password': 'IchBinRoboter',
    'elog_hostname': 'https://10.166.16.24',
    'elog_port': 8080,
    'elog_use_ssl': True
}

config['quattro'] = {
    'logbook': 'Quattro-Analysis'
}

config['yaml-editor'] = {
    'fav_editor_path': 'C:\\Program Files\\Notepad++\\notepad++.exe'
}

config['watchdog'] = {
    'mirroring_engine': 'robocopy',
    'shared_base_path': 'R:\\A226\\Results'

}
write_conffile(config, 'test.ini')
