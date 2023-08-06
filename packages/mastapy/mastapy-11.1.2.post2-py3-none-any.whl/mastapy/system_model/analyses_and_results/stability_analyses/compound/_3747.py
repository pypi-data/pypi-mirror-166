﻿"""_3747.py

StraightBevelGearCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2296
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3620
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3655
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'StraightBevelGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearCompoundStabilityAnalysis',)


class StraightBevelGearCompoundStabilityAnalysis(_3655.BevelGearCompoundStabilityAnalysis):
    """StraightBevelGearCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2296.StraightBevelGear':
        """StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign
        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3620.StraightBevelGearStabilityAnalysis]':
        """List[StraightBevelGearStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady
        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3620.StraightBevelGearStabilityAnalysis]':
        """List[StraightBevelGearStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases
        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
