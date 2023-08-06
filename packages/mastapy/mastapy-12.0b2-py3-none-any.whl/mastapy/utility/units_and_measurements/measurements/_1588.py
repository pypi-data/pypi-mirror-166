"""_1588.py

CurrentPerLength
"""


from mastapy.utility.units_and_measurements import _1567
from mastapy._internal.python_net import python_net_import

_CURRENT_PER_LENGTH = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'CurrentPerLength')


__docformat__ = 'restructuredtext en'
__all__ = ('CurrentPerLength',)


class CurrentPerLength(_1567.MeasurementBase):
    """CurrentPerLength

    This is a mastapy class.
    """

    TYPE = _CURRENT_PER_LENGTH

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CurrentPerLength.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
