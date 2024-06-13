
from .filter_controller import Filter


class Firewall(object):

    def __init__(self, device):
        self._device = device

    @property
    def filter_controller(self) -> Filter:
        return Filter(self._device)