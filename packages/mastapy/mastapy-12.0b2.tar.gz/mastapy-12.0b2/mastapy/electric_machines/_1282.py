"""_1282.py

SurfacePermanentMagnetRotor
"""


from mastapy.electric_machines import _1269
from mastapy._internal.python_net import python_net_import

_SURFACE_PERMANENT_MAGNET_ROTOR = python_net_import('SMT.MastaAPI.ElectricMachines', 'SurfacePermanentMagnetRotor')


__docformat__ = 'restructuredtext en'
__all__ = ('SurfacePermanentMagnetRotor',)


class SurfacePermanentMagnetRotor(_1269.PermanentMagnetRotor):
    """SurfacePermanentMagnetRotor

    This is a mastapy class.
    """

    TYPE = _SURFACE_PERMANENT_MAGNET_ROTOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SurfacePermanentMagnetRotor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
