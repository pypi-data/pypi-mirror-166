"""_2283.py

HypoidGear
"""


from mastapy.gears.gear_designs.hypoid import _948
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2262
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGear',)


class HypoidGear(_2262.AGMAGleasonConicalGear):
    """HypoidGear

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def conical_gear_design(self) -> '_948.HypoidGearDesign':
        """HypoidGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConicalGearDesign
        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def hypoid_gear_design(self) -> '_948.HypoidGearDesign':
        """HypoidGearDesign: 'HypoidGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearDesign
        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
