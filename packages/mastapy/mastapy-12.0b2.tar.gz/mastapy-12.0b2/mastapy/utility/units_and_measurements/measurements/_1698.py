"""_1698.py

Volume
"""


from mastapy.utility.units_and_measurements import _1567
from mastapy._internal.python_net import python_net_import

_VOLUME = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Volume')


__docformat__ = 'restructuredtext en'
__all__ = ('Volume',)


class Volume(_1567.MeasurementBase):
    """Volume

    This is a mastapy class.
    """

    TYPE = _VOLUME

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Volume.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
