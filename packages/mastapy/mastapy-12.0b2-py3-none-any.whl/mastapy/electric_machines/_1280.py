"""_1280.py

StatorRotorMaterialDatabase
"""


from mastapy.materials import _264
from mastapy.electric_machines import _1279
from mastapy._internal.python_net import python_net_import

_STATOR_ROTOR_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.ElectricMachines', 'StatorRotorMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('StatorRotorMaterialDatabase',)


class StatorRotorMaterialDatabase(_264.MaterialDatabase['_1279.StatorRotorMaterial']):
    """StatorRotorMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _STATOR_ROTOR_MATERIAL_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StatorRotorMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
