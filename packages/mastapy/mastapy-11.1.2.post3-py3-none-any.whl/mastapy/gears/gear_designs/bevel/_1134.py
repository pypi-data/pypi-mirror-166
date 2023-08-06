﻿"""_1134.py

BevelGearDesign
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.bevel import _1140
from mastapy.gears.gear_designs.agma_gleason_conical import _1147
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'BevelGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearDesign',)


class BevelGearDesign(_1147.AGMAGleasonConicalGearDesign):
    """BevelGearDesign

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'BevelGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def addendum(self) -> 'float':
        """float: 'Addendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Addendum
        return temp

    @property
    def addendum_angle(self) -> 'float':
        """float: 'AddendumAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AddendumAngle
        return temp

    @property
    def crown_to_cross_point(self) -> 'float':
        """float: 'CrownToCrossPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CrownToCrossPoint
        return temp

    @property
    def dedendum(self) -> 'float':
        """float: 'Dedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Dedendum
        return temp

    @property
    def dedendum_angle(self) -> 'float':
        """float: 'DedendumAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DedendumAngle
        return temp

    @property
    def difference_from_ideal_pitch_angle(self) -> 'float':
        """float: 'DifferenceFromIdealPitchAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DifferenceFromIdealPitchAngle
        return temp

    @property
    def face_apex_to_cross_point(self) -> 'float':
        """float: 'FaceApexToCrossPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceApexToCrossPoint
        return temp

    @property
    def face_width_as_percent_of_cone_distance(self) -> 'float':
        """float: 'FaceWidthAsPercentOfConeDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceWidthAsPercentOfConeDistance
        return temp

    @property
    def finishing_method(self) -> '_1140.FinishingMethods':
        """FinishingMethods: 'FinishingMethod' is the original name of this property."""

        temp = self.wrapped.FinishingMethod
        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1140.FinishingMethods)(value) if value is not None else None

    @finishing_method.setter
    def finishing_method(self, value: '_1140.FinishingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FinishingMethod = value

    @property
    def front_crown_to_cross_point(self) -> 'float':
        """float: 'FrontCrownToCrossPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrontCrownToCrossPoint
        return temp

    @property
    def inner_slot_width_at_minimum_backlash(self) -> 'float':
        """float: 'InnerSlotWidthAtMinimumBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerSlotWidthAtMinimumBacklash
        return temp

    @property
    def inner_spiral_angle(self) -> 'float':
        """float: 'InnerSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InnerSpiralAngle
        return temp

    @property
    def mean_addendum(self) -> 'float':
        """float: 'MeanAddendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanAddendum
        return temp

    @property
    def mean_chordal_addendum(self) -> 'float':
        """float: 'MeanChordalAddendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanChordalAddendum
        return temp

    @property
    def mean_dedendum(self) -> 'float':
        """float: 'MeanDedendum' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanDedendum
        return temp

    @property
    def mean_normal_circular_thickness_for_zero_backlash(self) -> 'float':
        """float: 'MeanNormalCircularThicknessForZeroBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalCircularThicknessForZeroBacklash
        return temp

    @property
    def mean_normal_circular_thickness_with_backlash(self) -> 'float':
        """float: 'MeanNormalCircularThicknessWithBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanNormalCircularThicknessWithBacklash
        return temp

    @property
    def mean_pitch_diameter(self) -> 'float':
        """float: 'MeanPitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanPitchDiameter
        return temp

    @property
    def mean_slot_width_at_minimum_backlash(self) -> 'float':
        """float: 'MeanSlotWidthAtMinimumBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanSlotWidthAtMinimumBacklash
        return temp

    @property
    def mean_transverse_circular_thickness_for_zero_backlash(self) -> 'float':
        """float: 'MeanTransverseCircularThicknessForZeroBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTransverseCircularThicknessForZeroBacklash
        return temp

    @property
    def mean_transverse_circular_thickness_with_backlash(self) -> 'float':
        """float: 'MeanTransverseCircularThicknessWithBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanTransverseCircularThicknessWithBacklash
        return temp

    @property
    def outer_slot_width_at_minimum_backlash(self) -> 'float':
        """float: 'OuterSlotWidthAtMinimumBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSlotWidthAtMinimumBacklash
        return temp

    @property
    def outer_spiral_angle(self) -> 'float':
        """float: 'OuterSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterSpiralAngle
        return temp

    @property
    def outer_tip_diameter(self) -> 'float':
        """float: 'OuterTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterTipDiameter
        return temp

    @property
    def outer_transverse_circular_thickness_for_zero_backlash(self) -> 'float':
        """float: 'OuterTransverseCircularThicknessForZeroBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterTransverseCircularThicknessForZeroBacklash
        return temp

    @property
    def outer_transverse_circular_thickness_with_backlash(self) -> 'float':
        """float: 'OuterTransverseCircularThicknessWithBacklash' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OuterTransverseCircularThicknessWithBacklash
        return temp

    @property
    def pitch_angle(self) -> 'float':
        """float: 'PitchAngle' is the original name of this property."""

        temp = self.wrapped.PitchAngle
        return temp

    @pitch_angle.setter
    def pitch_angle(self, value: 'float'):
        self.wrapped.PitchAngle = float(value) if value else 0.0

    @property
    def pitch_apex_to_boot(self) -> 'float':
        """float: 'PitchApexToBoot' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchApexToBoot
        return temp

    @property
    def pitch_apex_to_cross_point(self) -> 'float':
        """float: 'PitchApexToCrossPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchApexToCrossPoint
        return temp

    @property
    def pitch_apex_to_crown(self) -> 'float':
        """float: 'PitchApexToCrown' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchApexToCrown
        return temp

    @property
    def pitch_apex_to_front_boot(self) -> 'float':
        """float: 'PitchApexToFrontBoot' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchApexToFrontBoot
        return temp

    @property
    def pitch_apex_to_front_crown(self) -> 'float':
        """float: 'PitchApexToFrontCrown' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchApexToFrontCrown
        return temp

    @property
    def pitch_diameter(self) -> 'float':
        """float: 'PitchDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchDiameter
        return temp

    @property
    def pitch_diameter_at_wheel_outer_section(self) -> 'float':
        """float: 'PitchDiameterAtWheelOuterSection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PitchDiameterAtWheelOuterSection
        return temp

    @property
    def root_apex_to_cross_point(self) -> 'float':
        """float: 'RootApexToCrossPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootApexToCrossPoint
        return temp

    @property
    def stock_allowance(self) -> 'float':
        """float: 'StockAllowance' is the original name of this property."""

        temp = self.wrapped.StockAllowance
        return temp

    @stock_allowance.setter
    def stock_allowance(self, value: 'float'):
        self.wrapped.StockAllowance = float(value) if value else 0.0

    @property
    def surface_finish(self) -> 'float':
        """float: 'SurfaceFinish' is the original name of this property."""

        temp = self.wrapped.SurfaceFinish
        return temp

    @surface_finish.setter
    def surface_finish(self, value: 'float'):
        self.wrapped.SurfaceFinish = float(value) if value else 0.0
