"""_6596.py

ElectricMachineHarmonicLoadData
"""


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item
from mastapy.system_model.analyses_and_results.static_loads import _6630, _6704, _6680
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility_gui.charts import _1633
from mastapy.system_model.fe import _2135
from mastapy.math_utility import _1320
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadData',)


class ElectricMachineHarmonicLoadData(_6680.SpeedDependentHarmonicLoadData):
    """ElectricMachineHarmonicLoadData

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadData.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def apply_to_all_data_types(self) -> 'bool':
        """bool: 'ApplyToAllDataTypes' is the original name of this property."""

        temp = self.wrapped.ApplyToAllDataTypes
        return temp

    @apply_to_all_data_types.setter
    def apply_to_all_data_types(self, value: 'bool'):
        self.wrapped.ApplyToAllDataTypes = bool(value) if value else False

    @property
    def apply_to_all_speeds_for_selected_data_type(self) -> 'bool':
        """bool: 'ApplyToAllSpeedsForSelectedDataType' is the original name of this property."""

        temp = self.wrapped.ApplyToAllSpeedsForSelectedDataType
        return temp

    @apply_to_all_speeds_for_selected_data_type.setter
    def apply_to_all_speeds_for_selected_data_type(self, value: 'bool'):
        self.wrapped.ApplyToAllSpeedsForSelectedDataType = bool(value) if value else False

    @property
    def compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads(self) -> 'bool':
        """bool: 'CompareTorqueRippleAndStatorTorqueReactionDerivedFromStatorTangentialLoads' is the original name of this property."""

        temp = self.wrapped.CompareTorqueRippleAndStatorTorqueReactionDerivedFromStatorTangentialLoads
        return temp

    @compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads.setter
    def compare_torque_ripple_and_stator_torque_reaction_derived_from_stator_tangential_loads(self, value: 'bool'):
        self.wrapped.CompareTorqueRippleAndStatorTorqueReactionDerivedFromStatorTangentialLoads = bool(value) if value else False

    @property
    def constant_torque(self) -> 'float':
        """float: 'ConstantTorque' is the original name of this property."""

        temp = self.wrapped.ConstantTorque
        return temp

    @constant_torque.setter
    def constant_torque(self, value: 'float'):
        self.wrapped.ConstantTorque = float(value) if value else 0.0

    @property
    def data_type_for_force_distribution_and_temporal_spatial_harmonics_charts(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType':
        """enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType: 'DataTypeForForceDistributionAndTemporalSpatialHarmonicsCharts' is the original name of this property."""

        temp = self.wrapped.DataTypeForForceDistributionAndTemporalSpatialHarmonicsCharts
        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @data_type_for_force_distribution_and_temporal_spatial_harmonics_charts.setter
    def data_type_for_force_distribution_and_temporal_spatial_harmonics_charts(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DataTypeForForceDistributionAndTemporalSpatialHarmonicsCharts = value

    @property
    def data_type_for_scaling(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType':
        """enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType: 'DataTypeForScaling' is the original name of this property."""

        temp = self.wrapped.DataTypeForScaling
        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @data_type_for_scaling.setter
    def data_type_for_scaling(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DataTypeForScaling = value

    @property
    def display_interpolated_data(self) -> 'bool':
        """bool: 'DisplayInterpolatedData' is the original name of this property."""

        temp = self.wrapped.DisplayInterpolatedData
        return temp

    @display_interpolated_data.setter
    def display_interpolated_data(self, value: 'bool'):
        self.wrapped.DisplayInterpolatedData = bool(value) if value else False

    @property
    def force_distribution(self) -> 'Image':
        """Image: 'ForceDistribution' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceDistribution
        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def force_distribution_3d(self) -> '_1633.ThreeDVectorChartDefinition':
        """ThreeDVectorChartDefinition: 'ForceDistribution3D' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceDistribution3D
        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def invert_axis(self) -> 'bool':
        """bool: 'InvertAxis' is the original name of this property."""

        temp = self.wrapped.InvertAxis
        return temp

    @invert_axis.setter
    def invert_axis(self, value: 'bool'):
        self.wrapped.InvertAxis = bool(value) if value else False

    @property
    def plot_as_vectors(self) -> 'bool':
        """bool: 'PlotAsVectors' is the original name of this property."""

        temp = self.wrapped.PlotAsVectors
        return temp

    @plot_as_vectors.setter
    def plot_as_vectors(self, value: 'bool'):
        self.wrapped.PlotAsVectors = bool(value) if value else False

    @property
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(self) -> 'float':
        """float: 'RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff
        return temp

    @rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off.setter
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff = float(value) if value else 0.0

    @property
    def rotor_x_force_amplitude_cut_off(self) -> 'float':
        """float: 'RotorXForceAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorXForceAmplitudeCutOff
        return temp

    @rotor_x_force_amplitude_cut_off.setter
    def rotor_x_force_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorXForceAmplitudeCutOff = float(value) if value else 0.0

    @property
    def rotor_y_force_amplitude_cut_off(self) -> 'float':
        """float: 'RotorYForceAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorYForceAmplitudeCutOff
        return temp

    @rotor_y_force_amplitude_cut_off.setter
    def rotor_y_force_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorYForceAmplitudeCutOff = float(value) if value else 0.0

    @property
    def rotor_z_force_amplitude_cut_off(self) -> 'float':
        """float: 'RotorZForceAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorZForceAmplitudeCutOff
        return temp

    @rotor_z_force_amplitude_cut_off.setter
    def rotor_z_force_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorZForceAmplitudeCutOff = float(value) if value else 0.0

    @property
    def scale(self) -> 'float':
        """float: 'Scale' is the original name of this property."""

        temp = self.wrapped.Scale
        return temp

    @scale.setter
    def scale(self, value: 'float'):
        self.wrapped.Scale = float(value) if value else 0.0

    @property
    def selected_tooth(self) -> 'list_with_selected_item.ListWithSelectedItem_FESubstructureNode':
        """list_with_selected_item.ListWithSelectedItem_FESubstructureNode: 'SelectedTooth' is the original name of this property."""

        temp = self.wrapped.SelectedTooth
        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_FESubstructureNode)(temp) if temp is not None else None

    @selected_tooth.setter
    def selected_tooth(self, value: 'list_with_selected_item.ListWithSelectedItem_FESubstructureNode.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.SelectedTooth = value

    @property
    def show_all_forces(self) -> 'bool':
        """bool: 'ShowAllForces' is the original name of this property."""

        temp = self.wrapped.ShowAllForces
        return temp

    @show_all_forces.setter
    def show_all_forces(self, value: 'bool'):
        self.wrapped.ShowAllForces = bool(value) if value else False

    @property
    def show_all_teeth(self) -> 'bool':
        """bool: 'ShowAllTeeth' is the original name of this property."""

        temp = self.wrapped.ShowAllTeeth
        return temp

    @show_all_teeth.setter
    def show_all_teeth(self, value: 'bool'):
        self.wrapped.ShowAllTeeth = bool(value) if value else False

    @property
    def speed_to_view(self) -> 'float':
        """float: 'SpeedToView' is the original name of this property."""

        temp = self.wrapped.SpeedToView
        return temp

    @speed_to_view.setter
    def speed_to_view(self, value: 'float'):
        self.wrapped.SpeedToView = float(value) if value else 0.0

    @property
    def stator_axial_loads_amplitude_cut_off(self) -> 'float':
        """float: 'StatorAxialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.StatorAxialLoadsAmplitudeCutOff
        return temp

    @stator_axial_loads_amplitude_cut_off.setter
    def stator_axial_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.StatorAxialLoadsAmplitudeCutOff = float(value) if value else 0.0

    @property
    def stator_radial_loads_amplitude_cut_off(self) -> 'float':
        """float: 'StatorRadialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.StatorRadialLoadsAmplitudeCutOff
        return temp

    @stator_radial_loads_amplitude_cut_off.setter
    def stator_radial_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.StatorRadialLoadsAmplitudeCutOff = float(value) if value else 0.0

    @property
    def stator_tangential_loads_amplitude_cut_off(self) -> 'float':
        """float: 'StatorTangentialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.StatorTangentialLoadsAmplitudeCutOff
        return temp

    @stator_tangential_loads_amplitude_cut_off.setter
    def stator_tangential_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.StatorTangentialLoadsAmplitudeCutOff = float(value) if value else 0.0

    @property
    def sum_over_all_nodes(self) -> 'bool':
        """bool: 'SumOverAllNodes' is the original name of this property."""

        temp = self.wrapped.SumOverAllNodes
        return temp

    @sum_over_all_nodes.setter
    def sum_over_all_nodes(self, value: 'bool'):
        self.wrapped.SumOverAllNodes = bool(value) if value else False

    @property
    def torque_ripple_amplitude_cut_off(self) -> 'float':
        """float: 'TorqueRippleAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.TorqueRippleAmplitudeCutOff
        return temp

    @torque_ripple_amplitude_cut_off.setter
    def torque_ripple_amplitude_cut_off(self, value: 'float'):
        self.wrapped.TorqueRippleAmplitudeCutOff = float(value) if value else 0.0

    @property
    def torque_ripple_input_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType':
        """enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType: 'TorqueRippleInputType' is the original name of this property."""

        temp = self.wrapped.TorqueRippleInputType
        value = enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @torque_ripple_input_type.setter
    def torque_ripple_input_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.TorqueRippleInputType = value

    @property
    def use_stator_radius_from_masta_model(self) -> 'bool':
        """bool: 'UseStatorRadiusFromMASTAModel' is the original name of this property."""

        temp = self.wrapped.UseStatorRadiusFromMASTAModel
        return temp

    @use_stator_radius_from_masta_model.setter
    def use_stator_radius_from_masta_model(self, value: 'bool'):
        self.wrapped.UseStatorRadiusFromMASTAModel = bool(value) if value else False

    @property
    def excitations(self) -> 'List[_1320.FourierSeries]':
        """List[FourierSeries]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Excitations
        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
