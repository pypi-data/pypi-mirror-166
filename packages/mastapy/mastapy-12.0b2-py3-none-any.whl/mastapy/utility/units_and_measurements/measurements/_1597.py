﻿"""_1597.py

ElectricCurrent
"""


from mastapy.utility.units_and_measurements import _1567
from mastapy._internal.python_net import python_net_import

_ELECTRIC_CURRENT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'ElectricCurrent')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricCurrent',)


class ElectricCurrent(_1567.MeasurementBase):
    """ElectricCurrent

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_CURRENT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricCurrent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
