"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mvpnmenu` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``vpnmenu.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``vpnmenu.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-8s %(name)-12s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


import argparse
parser = argparse.ArgumentParser(description='Connect to your VPNs defined in NetworkManager using dynamic menus.')

def parse_args(args=None):
    # parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
    #                     help="A name of something.")
    args = parser.parse_args(args=args)
    return args

def get_all_vpn_conns():
    """Get vpn connections as an ordered dict

    The keys are the display values for the dynamic menu.
    The values are the corresponding objects.
    """
    from vpnmenu.mgr import all_conns
    conns = all_conns()

    from collections import OrderedDict
    return OrderedDict(((x.display_name, x) for x in conns))


def build_cmd():
    def get_menu_exec():
        from distutils.spawn import find_executable
        return find_executable('rofi') or find_executable('dmenu')

    basecmd = get_menu_exec()
    cmd = [basecmd]
    if basecmd.endswith('rofi'):
        cmd.append('-dmenu')
    else:
        cmd.extend(['-l', '10'])
    cmd.extend(['-i', '-p', 'Toggle VPN:'])
    return cmd

    
def main(args=None):
    args = parse_args(args=args)

    from dynmen import Menu
    menu = Menu(build_cmd())
    
    out = menu(get_all_vpn_conns())
    vpn_conn = out.value
    vpn_conn.toggle()
    return 0
