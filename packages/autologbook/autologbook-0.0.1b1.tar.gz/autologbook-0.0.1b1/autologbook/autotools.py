# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:06:58 2022

@author: elog-admin
"""

import configparser
import logging
import shutil
from datetime import datetime
from pathlib import Path

import elog
import yaml
from PIL.TiffImagePlugin import ImageFileDirectory_v2
from PyQt5 import QtCore

from autologbook import autoconfig, autoerror

log = logging.getLogger('__main__')


def init(config):
    """
    Itialize module wide global variables.

    Parameters
    ----------
    config : configparser object or string corresponding to a configuratio file
        The configuration object

    Returns
    -------
    None.

    """
    _config = configparser.ConfigParser()
    if isinstance(config, configparser.ConfigParser):
        _config = config
    elif isinstance(config, str):
        if Path(config).exists() and Path(config).is_file():
            _config.read(config)
        else:
            raise ValueError('Unable to initialize the autowatch-gui module because '
                             + 'the provided configuration file (%s) doesn\'t exist' %
                             (config))
    elif isinstance(config, Path):
        if config.exists() and config.is_file():
            _config.read(str(config))
        else:
            raise ValueError(
                'Unable to initialize the autowatch-gui module because the provided '
                + 'configuration file (%s) doesn\'t exist' % config)
    else:
        raise TypeError(
            'Unable to initialize the autowatch-gui module because of wrong config file')

    # ELOG section
    autoconfig.ELOG_USER = _config.get(
        'elog', 'elog_user', fallback=autoconfig.ELOG_USER)
    autoconfig.ELOG_PASSWORD = _config.get(
        'elog', 'elog_password', fallback=autoconfig.ELOG_PASSWORD)
    autoconfig.ELOG_HOSTNAME = _config.get(
        'elog', 'elog_hostname', fallback=autoconfig.ELOG_HOSTNAME)
    autoconfig.ELOG_PORT = _config.getint(
        'elog', 'elog_port', fallback=autoconfig.ELOG_PORT)
    autoconfig.USE_SSL = _config.getboolean(
        'elog', 'use_ssl', fallback=autoconfig.USE_SSL)
    autoconfig.MAX_AUTH_ERROR = _config.getint(
        'elog', 'max_auth_error', fallback=autoconfig.MAX_AUTH_ERROR)

    # EXTERNAL TOOLS section
    autoconfig.NOTEPAD_BEST = Path(_config.get(
        'external tools', 'favourite text editor', fallback=autoconfig.NOTEPAD_BEST))
    autoconfig.ROBOCOPY_EXE = Path(_config.get(
        'external tools', 'robocopy', fallback=autoconfig.ROBOCOPY_EXE))

    # AUTOLOGBOOK WATCHDOG
    autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS = _config.getint('Autologbook watchdog', 'max_attempts',
                                                                  fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS)
    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN = _config.getfloat('Autologbook watchdog', 'wait_min',
                                                                fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN)
    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX = _config.getfloat('Autologbook watchdog', 'wait_max',
                                                                fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX)
    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT = _config.getfloat('Autologbook watchdog', 'wait_increment',
                                                                      fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT)
    autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY = _config.getfloat('Autologbook watchdog', 'minimum delay between ELOG post',
                                                                 fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY)
    autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT = _config.getfloat('Autologbook watchdog', 'observer_timeout',
                                                               fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT)

    # MIRRORING WATCHDOG
    autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS = _config.getint('Mirroring watchdog', 'max_attempts',
                                                                   fallback=autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS)
    autoconfig.AUTOLOGBOOK_MIRRORING_WAIT = _config.getfloat(
        'Mirroring watchdog', 'wait', fallback=autoconfig.AUTOLOGBOOK_MIRRORING_WAIT)
    autoconfig.AUTOLOGBOOK_MIRRORING_TIMEOUT = _config.getfloat('Mirroring watchdog', 'observer_timeout',
                                                                fallback=autoconfig.AUTOLOGBOOK_MIRRORING_TIMEOUT)

    # IMAGE SERVER
    autoconfig.IMAGE_SERVER_BASE_PATH = _config.get(
        'Image_server', 'base_path', fallback=autoconfig.IMAGE_SERVER_BASE_PATH)
    autoconfig.IMAGE_SERVER_ROOT_URL = _config.get(
        'Image_server', 'server_root', fallback=autoconfig.IMAGE_SERVER_ROOT_URL)
    autoconfig.IMAGE_SAMPLE_THUMB_MAX_WIDTH = _config.getint(
        'Image_server', 'image_thumb_width', fallback=autoconfig.IMAGE_SAMPLE_THUMB_MAX_WIDTH)
    autoconfig.CUSTOMID_START = _config.getint(
        'Image_server', 'custom_id_start', fallback=autoconfig.CUSTOMID_START)
    autoconfig.CUSTOMID_TIFFCODE = _config.getint(
        'Image_server', 'tiff_tag_code', fallback=autoconfig.CUSTOMID_TIFFCODE)


    # FEI
    autoconfig.FEI_AUTO_CALIBRATION = _config.getboolean(
        'FEI', 'auto_calibration', fallback=autoconfig.FEI_AUTO_CALIBRATION)
    autoconfig.FEI_DATABAR_REMOVAL = _config.getboolean(
        'FEI', 'databar_removal', fallback=autoconfig.FEI_DATABAR_REMOVAL)


    # Quattro Specific
    autoconfig.IMAGE_NAVIGATION_MAX_WIDTH = _config.getint(
        'Quattro', 'image_navcam_width', fallback=autoconfig.IMAGE_NAVIGATION_MAX_WIDTH)
    autoconfig.QUATTRO_LOGBOOK = _config.get(
        'Quattro', 'logbook', fallback=autoconfig.QUATTRO_LOGBOOK)

    # Versa Specific
    autoconfig.VERSA_LOGBOOK = _config.get(
        'Versa', 'logbook', fallback=autoconfig.VERSA_LOGBOOK)


def generate_default_conf():
    """
    Generate a default configuration object.

    Parameters
    ----------
    filename : string or path-like, optional
        The name of the configuration file.
        The default is 'autolog-conf.ini'.

    Returns
    -------
    None.

    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section('elog')
    config['elog'] = {
        'elog_user': 'log-robot',
        'elog_password': encrypt_pass('IchBinRoboter'),
        'elog_hostname': 'https://10.166.16.24',
        'elog_port': '8080',
        'use_ssl': True,
        'use_encrypt_pwd': True,
        'max_auth_error': 5
    }
    config['external tools'] = {
        'favourite text editor': 'C:\\Program Files\\Notepad++\\notepad++.exe',
        'robocopy': shutil.which('robocopy.exe')
    }
    config['Quattro'] = {
        'logbook': 'Quattro-Analysis',
        'image_navcam_width': '500'
    }
    config['Versa'] = {
        'logbook': 'Versa-Analysis'
    }
    config['Mirroring engine'] = {
        'engine': 'watchdog'
    }
    config['Autologbook watchdog'] = {
        'max_attempts': '5',
        'wait_min': '1',
        'wait_max': '5',
        'wait_increment': '1',
        'minimum delay between ELOG post': '45',
        'observer_timeout': 0.5
    }
    config['Mirroring watchdog'] = {
        'max_attempts': '2',
        'wait': '0.5',
        'observer_timeout': 0.2
    }
    config['Image_server'] = {
        'base_path': 'R:\\A226\\Results',
        'server_root': 'https://10.166.16.24/micro',
        'image_thumb_width': 400,
        'custom_id_start': 1000,
        'tiff_tag_code': 37510
    }
    config['FEI'] = {
        'auto_calibration': True,
        'databar_removal': False
    }
    return config


def safe_configread(conffile):
    """
    Read the configuration file in a safe manner.

    This function is very useful to read in configuration file checking that
    all the relevant sections and options are there.

    The configuration file is read with the standard configparser.read method
    and a configuration object with all default sections and options is
    generated.

    The two configuration objects are compared and if a section in the read
    file is missing, then it is taken from the default.

    If any addition (section or option) was requested than the integrated
    configuration file is saved to the input file so that the same issue should
    not happen anymore.

    Parameters
    ----------
    conffile : path-like or string
        The filename of the configuration file to be read.

    Returns
    -------
    config : configparser.ConfigParser
        A ConfigParser object containing all sections and options required.

    """
    config = configparser.ConfigParser()
    config.read(conffile)

    # check if it is an old configuration file with plain text password
    if not config.has_option('elog', 'use_encrypt_pwd'):
        config['elog']['elog_password'] = encrypt_pass(
            config['elog']['elog_password'])

    # now we must check that we have everything
    conffile_needs_updates = False
    default_config = generate_default_conf()
    for section in default_config.sections():
        if not config.has_section(section):
            config.add_section(section)
            conffile_needs_updates = True
            log.info('Section %s is missing from configuration file %s. The default values will be used and the file updated' %
                     (section, conffile))
        for option in default_config.options(section):
            if not config.has_option(section, option):
                config.set(section, option, default_config[section][option])
                conffile_needs_updates = True
                log.info('Option %s from section %s is missing. The default value will be used and the file update' %
                         (option, section))

    if not config.getboolean('elog', 'use_encrypt_pwd'):
        # it looks like the user changed manually the configuration file introducing a
        # plain text password.
        # we need to hash the password and update the configuration file
        config['elog']['use_encrypt_pwd'] = "True"
        config['elog']['elog_password'] = encrypt_pass(
            config['elog']['elog_password'])
        conffile_needs_updates = True

    if conffile_needs_updates:
        write_conffile(config, conffile)
        
    return config


def write_default_conffile(filename='autolog-conf.ini'):
    """
    Write the default configuration object to a file.

    Parameters
    ----------
    filename : path-like object, optional
        The filename for the configuration file.
        The default is 'autolog-conf.ini'.

    Returns
    -------
    None.

    """
    write_conffile(generate_default_conf(), filename)


def write_conffile(config_object, filename):
    """
    Write a configuration object to a file.

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
               f'# Autologbook version v{autoconfig.VERSION}\n'
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


def parents_list(actual_path, base_path):
    """
    Generate the parents list of a given image.

    This tool is used to generate of a list of parents pairs.
    Let's assume you are adding a new image with the following path:
        actual_path = R:/A226/Results/2022/123 - proj - resp/SampleA/SubSampleB/SubSampleC/image.tiff
    and that the protocol folder is located at:
        base_path = R:/A226/Results/2022/123 - proj - resp/

    This function is returning the following list:
        ['SampleA', 'SampleA/SubSampleB', 'SampleA/SubSampleB/SubSampleC']

    It is to say a list of all parents.

    Parameters
    ----------
    actual_path : string or Path
        The full path (including the filename) of the pictures being considered.
    base_path : string or Path
        The path of the protocol.

    Returns
    -------
    parents_list : list
        A list of parent. See the function description for more details.

    """
    if not isinstance(actual_path, Path):
        actual_path = Path(actual_path)

    if not isinstance(base_path, Path):
        base_path = Path(base_path)

    full_name = str(actual_path.relative_to(base_path).parent).replace('\\','/')

    parents_list = []
    for i in range(len(full_name.split('/'))):
        element = "/".join(full_name.split("/")[0:i])
        if element != '':
            parents_list.append(element)
        
    parents_list.append(full_name)

    return parents_list




def decodeCommandOutput(text):
    """
    Decode the output of a command started with Popen.

    Parameters
    ----------
    text : STRING
        The text produced by Popen and to be decoded.

    Returns
    -------
    STRING
        The decoded text.

    """
    return '\n'.join(text.decode('utf-8').splitlines())


def ctname():
    """
    Return the current QThread name.

    Returns
    -------
    STRING
        The name of the current QThread.

    """
    return QtCore.QThread.currentThread().objectName()


class literal_str(str):
    """Type definition for the YAML representer."""

    pass


def change_style(style, representer):
    """
    Change the YAML dumper style.

    Parameters
    ----------
    style : String
        A string to define new style.
    representer : SafeRepresenter
        The yaml representer of which the style should be changed

    Returns
    -------
    Callable
        The new representer with the changed style.

    """

    def new_representer(dumper, data):
        """
        Return the new representer.

        Parameters
        ----------
        dumper : TYPE
            DESCRIPTION.
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        scalar : TYPE
            DESCRIPTION.

        """
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer


def my_excepthook(excType, excValue, traceback, logger=log):
    """Define a customized exception hook.

    Instead of printing the output of an uncaught exception to the stderr,
    it is redirected to the logger. It is very practical because it will
    appear on the GUI

    Parameters
    ----------
    excType : TYPE
        The exception type.
    excValue : TYPE
        The exception value.
    traceback : TYPE
        The whole traceback.
    logger : TYPE, optional
        The logger instance where the exception should be sent.
        The default is log.

    Returns
    -------
    None.

    """
    logger.error("Logging an uncaught exception",
                 exc_info=(excType, excValue, traceback))


def encrypt_pass(plainTextPWD):
    """
    Encrypt a plain text password.

    In order to avoid exposure of plain text password in the code, this
    helper function can be used to store hashed password directly usable for
    the elog connection.

    Parameters
    ----------
    plainTextPWD : string
        The plain text password as introduced by the user to be encrypted.

    Returns
    -------
    string
        The hashed password to be used directly in the elog connect method.

    """
    return elog.logbook._handle_pswd(plainTextPWD, True)


def dump_yaml_file(yaml_dict, yaml_filename):
    """
    Dump a yaml dictionary to a file.

    This helper function allows to save a yaml dictionary in a file using the
    right encoding.
    A line of comment is prepended to the file.

    Parameters
    ----------
    yaml_dict : dict
        The dictionary to be dumped on file.
    yaml_filename : str or path-like
        The output filename of the yaml dump..

    Returns
    -------
    None.

    """
    with open(yaml_filename, 'w', encoding='utf-8') as f:
        f.write(
            f'# YAML FILE Dumped at {datetime.now():%Y-%m-%d %H:%M:%S}\n\n')
        yaml.dump(yaml_dict, f, allow_unicode=True)


class Resolution_Unit():
    """Resolution unit of a TIFF file."""

    none = 1
    inch = 2
    cm = 3
    inverse_resolution_unit = {none: 'none', inch: 'dpi', cm: 'dpcm'}


class Picture_Resolution():
    """
    Picture Resolution class.

    It contains the horizontal and vertical resolution of a microscope picture
    along with the unit of measurements

    """

    def __init__(self, xres, yres, ures):
        self.xres = float(xres)
        self.yres = float(yres)
        if ures not in (Resolution_Unit.none, Resolution_Unit.inch, Resolution_Unit.cm):
            raise autoerror.WrongResolutionUnit('Invalid resolution unit')
        self.ures = ures

    def __eq__(self, other):
        """
        Compare two Picture Resolution object.

        If the second object has the same unit of measurements of the first one,
        the comparison is made straight forward looking at the horizontal and
        vertical resolution.

        If the two have different unit of measurements, then the second is
        temporary converted and the two resolution values are then compared.

        For the comparison a rounding of 5 digits is used.

        Parameters
        ----------
        other : Picture_Resolution instance
            Another picture resolution instance

        Returns
        -------
        bool
            True if the two Picture_Resolution objects are identical or at
            least equivalent. False otherwise.

        """
        if self.ures == other.ures:
            return round(self.xres, 5) == round(other.xres, 5) and round(self.yres, 5) == round(other.yres, 5)
        else:
            old_ures = other.ures
            other.convert_to_unit(self.ures)
            is_equal = round(self.xres, 5) == round(other.xres, 5) and round(
                self.yres, 5) == round(other.yres, 5)
            other.convert_to_unit(old_ures)
            return is_equal

    def __str__(self):
        """Print out a Picture Resolution instance."""
        return (f'({self.xres:.5} {Resolution_Unit.inverse_resolution_unit[self.ures]} '
                f'x {self.yres:5} {Resolution_Unit.inverse_resolution_unit[self.ures]})')

    def __repr__(self):
        """Represent a Picture_resolution."""        
        return f'{self.__class__.__name__}(self.xres, self.yres, self.ures)'

    def as_tuple(self):
        """Return the picture resolution as a tuple."""
        return (self.xres, self.yres, self.ures)

    def convert_to_unit(self, desired_um):
        """
        Convert the Picture Resolution to the desired unit of measurement.

        Parameters
        ----------
        desired_um : Resolution_Unit
            The target resolution unit

        Raises
        ------
        autoerror.WrongResolutionUnit
            If an invalid target resolution unit is passed.

        autoerror.ImpossibleToConvert
            If one of the two resolution has Resolution_Unit.none

        Returns
        -------
        None.

        """
        if self.ures == Resolution_Unit.none or desired_um == Resolution_Unit.none:
            raise autoerror.ImpossibleToConvert(
                'Impossible to convert, because resolution unit of measurement is none.')

        if self.ures == desired_um:
            conv_fact = 1
        else:
            if self.ures == Resolution_Unit.inch:
                if desired_um == Resolution_Unit.cm:
                    conv_fact = 1 / 2.54
                else:
                    raise autoerror.WrongResolutionUnit(
                        'Invalid resolution unit of measurment')
            else:  # self.ures == resolution_unit.cm
                if desired_um == Resolution_Unit.inch:
                    conv_fact = 2.54
                else:
                    raise autoerror.WrongResolutionUnit(
                        'Invalid resolution unit of measurment')

        self.ures = desired_um
        self.xres *= conv_fact
        self.yres *= conv_fact


def getPictureResolution(tiffinfo, source='tif', desired_um=None):
    """
    Get the Picture Resolution object from TIFF tags.

    All TIFF images must have the resolution information store in the TIFF tags.
    In the case of FEI images, the resolution information stored in the basic
    TIFF tags is incorrect while the correct one is saved in the custom FEI
    tags.

    Using this method, both resolution information can be retrieved using the
    source switch:
        'tif' : for the standard TIFF tag
        'fei' : for the FEI specific TIFF tag

    Using the desired_um, the Picture Resolution can be converted to a convenient
    unit of measurements

    Parameters
    ----------
    tiffinfo : PIL.TiffImagePlugin.ImageFileDirectory_v2
        A dictionary containing all TIFF tags
    source : str, optional
        From where the resolution information should be taken from.
        Possible values are 'fei' and 'tif'.
        The default is 'tif'.
    desired_um : Resolution_Unit, optional
        The resolution unit in which the Picture resolution should be returned.
        Use None to obtain the original one without conversion.
        The default is None.

    Returns
    -------
    None.

    """
    if not isinstance(tiffinfo, ImageFileDirectory_v2):
        raise TypeError(
            'tiffinfo must be a PIL.TiffImagePlugin.ImageFileDirectory_v2')

    source = source.lower()
    if source not in ('fei', 'tif'):
        raise ValueError('Unknown source of resolution')

    if desired_um not in (Resolution_Unit.none, Resolution_Unit.inch, Resolution_Unit.cm):
        raise ValueError('Invalid value for the target unit of measurement')

    if source == 'tif':
        xres_code = 282
        yres_code = 283
        ures_code = 296

        resolution = Picture_Resolution(tiffinfo.get(
            xres_code), tiffinfo.get(yres_code), tiffinfo.get(ures_code))
        if desired_um is not None:
            resolution.convert_to_unit(desired_um)
    elif source == 'fei':

        fei_tag_code = 34682
        fei_metadata = configparser.ConfigParser(allow_no_value=True)
        fei_metadata.read_string(tiffinfo[fei_tag_code])

        pixel_width = fei_metadata.getfloat('Scan', 'PixelWidth')
        pixel_height = fei_metadata.getfloat('Scan', 'PixelHeight')

        xres = 1 / (pixel_width * 100)
        yres = 1 / (pixel_height * 100)
        ures = Resolution_Unit.cm

        resolution = Picture_Resolution(xres, yres, ures)
        if desired_um is not None:
            resolution.convert_to_unit(desired_um)

    return resolution

