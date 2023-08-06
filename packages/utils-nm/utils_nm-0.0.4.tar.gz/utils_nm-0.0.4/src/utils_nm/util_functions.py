# util_functions.py
# -*- coding: utf-8 -*-

"""
Functions which serve for general purposes
"""

import inspect
import logging
import warnings
import traceback
from pathlib import Path
from datetime import datetime


# ______________________________________________________________________________________________________________________


def add_to_namespace(name: str, value: object, namespace: dict) -> None:
    """
    adds a variable to the namespace

    Args:
        name: the name of the variable
        value: the value of the variable
        namespace: the namespace where it should be added

    Returns:
        None
    """

    if name in namespace:
        warnings.warn(
            f'Function <{inspect.currentframe().f_code.co_name}>: '
            f'overwriting <{name}> which already existed in the namespace!'
        )
    namespace[name] = value
    return None


# ______________________________________________________________________________________________________________________


def check_if_in_argv(arg, argument) -> bool:
    """
    checks if -arg or --argument is in sys.argv

    Args:
        arg: the name of the argument in short notation
        argument: the name of the argument in verbose notation

    Returns:
        True if the argument is part of argv, else False
    """
    import sys
    return f'-{arg}' in sys.argv or f'--{argument}' in sys.argv


# ______________________________________________________________________________________________________________________


def parse_bool(arg: str) -> bool:
    """
    parse a script argument to a boolean value.

    Args:
        arg: the input argument

    Returns:
        Boolean value of arg
    """
    inp = str(arg).lower()
    if 'true'.startswith(inp):
        return True
    elif 'false'.startswith(inp):
        return False
    else:
        raise ValueError(f'arg needs to be one of [ True | False ], but arg was {str(arg)}')


# ______________________________________________________________________________________________________________________


def input_prompt(name: str, choices: tuple = (None, ), default: object = None, enum: bool = False) -> object:
    """
    wrapper for pythons input() with choices, default value and continuous prompting if an invalid input was supplied.

    Args:
        name: the name of the variable
        choices: the allowed values for input. If None, anything can be input
        default: the default value. If None, the user will continue to be prompted
        enum: enumerate the choices and allow for numerical input

    Returns:
        user input
    """

    print(f'please set the {name}:')
    inp = None
    if choices == (None, ):
        inp = input()
    elif not enum:
        while inp not in choices:
            inp = input(f'\t-> choose between [{", ".join(str(e) for e in choices)}], default to: {default} ')
            inp = default if inp == '' else inp
        print()
    else:
        available_choices = {i: item for i, item in enumerate(choices, start=1)}
        print('  choose from', end='')
        print('\t', *available_choices.items(), sep='\n\t')
        print(f'  default will be {default}')
        while not (inp in available_choices.values() or inp in [str(i) for i in available_choices.keys()] or inp == ''):
            inp = input('\t-> enter the number or value of your choice ')
            inp = default if inp == '' else inp

        if inp.isdigit():
            inp = available_choices[int(inp)]

    return inp


# ______________________________________________________________________________________________________________________


def create_logger(name: str, log_file_path: str | Path = None) -> logging.Logger:
    """
    logger factory function

    Args:
        name: the name of the logger
        log_file_path: the path to the logging file, if None, then no file handler will be added

    Returns:
        an instance of a logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logging_console_formatter = logging.Formatter('%(levelname)s | %(message)s')
    logging_console_handler = logging.StreamHandler()
    logging_console_handler.setLevel(logging.DEBUG)
    logging_console_handler.setFormatter(logging_console_formatter)
    logger.addHandler(logging_console_handler)

    if log_file_path is not None:
        logging_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | module: %(module)s | %(message)s')
        logging_file_handler = logging.FileHandler(log_file_path)
        logging_file_handler.setLevel(logging.INFO)
        logging_file_handler.setFormatter(logging_file_formatter)
        logger.addHandler(logging_file_handler)

    return logger


# ______________________________________________________________________________________________________________________


def format_email_error_message(exception: Exception, project: str, wd: Path, log_file_path: Path) -> tuple:
    """
    prepares a formatted subject and body for the e_mail message

    Args:
        exception: the raised exception from the try block
        project: the project name
        wd: the working directory
        log_file_path: the Path object to the log file

    Returns:
        tuple of strings (e_mail_subject, e_mail_message)
    """

    tb = traceback.TracebackException.from_exception(exception)
    traceback_error = ''.join(tb.format())
    error = tb.exc_type.__name__

    e_mail_subject = f'Error {error} in {project}'
    with open(wd / 'templates' / 'email' / 'error_message.html', 'r', encoding='utf-8') as f:
        e_mail_message = f.read()
    e_mail_message = e_mail_message.replace('{{ project }}', project)
    e_mail_message = e_mail_message.replace('{{ datetime_now }}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    e_mail_message = e_mail_message.replace('{{ error }}', error)
    e_mail_message = e_mail_message.replace('{{ traceback_error }}', traceback_error)
    e_mail_message = e_mail_message.replace('{{ log_file_path }}', str(log_file_path.resolve()))

    return e_mail_subject, e_mail_message

# ______________________________________________________________________________________________________________________
