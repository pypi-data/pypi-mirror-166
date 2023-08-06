﻿"""_360.py

VirtualCylindricalGear
"""


from mastapy._internal import constructor
from mastapy.gears.rating.virtual_cylindrical_gears import _361
from mastapy._internal.python_net import python_net_import

_VIRTUAL_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears', 'VirtualCylindricalGear')


__docformat__ = 'restructuredtext en'
__all__ = ('VirtualCylindricalGear',)


class VirtualCylindricalGear(_361.VirtualCylindricalGearBasic):
    """VirtualCylindricalGear

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_CYLINDRICAL_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'VirtualCylindricalGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def base_diameter_of_virtual_cylindrical_gear(self) -> 'float':
        """float: 'BaseDiameterOfVirtualCylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseDiameterOfVirtualCylindricalGear
        return temp

    @property
    def base_pitch_normal_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'BasePitchNormalForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasePitchNormalForVirtualCylindricalGears
        return temp

    @property
    def base_pitch_transverse_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'BasePitchTransverseForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasePitchTransverseForVirtualCylindricalGears
        return temp

    @property
    def contact_ratio_of_addendum_normal_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'ContactRatioOfAddendumNormalForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioOfAddendumNormalForVirtualCylindricalGears
        return temp

    @property
    def contact_ratio_of_addendum_transverse_for_virtual_cylindrical_gears(self) -> 'float':
        """float: 'ContactRatioOfAddendumTransverseForVirtualCylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactRatioOfAddendumTransverseForVirtualCylindricalGears
        return temp

    @property
    def effective_pressure_angle(self) -> 'float':
        """float: 'EffectivePressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectivePressureAngle
        return temp

    @property
    def path_of_addendum_contact_normal(self) -> 'float':
        """float: 'PathOfAddendumContactNormal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PathOfAddendumContactNormal
        return temp

    @property
    def path_of_addendum_contact_transverse(self) -> 'float':
        """float: 'PathOfAddendumContactTransverse' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PathOfAddendumContactTransverse
        return temp

    @property
    def transverse_pressure_angle(self) -> 'float':
        """float: 'TransversePressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransversePressureAngle
        return temp
