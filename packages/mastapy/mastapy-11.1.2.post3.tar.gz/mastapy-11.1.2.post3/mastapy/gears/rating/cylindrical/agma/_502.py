﻿"""_502.py

AGMA2101MeshSingleFlankRating
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.materials import _231
from mastapy.gears.gear_designs.cylindrical import _989, _1033
from mastapy.gears.rating.cylindrical.agma import _501
from mastapy.gears.rating.cylindrical import _437
from mastapy._internal.python_net import python_net_import

_AGMA2101_MESH_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.AGMA', 'AGMA2101MeshSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMA2101MeshSingleFlankRating',)


class AGMA2101MeshSingleFlankRating(_437.CylindricalMeshSingleFlankRating):
    """AGMA2101MeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _AGMA2101_MESH_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'AGMA2101MeshSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_length_of_line_of_contact(self) -> 'float':
        """float: 'ActiveLengthOfLineOfContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveLengthOfLineOfContact
        return temp

    @property
    def actual_tangential_load(self) -> 'float':
        """float: 'ActualTangentialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActualTangentialLoad
        return temp

    @property
    def average_roughness_ra(self) -> 'float':
        """float: 'AverageRoughnessRa' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageRoughnessRa
        return temp

    @property
    def bearing_span(self) -> 'float':
        """float: 'BearingSpan' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingSpan
        return temp

    @property
    def combined_derating_factor(self) -> 'float':
        """float: 'CombinedDeratingFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CombinedDeratingFactor
        return temp

    @property
    def composite_surface_roughness_at_fc(self) -> 'float':
        """float: 'CompositeSurfaceRoughnessAtFC' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CompositeSurfaceRoughnessAtFC
        return temp

    @property
    def contact_load_factor(self) -> 'float':
        """float: 'ContactLoadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactLoadFactor
        return temp

    @property
    def elastic_coefficient(self) -> 'float':
        """float: 'ElasticCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ElasticCoefficient
        return temp

    @property
    def entraining_velocity_at_end_of_active_profile(self) -> 'float':
        """float: 'EntrainingVelocityAtEndOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EntrainingVelocityAtEndOfActiveProfile
        return temp

    @property
    def entraining_velocity_at_pitch_point(self) -> 'float':
        """float: 'EntrainingVelocityAtPitchPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EntrainingVelocityAtPitchPoint
        return temp

    @property
    def entraining_velocity_at_start_of_active_profile(self) -> 'float':
        """float: 'EntrainingVelocityAtStartOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EntrainingVelocityAtStartOfActiveProfile
        return temp

    @property
    def face_load_distribution_factor(self) -> 'float':
        """float: 'FaceLoadDistributionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceLoadDistributionFactor
        return temp

    @property
    def fifth_distance_along_line_of_action(self) -> 'float':
        """float: 'FifthDistanceAlongLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FifthDistanceAlongLineOfAction
        return temp

    @property
    def filter_cutoff_wave_length(self) -> 'float':
        """float: 'FilterCutoffWaveLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FilterCutoffWaveLength
        return temp

    @property
    def first_distance_along_line_of_action(self) -> 'float':
        """float: 'FirstDistanceAlongLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FirstDistanceAlongLineOfAction
        return temp

    @property
    def fourth_distance_along_line_of_action(self) -> 'float':
        """float: 'FourthDistanceAlongLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FourthDistanceAlongLineOfAction
        return temp

    @property
    def gearing_type(self) -> '_231.GearingTypes':
        """GearingTypes: 'GearingType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearingType
        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_231.GearingTypes)(value) if value is not None else None

    @property
    def geometry_factor_i(self) -> 'float':
        """float: 'GeometryFactorI' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorI
        return temp

    @property
    def helical_overlap_factor(self) -> 'float':
        """float: 'HelicalOverlapFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelicalOverlapFactor
        return temp

    @property
    def improved_gearing(self) -> 'bool':
        """bool: 'ImprovedGearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ImprovedGearing
        return temp

    @property
    def lead_correction_factor(self) -> 'float':
        """float: 'LeadCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadCorrectionFactor
        return temp

    @property
    def load_distribution_factor(self) -> 'float':
        """float: 'LoadDistributionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactor
        return temp

    @property
    def load_distribution_factor_source(self) -> 'str':
        """str: 'LoadDistributionFactorSource' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadDistributionFactorSource
        return temp

    @property
    def load_sharing_ratio(self) -> 'float':
        """float: 'LoadSharingRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadSharingRatio
        return temp

    @property
    def materials_parameter(self) -> 'float':
        """float: 'MaterialsParameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialsParameter
        return temp

    @property
    def maximum_contact_temperature(self) -> 'float':
        """float: 'MaximumContactTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumContactTemperature
        return temp

    @property
    def maximum_flash_temperature(self) -> 'float':
        """float: 'MaximumFlashTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumFlashTemperature
        return temp

    @property
    def mean_coefficient_of_friction_calculated_constant_flash_temperature_method(self) -> 'float':
        """float: 'MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanCoefficientOfFrictionCalculatedConstantFlashTemperatureMethod
        return temp

    @property
    def mesh_alignment_correction_factor(self) -> 'float':
        """float: 'MeshAlignmentCorrectionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshAlignmentCorrectionFactor
        return temp

    @property
    def mesh_alignment_factor(self) -> 'float':
        """float: 'MeshAlignmentFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshAlignmentFactor
        return temp

    @property
    def minimum_contact_length(self) -> 'float':
        """float: 'MinimumContactLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumContactLength
        return temp

    @property
    def minimum_film_thickness(self) -> 'float':
        """float: 'MinimumFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumFilmThickness
        return temp

    @property
    def minimum_length_of_contact_lines_per_unit_module(self) -> 'float':
        """float: 'MinimumLengthOfContactLinesPerUnitModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumLengthOfContactLinesPerUnitModule
        return temp

    @property
    def minimum_specific_film_thickness(self) -> 'float':
        """float: 'MinimumSpecificFilmThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumSpecificFilmThickness
        return temp

    @property
    def normal_operating_load(self) -> 'float':
        """float: 'NormalOperatingLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalOperatingLoad
        return temp

    @property
    def normal_unit_load(self) -> 'float':
        """float: 'NormalUnitLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalUnitLoad
        return temp

    @property
    def operating_centre_distance(self) -> 'float':
        """float: 'OperatingCentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OperatingCentreDistance
        return temp

    @property
    def overload_factor(self) -> 'float':
        """float: 'OverloadFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OverloadFactor
        return temp

    @property
    def parameter_for_calculating_tooth_temperature(self) -> 'float':
        """float: 'ParameterForCalculatingToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParameterForCalculatingToothTemperature
        return temp

    @property
    def pinion_offset_from_bearing(self) -> 'float':
        """float: 'PinionOffsetFromBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionOffsetFromBearing
        return temp

    @property
    def pinion_proportion_factor(self) -> 'float':
        """float: 'PinionProportionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionProportionFactor
        return temp

    @property
    def pinion_proportion_modifier(self) -> 'float':
        """float: 'PinionProportionModifier' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionProportionModifier
        return temp

    @property
    def pressure_viscosity_coefficient(self) -> 'float':
        """float: 'PressureViscosityCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureViscosityCoefficient
        return temp

    @property
    def probability_of_scuffing(self) -> 'float':
        """float: 'ProbabilityOfScuffing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProbabilityOfScuffing
        return temp

    @property
    def probability_of_wear(self) -> 'float':
        """float: 'ProbabilityOfWear' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProbabilityOfWear
        return temp

    @property
    def profile_modification(self) -> '_989.CylindricalGearProfileModifications':
        """CylindricalGearProfileModifications: 'ProfileModification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileModification
        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_989.CylindricalGearProfileModifications)(value) if value is not None else None

    @property
    def rating_standard_name(self) -> 'str':
        """str: 'RatingStandardName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingStandardName
        return temp

    @property
    def scuffing_temperature(self) -> 'float':
        """float: 'ScuffingTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperature
        return temp

    @property
    def scuffing_temperature_method(self) -> '_1033.ScuffingTemperatureMethodsAGMA':
        """ScuffingTemperatureMethodsAGMA: 'ScuffingTemperatureMethod' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ScuffingTemperatureMethod
        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1033.ScuffingTemperatureMethodsAGMA)(value) if value is not None else None

    @property
    def second_distance_along_line_of_action(self) -> 'float':
        """float: 'SecondDistanceAlongLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SecondDistanceAlongLineOfAction
        return temp

    @property
    def sixth_distance_along_line_of_action(self) -> 'float':
        """float: 'SixthDistanceAlongLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SixthDistanceAlongLineOfAction
        return temp

    @property
    def size_factor_bending(self) -> 'float':
        """float: 'SizeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SizeFactorBending
        return temp

    @property
    def sliding_velocity_at_end_of_active_profile(self) -> 'float':
        """float: 'SlidingVelocityAtEndOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityAtEndOfActiveProfile
        return temp

    @property
    def sliding_velocity_at_pitch_point(self) -> 'float':
        """float: 'SlidingVelocityAtPitchPoint' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityAtPitchPoint
        return temp

    @property
    def sliding_velocity_at_start_of_active_profile(self) -> 'float':
        """float: 'SlidingVelocityAtStartOfActiveProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SlidingVelocityAtStartOfActiveProfile
        return temp

    @property
    def sump_temperature(self) -> 'float':
        """float: 'SumpTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SumpTemperature
        return temp

    @property
    def surface_condition_factor(self) -> 'float':
        """float: 'SurfaceConditionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceConditionFactor
        return temp

    @property
    def surface_roughness_constant(self) -> 'float':
        """float: 'SurfaceRoughnessConstant' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceRoughnessConstant
        return temp

    @property
    def temperature_factor(self) -> 'float':
        """float: 'TemperatureFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TemperatureFactor
        return temp

    @property
    def third_distance_along_line_of_action(self) -> 'float':
        """float: 'ThirdDistanceAlongLineOfAction' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThirdDistanceAlongLineOfAction
        return temp

    @property
    def tooth_temperature(self) -> 'float':
        """float: 'ToothTemperature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothTemperature
        return temp

    @property
    def transmission_accuracy_number(self) -> 'float':
        """float: 'TransmissionAccuracyNumber' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransmissionAccuracyNumber
        return temp

    @property
    def transverse_load_distribution_factor(self) -> 'float':
        """float: 'TransverseLoadDistributionFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseLoadDistributionFactor
        return temp

    @property
    def transverse_metric_module(self) -> 'float':
        """float: 'TransverseMetricModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseMetricModule
        return temp

    @property
    def gear_single_flank_ratings(self) -> 'List[_501.AGMA2101GearSingleFlankRating]':
        """List[AGMA2101GearSingleFlankRating]: 'GearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSingleFlankRatings
        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def agma_cylindrical_gear_single_flank_ratings(self) -> 'List[_501.AGMA2101GearSingleFlankRating]':
        """List[AGMA2101GearSingleFlankRating]: 'AGMACylindricalGearSingleFlankRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AGMACylindricalGearSingleFlankRatings
        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
