# https://github.com/firecat53/nmcli-dmenu/blob/master/nmcli_dmenu
# https://github.com/seveas/python-networkmanager
#     pip3 install --user python-networkmanager

# http://stackoverflow.com/questions/3472430/how-can-i-make-setuptools-install-a-package-thats-not-on-pypi
# http://stackoverflow.com/questions/12518499/pip-ignores-dependency-links-in-setup-py

from NetworkManager import (NetworkManager as _NetworkManager,
                            Settings as _Settings)
from collections import namedtuple as _namedtuple
from functools import lru_cache as _lru_cache
from dbus import DBusException as _DBusException


def _uniq(iterable):
    "Yield uniqe elements in iterable"
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item

@_lru_cache()
def get_vpn_conns():
    def _get_vpn_conns():
        for conn in _Settings.ListConnections():
            csettings = conn.GetSettings()
            if csettings['connection']['type'] == 'vpn':
                yield VpnConn(conn)
    return list(_get_vpn_conns())

def _do_wait(fn, *exceptions, initial_sleep=0.02):
    "Call fn until it doesn't raise any exceptions & return output"
    base = 1.1
    # max_factor = 100            # 100 times base
    n_steps = 48 # math.floor(math.log(max_factor, base))
    times = (initial_sleep * base**i for i in range(n_steps+1))
    for time in times:
        try:
            out = fn()
        except exceptions:
            from time import sleep
            sleep(time)
            continue
        else:
            return out
    
def get_active_vpn_conns():
    def _get_conns():
        for conn in _NetworkManager.ActiveConnections:
            if conn.Type == 'vpn':
                yield ActiveVpnConn(conn)
    return _do_wait(lambda: list(_get_conns()), _DBusException)


VpnStatus = _namedtuple('VpnStatus', 'active active_path path')

class VpnConn(object):
    def __init__(self, conn):
        try:
            data = conn.GetSettings()
            conn_active = None
        except _DBusException:
            self._active_conn = conn
            conn = conn.Connection
            data = conn.GetSettings()

        self._name = data['connection']['id']
        self._uuid = data['connection']['uuid']
        self.conn = conn

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self.name

    @property
    def uuid(self):
        return self._uuid

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __hash__(self):
        return self.uuid.__hash__()

    def __lt__(self, other):
        return self.name < other.name

    @property
    def path(self):
        return str(self.conn.object_path)

    def get_status(self):
        active = [x for x in get_active_vpn_conns() if x.uuid == self.uuid]
        if len(active) == 0:
            return VpnStatus(active=False, active_path='', path=self.path)
        elif len(active) == 1:
            return VpnStatus(
                active=True,
                active_path=str(active[0]._active_conn.object_path),
                path = self.path,
            )
        else:
            raise ConnectionError('vpn is active multiple times: {}'.format(active))

    def toggle(self):
        status = self.get_status()
        if status.active:
            self.stop()
        else:
            self.start()

    def start(self):
        status = self.get_status()
        if status.active:
            return status
        active = [x for x in get_active_vpn_conns() if x.uuid != self.uuid]
        if active:
            raise ConnectionError('Another vpn connection is active: {}'.format(active))
        _NetworkManager.ActivateConnection(status.path, '/', '/')
        return self.get_status()

    def stop(self):
        status = self.get_status()
        if not status.active:
            return status
        _NetworkManager.DeactivateConnection(status.active_path)
        return self.get_status()

    def __repr__(self):
        cname = self.__class__.__name__
        rep = '{}('.format(cname) + '{!r}, {!r})'
        return rep.format(self.name, self.uuid)


class ActiveVpnConn(VpnConn):
    @property
    def display_name(self):
        return '• {}'.format(self.name)

def all_conns():
    """Get a list of all active & available vpn connections

    active connections listed first and are of type ActiveVpnConn
    available connections are of type VpnConn

    both classes are functionally identital, except that
    their display_name attributes are different
    """
    from itertools import chain
    conns = _uniq(chain(get_active_vpn_conns(), sorted(get_vpn_conns())))
    return list(conns)

if __name__ == '__main__':
    for conn in all_conns():
        print(conn.display_name)
