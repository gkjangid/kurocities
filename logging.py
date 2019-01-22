from pprint import pformat
import logging as _logging

colors = {
    'black'         : '\033[0;30m%s\033[0;0m',
    'blue'          : '\033[0;34m%s\033[0;0m',
    'green'         : '\033[0;32m%s\033[0;0m',
    'cyan'          : '\033[0;36m%s\033[0;0m',
    'red'           : '\033[0;31m%s\033[0;0m',
    'purple'        : '\033[0;35m%s\033[0;0m',
    'brown'         : '\033[0;33m%s\033[0;0m',
    'light_gray'    : '\033[0;37m%s\033[0;0m',
    'dark_gray'     : '\033[1;30m%s\033[0;0m',
    'light_blue'    : '\033[1;34m%s\033[0;0m',
    'light_green'   : '\033[1;32m%s\033[0;0m',
    'light_cyan'    : '\033[1;36m%s\033[0;0m',
    'light_red'     : '\033[1;31m%s\033[0;0m',
    'light_purple'  : '\033[1;35m%s\033[0;0m',
    'yellow'        : '\033[1;33m%s\033[0;0m',
    'white'         : '\033[1;37m%s\033[0;0m',
}

def color_text( text: str, color_name: str ) -> str:
    color_name = color_name.lower()
    color = colors.get( color_name, '%s' )
    return color % text

def comment( msg: str ) -> None:
    _logging.warn( color_text( msg, 'cyan' ) )

def debug( msg: str ) -> None:
    _logging.debug( color_text( msg, 'blue' ) )


def info( msg: str ) -> None:
    _logging.info( color_text( msg, 'green' ) )

def warn( msg: str ) -> None:
    _logging.warn( color_text( msg, 'yellow' ) )

def error( msg: str ) -> None:
    _logging.error( color_text( msg, 'red' ) )

def critical( msg: str ) -> None:
    _logging.critical( color_text( msg, 'light_red' ) )


def pp( obj, comment_text=None, level='warn' ):
    method = getattr( globals(), level, warn )
    if comment_text:
        comment( comment_text )
    method( pformat( obj ))

def ppdir( obj, comment_text=None, level='warn' ):
    method = getattr( globals(), level, warn )
    if comment_text:
        comment( comment_text )
    method( pformat( dir( obj ) ))
