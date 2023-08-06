"""Holds various Version strings of FAST-MPF.

This modules holds the FAST-MPF version strings, including the version of BCP
it needs and the config file version it needs.

It's used internally for all sorts of things, from printing the output of the
`fast-mpf --version` command, to making sure any processes connected via BCP
are the proper versions, to automatically triggering new builds and deployments
to PyPI.

"""

__version__ = '0.56.0.dev42'
'''The full version of FAST-MPF. major.minor.patch.build'''

__short_version__ = '0.56'
'''The major.minor version of FAST-MPF.'''

__bcp_version__ = '1.1'
'''The version of BCP this build of FAST-MPF uses.'''

__config_version__ = '5'
'''The config file version this build of MPF uses.'''

__show_version__ = '5'
'''The show format version this build of MPF uses.'''

# pylint: disable-msg=invalid-name
version = "FAST-MPF v{}".format(__version__)
'''A friendly version string for this build of MPF.'''

# pylint: disable-msg=invalid-name
extended_version = "FAST-MPF v{}, Config version:{}, Show version: {}, " \
                   "BCP version:{}".format(__version__, __config_version__,
                                           __show_version__, __bcp_version__)
'''An extended version string that includes the FAST-MPF version, show version,
and BCP versions used in this build of FAST-MPF.'''

if "dev" in __version__:
    # pylint: disable-msg=invalid-name
    log_url = "https://docs.missionpinball.org/en/dev/logs/{}.html"
else:
    # pylint: disable-msg=invalid-name
    log_url = "https://docs.missionpinball.org/en/{}/logs/{{}}.html".format(__short_version__)

__api__ = ['version',
           '__short_version__',
           '__bcp_version__',
           '__config_version__',
           '__show_version__',
           'version',
           'extended_version',
           'log_url']
