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
import argparse
from vpnmenu import mgr
from dynmen.rofi import Rofi as _Rofi
from collections import OrderedDict



def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Connect to your VPNs defined in NetworkManager using dynamic menus.')
    parser.add_argument('names', metavar='NAME', nargs=argparse.ZERO_OR_MORE,
                        help="A name of something.")
    args = parser.parse_args(args=args)
    return args

def main(args=None):
    args = parse_args(args=args)
    conns = mgr.all_conns()
    od = OrderedDict(((x.display_name, x) for x in conns))
    rofi = _Rofi()
    rofi.case_insensitive = True
    out = rofi(od)
    print(out)
    
    

