﻿"""_2037.py

GreaseQuantity
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _2045
from mastapy._internal.python_net import python_net_import

_GREASE_QUANTITY = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'GreaseQuantity')


__docformat__ = 'restructuredtext en'
__all__ = ('GreaseQuantity',)


class GreaseQuantity(_2045.SKFCalculationResult):
    """GreaseQuantity

    This is a mastapy class.
    """

    TYPE = _GREASE_QUANTITY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GreaseQuantity.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ring(self) -> 'float':
        """float: 'Ring' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Ring

        if temp is None:
            return 0.0

        return temp

    @property
    def side(self) -> 'float':
        """float: 'Side' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Side

        if temp is None:
            return 0.0

        return temp
