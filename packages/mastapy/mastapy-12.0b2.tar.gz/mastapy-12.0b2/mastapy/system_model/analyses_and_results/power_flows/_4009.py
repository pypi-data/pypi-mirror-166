﻿"""_4009.py

CVTBeltConnectionPowerFlow
"""


from mastapy.system_model.connections_and_sockets import _2218
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _3978
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CVTBeltConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionPowerFlow',)


class CVTBeltConnectionPowerFlow(_3978.BeltConnectionPowerFlow):
    """CVTBeltConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE = _CVT_BELT_CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2218.CVTBeltConnection':
        """CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
