﻿"""_1485.py

RealMatrix
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1474
from mastapy._internal.python_net import python_net_import

_REAL_MATRIX = python_net_import('SMT.MastaAPI.MathUtility', 'RealMatrix')


__docformat__ = 'restructuredtext en'
__all__ = ('RealMatrix',)


class RealMatrix(_1474.GenericMatrix['float', 'RealMatrix']):
    """RealMatrix

    This is a mastapy class.
    """

    TYPE = _REAL_MATRIX

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RealMatrix.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def get_column_at(self, index: 'int') -> 'List[float]':
        """ 'GetColumnAt' is the original name of this method.

        Args:
            index (int)

        Returns:
            List[float]
        """

        index = int(index)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetColumnAt(index if index else 0), float)

    def get_row_at(self, index: 'int') -> 'List[float]':
        """ 'GetRowAt' is the original name of this method.

        Args:
            index (int)

        Returns:
            List[float]
        """

        index = int(index)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetRowAt(index if index else 0), float)
