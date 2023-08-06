﻿"""_1017.py

ISO6336GeometryForShapedGears
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _1016
from mastapy._internal.python_net import python_net_import

_ISO6336_GEOMETRY_FOR_SHAPED_GEARS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'ISO6336GeometryForShapedGears')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO6336GeometryForShapedGears',)


class ISO6336GeometryForShapedGears(_1016.ISO6336GeometryBase):
    """ISO6336GeometryForShapedGears

    This is a mastapy class.
    """

    TYPE = _ISO6336_GEOMETRY_FOR_SHAPED_GEARS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ISO6336GeometryForShapedGears.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def auxiliary_angle(self) -> 'float':
        """float: 'AuxiliaryAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AuxiliaryAngle
        return temp

    @property
    def base_radius_of_the_tool(self) -> 'float':
        """float: 'BaseRadiusOfTheTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BaseRadiusOfTheTool
        return temp

    @property
    def cutting_pitch_radius_of_the_gear(self) -> 'float':
        """float: 'CuttingPitchRadiusOfTheGear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CuttingPitchRadiusOfTheGear
        return temp

    @property
    def cutting_pitch_radius_of_the_tool(self) -> 'float':
        """float: 'CuttingPitchRadiusOfTheTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CuttingPitchRadiusOfTheTool
        return temp

    @property
    def distance_of_the_point_m_to_the_point_of_contact_of_the_pitch_circles(self) -> 'float':
        """float: 'DistanceOfThePointMToThePointOfContactOfThePitchCircles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DistanceOfThePointMToThePointOfContactOfThePitchCircles
        return temp

    @property
    def equivalent_numbers_of_teeth(self) -> 'float':
        """float: 'EquivalentNumbersOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentNumbersOfTeeth
        return temp

    @property
    def half_angle_of_thickness_at_point_m(self) -> 'float':
        """float: 'HalfAngleOfThicknessAtPointM' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfAngleOfThicknessAtPointM
        return temp

    @property
    def manufacturing_centre_distance(self) -> 'float':
        """float: 'ManufacturingCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ManufacturingCentreDistance
        return temp

    @property
    def manufacturing_tooth_ratio(self) -> 'float':
        """float: 'ManufacturingToothRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ManufacturingToothRatio
        return temp

    @property
    def radius_of_point_m(self) -> 'float':
        """float: 'RadiusOfPointM' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadiusOfPointM
        return temp

    @property
    def theta(self) -> 'float':
        """float: 'Theta' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Theta
        return temp

    @property
    def tooth_root_fillet_radius(self) -> 'float':
        """float: 'ToothRootFilletRadius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootFilletRadius
        return temp

    @property
    def tooth_root_thickness(self) -> 'float':
        """float: 'ToothRootThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootThickness
        return temp

    @property
    def transverse_pressure_angle_for_radius_of_point_m(self) -> 'float':
        """float: 'TransversePressureAngleForRadiusOfPointM' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransversePressureAngleForRadiusOfPointM
        return temp

    @property
    def virtual_tip_diameter_of_tool(self) -> 'float':
        """float: 'VirtualTipDiameterOfTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VirtualTipDiameterOfTool
        return temp

    @property
    def working_pressure_angle(self) -> 'float':
        """float: 'WorkingPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingPressureAngle
        return temp
