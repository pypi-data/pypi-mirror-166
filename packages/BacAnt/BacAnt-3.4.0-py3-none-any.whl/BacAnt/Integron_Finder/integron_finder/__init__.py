import sys
from time import localtime, strftime

__version__ = '2-{}'.format(strftime("%Y-%m-%d", localtime()))
current_dir = sys.path[0]
__INTEGRON_DATA__ = current_dir+"/../BacAnt/Integron_Finder"


class IntegronError(Exception):
    pass


class EmptyFileError(IntegronError):
    pass


def get_version_message():
    from numpy import __version__ as np_vers
    from pandas import __version__ as pd_vers
    from matplotlib import __version__ as mplt_vers
    from Bio import __version__ as bio_vers
    version_text = """integron_finder version {i_f}
Using:    
 - Python {py}
 - numpy {np}
 - pandas {pd}
 - matplolib {mplt}
 - biopython {bio}
 """.format(i_f=__version__,
            py=sys.version.replace('\n', ' '),
            np=np_vers,
            pd=pd_vers,
            mplt=mplt_vers,
            bio=bio_vers
            )
    return version_text


def init_logger(log_file=None, out=True):
    import colorlog
    logger = colorlog.getLogger('integron_finder')
    logging = colorlog.logging.logging
    if out:
        stdout_handler = colorlog.StreamHandler(sys.stdout)
        stdout_formatter = colorlog.ColoredFormatter("%(log_color)s%(levelname)-8s : %(reset)s %(message)s",
                                                     datefmt=None,
                                                     reset=True,
                                                     log_colors={
                                                         'DEBUG':    'cyan',
                                                         'INFO':     'green',
                                                         'WARNING':  'yellow',
                                                         'ERROR':    'red',
                                                         'CRITICAL': 'bold_red',
                                                     },
                                                     secondary_log_colors={},
                                                     style='%'
                                                     )
        stdout_handler.setFormatter(stdout_formatter)
        logger.addHandler(stdout_handler)
    else:
        null_handler = logging.NullHandler()
        logger.addHandler(null_handler)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter("%(levelname)-8s : %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    logger.setLevel(logging.WARNING)


def logger_set_level(level='WARNING'):
    # default value must be a string
    # cannot be colorlog.logging.logging.WARNING for instance
    # because setup import __init__ to get __version__
    # so logger_set_level is defined
    # if level is colorlog.logging.logging.WARNING
    # that mean that colorlog must be already installed
    # otherwise an error occured during pip install
    #  NameError: name 'colorlog' is not defined
    import colorlog

    levels = {'NOTSET': colorlog.logging.logging.NOTSET,
              'DEBUG': colorlog.logging.logging.DEBUG,
              'INFO': colorlog.logging.logging.INFO,
              'WARNING': colorlog.logging.logging.WARNING,
              'ERROR': colorlog.logging.logging.ERROR,
              'CRITICAL': colorlog.logging.logging.CRITICAL,
              }
    if level in levels:
        level = levels[level]
    elif not isinstance(level, int):
        raise IntegronError("Level must be {} or a positive integer")
    elif level < 0:
        raise IntegronError("Level must be {} or a positive integer")

    logger = colorlog.getLogger('integron_finder')
    if level <= colorlog.logging.logging.DEBUG:
        stdout_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s : %(module)s: L %(lineno)d :%(reset)s %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
            secondary_log_colors={},
            style='%'
            )
        stdout_handler = logger.handlers[0]
        stdout_handler.setFormatter(stdout_formatter)

        logging = colorlog.logging.logging
        file_formatter = logging.Formatter("%(levelname)-8s : %(module)s: L %(lineno)d : %(message)s")
        file_handler = logger.handlers[1]
        file_handler.setFormatter(file_formatter)

    logger.setLevel(level)
