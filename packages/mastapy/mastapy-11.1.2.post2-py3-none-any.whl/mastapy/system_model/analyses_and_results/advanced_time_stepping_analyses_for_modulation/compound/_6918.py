﻿"""_6918.py

DatumCompoundAdvancedTimeSteppingAnalysisForModulation
"""


from typing import List

from mastapy.system_model.part_model import _2199
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6788
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6892
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'DatumCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundAdvancedTimeSteppingAnalysisForModulation',)


class DatumCompoundAdvancedTimeSteppingAnalysisForModulation(_6892.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation):
    """DatumCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _DATUM_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2199.Datum':
        """Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign
        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6788.DatumAdvancedTimeSteppingAnalysisForModulation]':
        """List[DatumAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady
        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6788.DatumAdvancedTimeSteppingAnalysisForModulation]':
        """List[DatumAdvancedTimeSteppingAnalysisForModulation]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases
        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
