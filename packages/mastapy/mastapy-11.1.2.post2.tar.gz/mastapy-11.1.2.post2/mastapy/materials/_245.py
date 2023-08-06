﻿"""_245.py

Material
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.materials import _234, _248
from mastapy.utility.databases import _1605
from mastapy._internal.python_net import python_net_import

_MATERIAL = python_net_import('SMT.MastaAPI.Materials', 'Material')


__docformat__ = 'restructuredtext en'
__all__ = ('Material',)


class Material(_1605.NamedDatabaseItem):
    """Material

    This is a mastapy class.
    """

    TYPE = _MATERIAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Material.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def coefficient_of_thermal_expansion(self) -> 'float':
        """float: 'CoefficientOfThermalExpansion' is the original name of this property."""

        temp = self.wrapped.CoefficientOfThermalExpansion
        return temp

    @coefficient_of_thermal_expansion.setter
    def coefficient_of_thermal_expansion(self, value: 'float'):
        self.wrapped.CoefficientOfThermalExpansion = float(value) if value else 0.0

    @property
    def density(self) -> 'float':
        """float: 'Density' is the original name of this property."""

        temp = self.wrapped.Density
        return temp

    @density.setter
    def density(self, value: 'float'):
        self.wrapped.Density = float(value) if value else 0.0

    @property
    def hardness_type(self) -> '_234.HardnessType':
        """HardnessType: 'HardnessType' is the original name of this property."""

        temp = self.wrapped.HardnessType
        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_234.HardnessType)(value) if value is not None else None

    @hardness_type.setter
    def hardness_type(self, value: '_234.HardnessType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HardnessType = value

    @property
    def material_name(self) -> 'str':
        """str: 'MaterialName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialName
        return temp

    @property
    def maximum_allowable_temperature(self) -> 'float':
        """float: 'MaximumAllowableTemperature' is the original name of this property."""

        temp = self.wrapped.MaximumAllowableTemperature
        return temp

    @maximum_allowable_temperature.setter
    def maximum_allowable_temperature(self, value: 'float'):
        self.wrapped.MaximumAllowableTemperature = float(value) if value else 0.0

    @property
    def modulus_of_elasticity(self) -> 'float':
        """float: 'ModulusOfElasticity' is the original name of this property."""

        temp = self.wrapped.ModulusOfElasticity
        return temp

    @modulus_of_elasticity.setter
    def modulus_of_elasticity(self, value: 'float'):
        self.wrapped.ModulusOfElasticity = float(value) if value else 0.0

    @property
    def plane_strain_modulus(self) -> 'float':
        """float: 'PlaneStrainModulus' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlaneStrainModulus
        return temp

    @property
    def poissons_ratio(self) -> 'float':
        """float: 'PoissonsRatio' is the original name of this property."""

        temp = self.wrapped.PoissonsRatio
        return temp

    @poissons_ratio.setter
    def poissons_ratio(self, value: 'float'):
        self.wrapped.PoissonsRatio = float(value) if value else 0.0

    @property
    def shear_fatigue_strength(self) -> 'float':
        """float: 'ShearFatigueStrength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearFatigueStrength
        return temp

    @property
    def shear_modulus(self) -> 'float':
        """float: 'ShearModulus' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearModulus
        return temp

    @property
    def shear_yield_stress(self) -> 'float':
        """float: 'ShearYieldStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShearYieldStress
        return temp

    @property
    def standard(self) -> '_248.MaterialStandards':
        """MaterialStandards: 'Standard' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Standard
        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_248.MaterialStandards)(value) if value is not None else None

    @property
    def surface_hardness(self) -> 'float':
        """float: 'SurfaceHardness' is the original name of this property."""

        temp = self.wrapped.SurfaceHardness
        return temp

    @surface_hardness.setter
    def surface_hardness(self, value: 'float'):
        self.wrapped.SurfaceHardness = float(value) if value else 0.0

    @property
    def surface_hardness_range_max_in_hb(self) -> 'float':
        """float: 'SurfaceHardnessRangeMaxInHB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceHardnessRangeMaxInHB
        return temp

    @property
    def surface_hardness_range_max_in_hrc(self) -> 'float':
        """float: 'SurfaceHardnessRangeMaxInHRC' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceHardnessRangeMaxInHRC
        return temp

    @property
    def surface_hardness_range_max_in_hv(self) -> 'float':
        """float: 'SurfaceHardnessRangeMaxInHV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceHardnessRangeMaxInHV
        return temp

    @property
    def surface_hardness_range_min_in_hb(self) -> 'float':
        """float: 'SurfaceHardnessRangeMinInHB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceHardnessRangeMinInHB
        return temp

    @property
    def surface_hardness_range_min_in_hrc(self) -> 'float':
        """float: 'SurfaceHardnessRangeMinInHRC' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceHardnessRangeMinInHRC
        return temp

    @property
    def surface_hardness_range_min_in_hv(self) -> 'float':
        """float: 'SurfaceHardnessRangeMinInHV' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfaceHardnessRangeMinInHV
        return temp

    @property
    def tensile_yield_strength(self) -> 'float':
        """float: 'TensileYieldStrength' is the original name of this property."""

        temp = self.wrapped.TensileYieldStrength
        return temp

    @tensile_yield_strength.setter
    def tensile_yield_strength(self, value: 'float'):
        self.wrapped.TensileYieldStrength = float(value) if value else 0.0

    @property
    def ultimate_tensile_strength(self) -> 'float':
        """float: 'UltimateTensileStrength' is the original name of this property."""

        temp = self.wrapped.UltimateTensileStrength
        return temp

    @ultimate_tensile_strength.setter
    def ultimate_tensile_strength(self, value: 'float'):
        self.wrapped.UltimateTensileStrength = float(value) if value else 0.0
