﻿"""_1510.py

ParetoOptimisationStrategy
"""


from typing import List

from mastapy.math_utility.optimisation import _1512, _1508, _1509
from mastapy._internal import constructor, conversion
from mastapy.utility.databases import _1789
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_STRATEGY = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationStrategy')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationStrategy',)


class ParetoOptimisationStrategy(_1789.NamedDatabaseItem):
    """ParetoOptimisationStrategy

    This is a mastapy class.
    """

    TYPE = _PARETO_OPTIMISATION_STRATEGY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParetoOptimisationStrategy.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def charts(self) -> 'List[_1512.ParetoOptimisationStrategyChartInformation]':
        """List[ParetoOptimisationStrategyChartInformation]: 'Charts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Charts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def inputs(self) -> 'List[_1508.ParetoOptimisationInput]':
        """List[ParetoOptimisationInput]: 'Inputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Inputs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def outputs(self) -> 'List[_1509.ParetoOptimisationOutput]':
        """List[ParetoOptimisationOutput]: 'Outputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Outputs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def add_chart(self):
        """ 'AddChart' is the original name of this method."""

        self.wrapped.AddChart()
