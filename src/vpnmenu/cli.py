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

def main(args=None):
    from dynmen.rofi import Rofi
    rofi = Rofi()
    rofi.dmenu = True
    rofi.i = True
    rofi.p = 'Toggle VPN:'

    args = parse_args(args=args)
    from pprint import pprint
    pprint(args)
    for k,v in vars(args).items():
        if v is not None:
            setattr(rofi, k, v)
    out = rofi(get_all_vpn_conns())
    if out.returncode != 0:
        import sys
        print(out, file=sys.stderr)
        return out.returncode
    vpn_conn = out.value
    vpn_conn.toggle()
    return 0
