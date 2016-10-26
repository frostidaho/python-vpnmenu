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

def add_menu_flags(flags):
    for flag in flags:
        name = flag.name
        flagtxt = '--' + name.replace('_', '-')
        parser.add_argument(flagtxt, action='store_true', help=flag.info)

def add_menu_opts(opts):
    from dynmen.common import Default
    for descr in opts:
        name = descr.name
        name = '--' + name.replace('_', '-')
        d = dict(help=descr.info)
        if descr.default != Default.value:
            d['default'] = descr.default
        if descr.type != Default.type:
            d['type'] = descr.type
        parser.add_argument(name, **d)

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
    settings = rofi.meta_settings
    flags = filter(
        lambda x: x.name not in ('case_insensitive', 'password'),
        settings['Flag'],
    )
    add_menu_flags(flags)
    opts = filter(
        lambda x: x.name not in ('separator', 'prompt', 'element_height'),
        settings['Option'],
    )
    add_menu_opts(opts)
    args = parse_args(args=args)
    from pprint import pprint
    pprint(args)
    for k,v in vars(args).items():
        if v is not None:
            setattr(rofi, k, v)
    rofi.case_insensitive = True
    rofi.prompt = 'Toggle VPN:'
    out = rofi(get_all_vpn_conns())
    if out.returncode != 0:
        import sys
        print(out, file=sys.stderr)
        return out.returncode
    vpn_conn = out.value
    vpn_conn.toggle()
    return 0
